import io
import os

from click.termui import _ansi_colors, _ansi_reset_all
from rich.console import CaptureError, Console
from rich.errors import MissingStyle
from rich.text import Text

console = Console()


class HelpColorsException(Exception):
    pass


def _get_rich_output(text, color):
    try:
        with console.capture() as capture:
            console.print(text, style=color, end="")
        return capture.get()
    except MissingStyle:
        raise ValueError
    except CaptureError:
        raise ValueError(f"Error capturing output for text: {text} and style: {color}")


def _apply_rich(help_text):
    try:
        with console.capture() as capture:
            console.print(help_text, end="")
        return capture.get()
    except CaptureError:
        raise ValueError("error in help style")


def _colorize(text, color=None, suffix=None):
    if not color or "NO_COLOR" in os.environ:
        return text + (suffix or "")
    try:
        return _get_rich_output(text, color) + (suffix or "")
    except ValueError:
        raise HelpColorsException("Unknown color %r" % color)


def _extend_instance(obj, cls):
    """Apply mixin to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (cls, base_cls), {})
