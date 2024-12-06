import sys
from asyncio import CancelledError, create_task
from asyncio import run as await_task
from asyncio import sleep as async_sleep
from functools import wraps
from math import ceil
from os import environ
from os import get_terminal_size as os_terminal_size
from threading import Thread
from time import sleep as sync_sleep
from types import MethodType
from typing import Any, Callable, Iterable, Optional
from typing import TextIO as Stream
from unicodedata import category, combining, east_asian_width

if sys.platform == "win32":

    def _():
        """
        Enable windows virtual terminal processing so
        escape codes and colors work.
        """
        try:
            from ctypes import byref, c_ulong, windll
        except ImportError:
            return
        VT_PROCESSING = 0x0004
        OUTPUT_HANDLE = -11
        kernel32 = windll.kernel32
        GetStdHandle = kernel32.GetStdHandle
        GetConsoleMode = kernel32.GetConsoleMode
        SetConsoleMode = kernel32.SetConsoleMode

        handle = GetStdHandle(OUTPUT_HANDLE)
        mode = c_ulong()
        GetConsoleMode(handle, byref(mode))
        mode.value |= VT_PROCESSING
        SetConsoleMode(handle, mode)

    echo = None
    _()

else:
    import termios
    from sys import stdin

    class echo:
        """
        Used to disable keystrokes from
        being echoed when the spinner is running.
        """

        fd = stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        @classmethod
        def disable(cls):
            new_settings = termios.tcgetattr(cls.fd)
            new_settings[3] = new_settings[3] & ~termios.ECHO
            termios.tcsetattr(cls.fd, termios.TCSADRAIN, new_settings)

        @classmethod
        def enable(cls):
            termios.tcsetattr(cls.fd, termios.TCSADRAIN, cls.old_settings)


def get_terminal_size(fallback: tuple[int, int] = (80, 24)):
    try:
        columns = max(int(environ.get("COLUMNS", 0)), 0)
    except ValueError:
        columns = 0

    try:
        lines = max(int(environ.get("LINES", 0)), 0)
    except ValueError:
        lines = 0

    if not (columns and lines):
        try:
            columns, lines = os_terminal_size(sys.stdout.fileno())
        except (AttributeError, ValueError, OSError):
            pass

    return columns or fallback[0], lines or fallback[0]


def wcwidth(char: str) -> int:
    if not char:
        return 0
    if category(char) in ["Cc", "Cf"]:
        return -1
    if combining(char):
        return 0
    width = east_asian_width(char)
    if width in ["W", "F"]:
        return 2
    return 1


def walk_text(text: str):
    met_escape = False
    for i in text:
        if i == "m" or i == " ":
            if met_escape:
                met_escape = False
                yield i.encode(), 0
                continue
        elif i == "\x1b":
            met_escape = True
        yield i.encode(), not met_escape and wcwidth(i)


class cursor:
    @staticmethod
    def hide(stream: Stream):
        if echo:
            echo.disable()
        stream.write("\x1b[?25l")
        stream.flush()

    @staticmethod
    def show(stream: Stream):
        if echo:
            echo.enable()
        stream.write("\x1b[?25h")
        stream.flush()
        pass

    @staticmethod
    def move_up(stream: Stream, lines: int):
        stream.write(f"\x1b[{lines}A")
        stream.flush()

    @staticmethod
    def clear(stream: Stream, lines: int):
        for _ in range(lines):
            stream.write("\x1b[F\x1b[K")
        stream.flush()


class Renderer:
    def __init__(self, stream: Stream) -> None:
        self.grid: tuple[int, int, int] = 0, 0, 0
        self.stream = stream
        self.isatty = stream.isatty()

    def render(self, buffer: str):
        stream = self.stream
        column, lines = get_terminal_size()
        prevmaxcol, prevheight, _ = self.grid
        maxcol = 0
        if lines < 2:
            return
        self.flush()
        rows = buffer.splitlines()
        height = 0
        for row in rows:
            if height >= lines - 1:
                break

            width = 0
            break_out = False

            for char, length in walk_text(row):
                width += length
                stream.buffer.write(char)
                if width >= column:
                    height += 1
                    if height >= lines - 1:
                        break_out = True
                        break

            maxcol = max(maxcol, width)
            if break_out:
                break

            if width < prevmaxcol:
                fill = min(prevmaxcol, column)
                for _ in range(fill - width):
                    stream.buffer.write(b" ")
            stream.buffer.write(b"\r\n")
            height += 1
        cfill = b" " * prevmaxcol
        dh = 0
        if height < prevheight:
            dh = prevheight - height
            for _ in range(dh):
                stream.buffer.write(cfill)
                stream.buffer.write(b"\r\n")

        self.grid = (maxcol or column), height, dh

    def clear(self):
        width, height, dh = self.grid
        height = height + dh
        if not height:
            return
        column, _ = get_terminal_size()
        lines = ceil(width / column) * height if column < width else height
        cursor.clear(self.stream, lines + dh)
        self.grid = 0, 0, 0

    def flush(self):
        width, height, dh = self.grid
        height = height + dh
        if not height:
            return
        _, lines = get_terminal_size()
        cursor.move_up(self.stream, min(height, lines))
        self.grid = width, height, 0


class Frames:
    def __init__(self, format: str, label: str, frames: Iterable[str]) -> None:
        self.label = label
        self.frames = list(frames)
        self.format = format
        self.iterable = iter(self)
        self.breakoff = False

    def __iter__(self):
        while True:
            for frame in self.frames:
                if self.breakoff:
                    self.breakoff = False
                    break
                yield self.format.format(frame=frame, label=self.label)

    def __next__(self):
        return next(self.iterable)


class CustomFrames:
    def __init__(self, format: Callable[[], str]) -> None:
        self.format = format
        self.iterable = iter(self)

    def __iter__(self):
        while True:
            yield self.format()

    def __next__(self):
        return next(self.iterable)


__spinner__ = None
__force__ = False

DEFAULT_STREAM = sys.stdout.isatty() and sys.stdout or sys.stderr


class BaseSpinner:
    def __init__(
        self,
        fps: int,
        stream: Stream,
    ) -> None:
        self.runner = None
        self.delayms = 1 / fps
        self.buffer = ""
        self.running = False
        self.framer: Any
        self.renderer = Renderer(stream or DEFAULT_STREAM)

    def echo(
        self,
        *text: Any,
        sep: Optional[str] = None,
        end: Optional[str] = None,
    ) -> None:
        log = (sep or "").join(map(str, text)) + (end or "\n")
        if __spinner__:
            __spinner__.buffer = f"{__spinner__.buffer}{log}"
        elif not self.renderer.isatty:
            self.renderer.stream.buffer.write(log.encode("utf-8"))
            self.renderer.stream.flush()
            return
        else:
            self.renderer.stream.write(log)
            self.renderer.stream.flush()

    def render(self):
        if self.buffer:
            self.renderer.clear()
            self.renderer.stream.buffer.write(self.buffer.encode("utf-8"))
            self.buffer = ""
            return
        self.renderer.render(next(self.framer))


class SimpleSpinner(BaseSpinner):
    def __init__(
        self,
        frames: Optional[Iterable[str]] = None,
        label: Optional[str] = None,
        fps: Optional[int] = None,
        format: Optional[str] = None,
        stream: Optional[Stream] = None,
    ) -> None:
        super().__init__(max((fps or 50), 0) or 50, stream or DEFAULT_STREAM)
        self.framer = Frames(
            format or "{frame} {label}",
            label or "",
            frames or r"\|/-",
        )

    @property
    def format(self) -> str:
        return self.framer.format

    @format.setter
    def format(self, format: str) -> None:
        self.framer.format = format

    @property
    def fps(self) -> int:

        return int(self.delayms * 1000)

    @fps.setter
    def fps(self, fps: int) -> None:
        if 0 < fps:
            self.delayms = fps / 1000

    @property
    def frames(self) -> list[str]:
        return self.framer.frames

    @frames.setter
    def frames(self, frames: Iterable[str]) -> None:
        self.framer.breakoff = True
        self.framer.frames = list(frames)

    @property
    def label(self) -> str:
        return self.framer.label

    @label.setter
    def label(self, label: str) -> None:
        self.framer.label = label


class CustomSpinner(BaseSpinner):
    def __init__(
        self,
        fps: Optional[int] = None,
        stream: Optional[Stream] = None,
    ) -> None:
        super().__init__(max(fps or 50, 0) or 50, stream or DEFAULT_STREAM)
        self.framer = CustomFrames(self.frame)

    @property
    def format(self) -> Callable[[Any], str]:
        return self.framer.format

    @format.setter
    def format(self, format: Callable[[Any], str]) -> None:
        self.framer.format = format

    @property
    def fps(self) -> int:
        return int(self.delayms * 1000)

    @fps.setter
    def fps(self, fps: int) -> None:
        if fps > 0:
            self.delayms = fps / 1000

    @property
    def frames(self) -> list[Any]:
        return self.framer.frames

    @frames.setter
    def frames(self, frames: Any) -> None:
        self.framer.frames = frames

    def frame(self) -> str:
        raise NotImplementedError("The view method is not implemented.")


class SyncRuntime:
    renderer: Renderer
    delayms: float
    buffer: str
    render: Callable[..., Any]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_: Any) -> None:
        self.stop()

    def run(self):
        cursor.hide(self.renderer.stream)
        while True:
            self.render()
            sync_sleep(self.delayms)
            if not self.running:
                self.renderer.clear()
                break
        cursor.show(self.renderer.stream)

    def start(self, force: bool = False) -> None:
        global __spinner__
        if __spinner__:
            return
        if not self.renderer.isatty and not (force or __force__):
            return
        __spinner__ = self
        self.running = True
        self.runner = Thread(target=self.run, daemon=True)
        self.runner.start()

    def stop(self, epilogue: Optional[str] = None) -> None:
        global __spinner__
        if not __spinner__:
            return
        if __spinner__ is not self:

            return stop(epilogue)
        __spinner__ = None
        self.running = False
        if self.runner:
            self.runner.join()
        epilogue = epilogue or ""
        if epilogue:
            epilogue = f"{epilogue}\n"
        if self.buffer:
            epilogue = f"{self.buffer}{epilogue}"
        self.renderer.stream.buffer.write(epilogue.encode())
        self.renderer.stream.flush()

    def bind(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(self: Any, *args: Any, **kwargs: Any):
            with self:
                return fn(self, *args, **kwargs)

        return MethodType(wrapper, self)


class AsyncRuntime:
    renderer: Renderer
    render: Callable[..., Any]
    delayms: float
    buffer: str

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.stop()

    async def run(self):
        cursor.hide(self.renderer.stream)
        while True:
            self.render()
            await async_sleep(self.delayms)
            if not self.running:
                self.renderer.clear()
                break
        cursor.show(self.renderer.stream)

    async def start(self, force: bool = False) -> None:
        global __spinner__
        if __spinner__:
            return
        if not self.renderer.isatty and not (force or __force__):
            return
        __spinner__ = self
        self.running = True
        self.runner = create_task(self.run())

    async def stop(self, epilogue: Optional[str] = None) -> None:
        global __spinner__
        if not __spinner__:
            return
        if __spinner__ is not self:
            return stop(epilogue)
        __spinner__ = None
        self.running = False
        if self.runner:
            try:
                await self.runner
            except CancelledError:
                pass
        epilogue = epilogue or ""
        if epilogue:
            epilogue = f"{epilogue}\n"
        if self.buffer:
            epilogue = f"{self.buffer}{epilogue}"
        self.renderer.stream.write(epilogue)

    def bind(self, fn: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(fn)
        async def wrapper(self: Any, *args: Any, **kwargs: Any):
            async with self:
                return fn(self, *args, **kwargs)

        return MethodType(wrapper, self)


def stop(epilogue: str | None = None):
    if __spinner__:
        if isinstance(__spinner__, SyncRuntime):
            __spinner__.stop(epilogue)
        else:
            await_task(__spinner__.stop())


class Spinner(SimpleSpinner, SyncRuntime):
    pass


class AsyncSpinner(SimpleSpinner, AsyncRuntime):
    pass


class Xspin(CustomSpinner, SyncRuntime):
    pass


class AsyncXspin(CustomSpinner, AsyncRuntime):
    pass


def force():
    global __force__
    __force__ = True
