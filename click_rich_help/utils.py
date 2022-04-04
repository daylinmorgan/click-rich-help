from typing import Union

from rich.console import CaptureError, Console
from rich.style import Style


def _colorize(
    console: Console,
    text: str = None,
    style: Union[str, Style] = None,
    suffix: str = None,
) -> str:
    try:
        with console.capture() as capture:
            console.print(text, style=style, end="")
        return capture.get() + (suffix or "")
    except CaptureError:
        raise ValueError(f"Error capturing output for text: {text} and style: {style}")
