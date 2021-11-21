import os

from rich.console import CaptureError, Console
from rich.errors import MissingStyle

console = Console(highlight=False)


class HelpStylesException(Exception):
    pass


def _get_rich_output(text: str = None, style: str = None) -> str:
    try:
        with console.capture() as capture:
            console.print(text, style=style, end="")
        return capture.get()
    except MissingStyle:
        raise ValueError
    except CaptureError:
        raise ValueError(f"Error capturing output for text: {text} and style: {style}")


def _apply_rich(text: str) -> str:
    try:
        with console.capture() as capture:
            console.print(text, end="")
        return capture.get()
    except MissingStyle:
        raise ValueError(f"Error: error in help string {text}")


def _colorize(text: str = None, style: str = None, suffix: str = None) -> str:
    if not style or "NO_COLOR" in os.environ:
        return (text or "") + (suffix or "")
    try:
        return _get_rich_output(text, style) + (suffix or "")
    except ValueError:
        raise HelpStylesException(f"Unknown style {style}")
