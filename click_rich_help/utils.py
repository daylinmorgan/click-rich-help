import os

from rich.console import CaptureError, Console
from rich.errors import MissingStyle

console = Console(highlight=False)


class HelpStylesException(Exception):
    pass


def _get_rich_output(text, style):
    try:
        with console.capture() as capture:
            console.print(text, style=style, end="")
        return capture.get()
    except MissingStyle:
        raise ValueError
    except CaptureError:
        raise ValueError(f"Error capturing output for text: {text} and style: {style}")


def _apply_rich(text):
    try:
        with console.capture() as capture:
            console.print(text, end="")
        return capture.get()
    except MissingStyle:
        raise ValueError(f"Error: error in help string {text}")


def _colorize(text, style=None, suffix=None):
    if not style or "NO_COLOR" in os.environ:
        return text + (suffix or "")
    try:
        return _get_rich_output(text, style) + (suffix or "")
    except ValueError:
        raise HelpStylesException(f"Unknown style {style}")


def _extend_instance(obj, cls):
    """Apply mixin to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (cls, base_cls), {})
