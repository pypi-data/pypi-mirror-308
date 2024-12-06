# Xspin
Python module for creating spinners in the terminal.

# Xspin

Python module for creating spinners in the console.

## Features
* Synchronous spinners
* Asynchronous spinners
* Custom spinner frames and text
* Multiline spinner frames.
* Support for windows Console Host.

## Installation
```bash
pip install xspin
```

## Chosing a spinner
The choice of a spinner depends on the type of task being run.
- Blocking tasks should use `Spinner` or `Xspin` since they run on a separate thread.
- Asynchronous tasks should use
`AsyncSpinner` or `AsyncXspin`.

## Spinner Variants
Spinners are classified based on the way they generate frames.

- ### Simple Spinners 
These take in an iterable of characters representing the changing part of the spinner frames and text for the label. They use python defaults format template syntax to define the position of the characters (`frame`) and the text in the label. These are `Spinner` and `AsyncSpinner`.

```python
from xspin import Spinner 
spinner = Spinner(
    frames = r"\|/-",
    label = "Some text",
    format = "{frame} {label}"
)
```

- ### Custom Spinners
These are inherited from and define a method in the subclass called `frame` that returns a string. This method is called on each frame render.

```python
from xspin import Xspin

count = 0 # Some external state

class Spinner(Xspin):
    def frame(self):
        return f"Some text{count}"      
```

## Running a spinner
There are three ways a spinner can be run.

- ### `start` and `stop` methods.
    All spinners contain a start and stop method 
    which can be called to start and stop the
    spinner instance respectively.

- ## Context manager.
    Spinner instances support the context manager
    protocal. Remember to use `async with` for the async spinners. This starts and stops
    the spinner automatically.

```python
spinner = Spinner()
with spinner:
    do_work()
```

For async spinners:

```python
spinner = AsyncSpinner()
async main():
    async with spinner:
        await do_work()
```


- ## Binding to a function.
    Spinner instances contain the `bind` method which acts like a decorator, for binding the 
    spinner to a function. The function should take in a spinner instance as its first parameter.

```python
spinner = Spinner()

@spinner.bind
def work(spinner: Spinner):
    ...

work()
```

For async spinners:

```python
spinner = AsyncSpinner()

@spinner.bind
async def work(spinner: AsyncSpinner):
    ...

async def main():
    await work()
```

## Logging
During spinner progress, the `echo` method should be used for logging to ensure the spinner animation is
not ruined.

```python
with spinner as sp:
    sp.echo("Doing something")
    sp.echo("Done!")
```

## Stream
The default stream that the spinner is rendered is
`stdout`. If `stdout` is not `tty`, it uses `stderr` and if `stderr` is not `tty`, then the spinner is not rendered. This is to ensure the spinner is not rendered when the process's output is redirected to a file. You can pass in `True` to the `start` method of the spinner to force it to be rendered regardless, or use the global `force` function. This can be useful
when using a program like [`ttyd`](https://github.com/tsl0922/ttyd) or [`vhs`](https://github.com/charmbracelet/vhs).

## Examples
- ![Simple sync](examples/simple_sync_example.py)
- ![Simple async](examples/simple_async_example.py)
- ![Bound function](examples/bound_method_example.py)
- ![Custom](examples/custom_example.py)

## LICENSE
[MIT](LICENSE)
