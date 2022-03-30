import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import click
from click.formatting import wrap_text
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from .utils import _colorize

CLICK_STYLES = ["header", "option", "metavar", "doc_style", "default"]


class HelpStylesFormatter(click.HelpFormatter):
    option_regex = re.compile(r"-{1,2}[\w\-]+")
    defaults_regex = re.compile(r"  \[default: (.*)\]")

    def __init__(
        self,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        option_custom_styles: Dict[str, str] = None,
        max_width: int = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.styles = self._get_styles(styles, theme)
        self.option_custom_styles = option_custom_styles
        self.console = self._load_console()
        super(HelpStylesFormatter, self).__init__(
            width=self._get_width(max_width), *args, **kwargs
        )

    def _get_width(self, max_width) -> int:
        if max_width is None:
            max_width = 120
        width = min((self.console.width - 2), (max_width - 2))
        return width

    def _get_styles(
        self,
        user_styles: Optional[Dict[str, Union[str, Style]]],
        theme: Optional[Theme],
    ) -> Dict[str, Union[str, Style]]:

        styles: Dict[str, Union[str, Style]] = {k: "none" for k in CLICK_STYLES}
        additions: Dict[str, Union[str, Style]] = {}
        if user_styles:
            if isinstance(user_styles, dict):
                additions = user_styles
            else:
                raise ValueError(
                    (
                        f"Invalid styles: {user_styles}\n\n"
                        "Styles must be a dict containing valid names/styles. "
                        "See rich for more info"
                    )
                )
        if theme:
            additions.update(theme.styles)

        # validate style definition and update
        styles.update(
            {
                name: style if isinstance(style, Style) else Style.parse(style)
                for name, style in additions.items()
            }
        )

        return styles

    def _load_console(self) -> Console:
        return Console(
            theme=Theme(self.styles, inherit=False),
            highlight=False,
            force_terminal=True,
        )

    def _get_opt_names(self, option_name: str) -> List[str]:
        opts = self.option_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name: str) -> Union[str, Style]:
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if self.option_custom_styles and (opt in self.option_custom_styles.keys()):
                return self.option_custom_styles[opt]
        return self.styles["option"]

    def _extract_metavar_choices(self, option_name: str) -> str:
        metavar = self.option_regex.sub("", option_name).replace(",", "").strip()

        if metavar == "/":
            return option_name
        else:
            return metavar

    def _extract_default(self, help_txt: str) -> str:

        default = self.defaults_regex.findall(help_txt)
        default = default[0] if default else None
        if default:
            return (
                self.defaults_regex.sub("", help_txt).rstrip()
                + rf"  [default]\[default: {default}][/]"
            )
        else:
            return help_txt

    def _write_definition(self, option_name: str) -> str:
        metavar = self._extract_metavar_choices(option_name)

        color = (
            self.styles["metavar"]
            if self.styles["metavar"] != "none"
            else self.styles["option"]
        )

        if not metavar == option_name:
            if "[" in metavar and "]" in metavar:
                choices = metavar.split("[")[1].split("]")[0].split("|")
                colorized_metavar = "[{}]".format(
                    "|".join(
                        [_colorize(self.console, choice, color) for choice in choices]
                    )
                )
            else:
                colorized_metavar = _colorize(self.console, metavar, color)

            term = option_name.replace(metavar, "")
            return (
                _colorize(self.console, term, self._pick_color(term))
                + colorized_metavar
            )

        elif "/" in option_name:
            return " / ".join(
                [
                    _colorize(self.console, flag.strip(), self._pick_color(option_name))
                    for flag in option_name.split("/")
                ]
            )
        else:

            return _colorize(self.console, option_name, self._pick_color(option_name))

    def _write_option_help(self, help_txt: str) -> str:
        return _colorize(self.console, self._extract_default(help_txt), "doc_style")

    def write_usage(self, prog: str, args: str = "", prefix: str = None) -> None:
        # TODO: make usage text a style
        if not prefix:
            prefix = "Usage"
        colorized_prefix = _colorize(self.console, prefix, style="header", suffix=": ")
        super(HelpStylesFormatter, self).write_usage(
            _colorize(self.console, prog, "bold"),
            _colorize(self.console, args, "bold"),
            prefix=colorized_prefix,
        )

    def write_heading(self, heading: str) -> None:
        colorized_heading = _colorize(self.console, heading, style="header")
        super(HelpStylesFormatter, self).write_heading(colorized_heading)

    def write_dl(
        self, rows: Sequence[Tuple[str, str]], col_max: int = 30, col_spacing: int = 2
    ) -> None:
        colorized_rows: Sequence[Tuple[str, str]] = [
            (self._write_definition(row[0]), self._write_option_help(row[1]))
            for row in rows
        ]
        super(HelpStylesFormatter, self).write_dl(colorized_rows, col_max, col_spacing)

    def write_text(self, text: str) -> None:

        indent = " " * self.current_indent
        self.write(
            _colorize(
                self.console,
                wrap_text(
                    text,
                    self.width,
                    initial_indent=indent,
                    subsequent_indent=indent,
                    preserve_paragraphs=True,
                ),
                style="doc_style",
            )
        )
        self.write("\n")


class StyledGroup(click.Group):
    def __init__(
        self,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.styles = styles
        self.theme = theme
        self.option_custom_styles = option_custom_styles
        super(StyledGroup, self).__init__(*args, **kwargs)

    @classmethod
    def from_group(cls, group: click.Group) -> "StyledGroup":
        styled_group = cls()

        for key, value in group.__dict__.items():
            styled_group.__dict__[key] = value
        return styled_group

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            styles=self.styles,
            theme=self.theme,
            option_custom_styles=self.option_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]:
        kwargs.setdefault("cls", StyledCommand)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        kwargs.setdefault("option_custom_styles", self.option_custom_styles)
        return super(StyledGroup, self).command(
            group_styles=self.styles, *args, **kwargs
        )

    def group(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Group]:
        kwargs.setdefault("cls", StyledGroup)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        kwargs.setdefault("option_custom_styles", self.option_custom_styles)
        return super(StyledGroup, self).group(*args, **kwargs)


class StyledCommand(click.Command):
    def __init__(
        self,
        group_styles: Dict[str, Union[str, Style]] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):

        self.styles = {
            **(group_styles if group_styles else {}),
            **(styles if styles else {}),
        }
        self.theme = theme
        self.option_custom_styles = option_custom_styles
        super(StyledCommand, self).__init__(*args, **kwargs)

    @classmethod
    def from_command(cls, command: click.Command) -> "StyledCommand":
        styled_command = cls()
        for key, value in command.__dict__.items():
            styled_command.__dict__[key] = value
        return styled_command

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            # width=100,
            # width=15,
            # width=ctx.terminal_width,
            # max_width=15,
            # max_width=ctx.max_content_width,
            styles=self.styles,
            theme=self.theme,
            option_custom_styles=self.option_custom_styles,
        )
        # print(ctx.terminal_width)
        # print(ctx.max_content_width)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")


class StyledMultiCommand(click.MultiCommand):
    def __init__(
        self,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.styles = styles
        self.theme = theme
        self.option_custom_styles = option_custom_styles
        super(StyledMultiCommand, self).__init__(*args, **kwargs)

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            styles=self.styles,
            theme=self.theme,
            option_custom_styles=self.option_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def resolve_command(
        self, ctx: click.Context, args: List[str]
    ) -> Tuple[Optional[str], Optional[click.Command], List[str]]:

        cmd_name, cmd, args[1:] = super(StyledMultiCommand, self).resolve_command(
            ctx, args
        )

        if isinstance(cmd, click.Group):
            cmd = StyledGroup.from_group(cmd)
        elif isinstance(cmd, click.Command):
            cmd = StyledCommand.from_command(cmd)

        if cmd:
            if not getattr(cmd, "styles", None):
                cmd.styles = self.styles
            if not getattr(cmd, "theme", None):
                cmd.theme = self.theme
            if not getattr(cmd, "option_custom_styles", None):
                cmd.option_custom_styles = self.option_custom_styles

        return cmd_name, cmd, args[1:]
