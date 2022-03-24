import os
from typing import Union

from rich.console import CaptureError, Console
from rich.style import Style


def _get_rich_output(
    console: Console, text: str = None, style: Union[str, Style] = None
) -> str:
    try:
        with console.capture() as capture:
            console.print(text, style=style, end="")
        return capture.get()
    except CaptureError:
        raise ValueError(f"Error capturing output for text: {text} and style: {style}")


def _colorize(
    console: Console,
    text: str = None,
    style: Union[str, Style] = None,
    suffix: str = None,
) -> str:
    if not style or "NO_COLOR" in os.environ:
        return (text or "") + (suffix or "")
    else:
        return _get_rich_output(console, text, style) + (suffix or "")
