"""
Module for creating console spinners.

## Chosing a spinner
This depends on how the task is running. If blocking,
the threaded spinners are used `Spinner`, `Xspin` and if async,
the async spinners `AsyncSpinner, AsyncXspin` are used.

## Spinner Variants.
There are two variants of spinners provided by the module based on
how the spinner frames are generated, ie
simple and custom .

- ### simple 
    These generate the spinner from an iterable of characters (frames) and
    some predefined text (label). Their position relative to each
    other is determined by a python format string with `frame` and `label` 
    fields. They are `Spinner` and `AsyncSpinner`

- ### custom
    These are inherited from and implement a `frame` method which returns 
    a string representing the current frame of the spinner. The sub-class
    can store its own state and use it to generate the spinner frame.
    They are `Xspin` and `AsyncXspin`

## Running a spinner.

Once an instance is created, each variant supports the following ways to
start and stop.

- ### start and stop
    These are methods called to, well, start and stop the spinner.

- ### context manager
    Spinner instances can be used with the `with` statement. For async spinners,
    `async with` should be used instead. The spinner is started and stopped
    automatically.

- ### bind
    This is a method that binds the spinner instance to a function. It 
    decorates a function that takes in the spinner instance as the first 
    argument and returns a bound method such that the spinner runs
    in the background when the function is called.

## Logging during spinner progress.
The `echo` should be used in order to ensure the animation is not 
ruined.

"""

from typing import (
    Any,
    Callable,
    Concatenate,
    Coroutine,
    Iterable,
    Optional,
    Self,
    TextIO,
    TypeVar,
    ParamSpec,
)

PS = ParamSpec("PS")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

class SimpleSpinner:
    def __init__(
        self,
        frames: Optional[Iterable[str]] = None,
        label: Optional[str] = None,
        fps: Optional[int] = None,
        format: Optional[str] = None,
        stream: Optional[TextIO] = None,
    ) -> None:
        """
        ## Parameters

        - `frames`
            An iterable of strings representing the frames of the spinner animation.

        - `label`
            The text attatched to the spinner frames based on the format provided.

        - `fps`
            The number of frames to show per second.

        - `format`
            The rule defining how the spinner frames and label are rendered next
            to each other. It should contain `frame` and `label` as fields.

        - `stream`:
            The output stream where the spinner should be rendered. By default, it
            uses stdout if its tty and fallbacks to stderr if the stdout is redirected
            to a non-terminal pipe.
        """

    @property
    def format(self) -> str:
        pass

    @format.setter
    def format(self, format: str) -> None:
        pass

    @property
    def fps(self) -> int:
        pass

    @fps.setter
    def fps(self, fps: int) -> None:
        pass

    @property
    def frames(self) -> list[str]:
        pass

    @frames.setter
    def frames(self, frames: Iterable[str]) -> None:
        pass

    @property
    def label(self) -> str:
        pass

    @label.setter
    def label(self, label: str) -> None:
        pass

class CustomSpinner:
    def __init__(
        self,
        fps: Optional[int] = None,
        stream: Optional[TextIO] = None,
    ) -> None:
        """
        ## Parameters

        - `fps`
            The number of frames to show per second.

        - `stream`
            The output stream where the spinner is rendered. Defaults to `stdout`
            and fallbacks to `stderr` if stdout is redirected to a pipe that
            is not a terminal handle.
        """

    @property
    def fps(self) -> int:
        pass

    @fps.setter
    def fps(self, fps: int) -> None:
        pass

    def frame(self) -> str:
        """
        This method is called on each render an should return
        the current spinner frame.
        """

class SyncRuntime:
    def __enter__(self) -> Self:
        pass

    def __exit__(self, *_: Any) -> None:
        pass

    def start(self, force: bool = False) -> None:
        """
        Starts the spinner if its not running already.
        If another spinner happens to be running, this one
        doesn't start.

        ## Parameter
        - `force`
            Forces the spinner to be renderered regardless of
            whether the output stream is tty.
        """

    def stop(self, epilogue: Optional[str] = None) -> None:
        """
        Stops the spinner.

        ## Parameter
        - `epilogue`
            The string that's shown when the last frame is cleared.
        """

    def bind(self, fn: Callable[Concatenate[Self, PS], R]) -> Callable[PS, R]:
        """
        Binds the spinner to a function such that the spinner runs in
        the background when the function is called.

        ## Parameter
        - `fn`
            The function to bind the spinner to. It should take in the spinner
            instance as its fast parameter.
        """

    def echo(
        self,
        *values: Any,
        sep: Optional[str] = None,
        end: Optional[str] = None,
    ) -> None:
        """
        Used for logging when the spinner is running without interfering with the
        spinner being rendered.

        ## Parameters

        - `values`
            The values to log.

        - `sep`
            The string to be used to join the values into a string.
            Defaults to space.

        - `end`
            The string to be printed at the end of the log.
            Defaults to the new line character.
        """

class AsyncRuntime:
    async def __aenter__(self) -> Self:
        pass

    async def __aexit__(self, *_: Any) -> None:
        pass

    async def start(self) -> None:
        """
        Starts the async spinner if its not running already.
        If another is running, it doesn't start.

        ## Parameter
        - `force`
            Forces the spinner to be renderered regardless of
            whether the output stream is tty.
        """

    async def stop(self, epilogue: Optional[str] = None) -> None:
        """
        Stops the async spinner if its running.
        It logs out the epilogue once the last frame is cleared.
        """

    def bind(
        self,
        fn: Callable[Concatenate[Self, PS], Coroutine[A, B, C]],
    ) -> Callable[PS, Coroutine[A, B, C]]:
        """
        Binds the spinner instance to an async function.

        ## Parameter

        - `fn`
            The async function to bind the spinner to. It should take in the spinner
            instance as its fast parameter.
        """

    def echo(
        self,
        *text: Any,
        sep: Optional[str] = None,
        end: Optional[str] = None,
    ) -> None:
        """
        Used for logging when the spinner is running without interfering with the
        spinner being rendered.

        ## Parameters

        - `values`
            The values to log.

        - `sep`
            The string to be used to join the values into a string.
            Defaults to space.

        - `end`
            The string to be printed at the end of the log.
            Defaults to the new line character.
        """

class Spinner(SimpleSpinner, SyncRuntime):
    pass

class AsyncSpinner(SimpleSpinner, AsyncRuntime):
    pass

class Xspin(CustomSpinner, SyncRuntime):
    pass

class AsyncXspin(CustomSpinner, AsyncRuntime):
    pass

def force() -> None:
    """Force spinner rendering regardless of whether the stream is tty."""

def stop() -> None:
    """Stops any currently running spinner."""
