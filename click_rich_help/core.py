import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import click
from click.formatting import wrap_text
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from .utils import _colorize


class HelpStylesFormatter(click.HelpFormatter):
    options_regex = re.compile(r"-{1,2}[\w\-]+")

    def __init__(
        self,
        headers_style: str = None,
        options_style: str = None,
        metavar_style: str = None,
        doc_style: str = None,
        options_custom_styles: Dict[str, str] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.doc_style = doc_style
        self.options_custom_styles = options_custom_styles
        self.styles = self._get_styles(styles, theme)
        self.console = self._load_console()
        super(HelpStylesFormatter, self).__init__(*args, **kwargs)

    def _get_styles(
        self,
        user_styles: Optional[Dict[str, Union[str, Style]]],
        theme: Optional[Theme],
    ) -> Dict[str, Union[str, Style]]:

        styles: Dict[str, Union[str, Style]] = {
            k: "none" for k in ["headers", "options", "metavar", "doc_style"]
        }
        additions: Dict[str, Union[str, Style]] = {
            k: v
            for k, v in {
                **{
                    "headers": self.headers_style,
                    "options": self.options_style,
                    "metavar": self.metavar_style,
                    "doc_style": self.doc_style,
                },
            }.items()
            if v
        }
        if user_styles:
            if isinstance(user_styles, dict):
                additions.update(user_styles)
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
        opts = self.options_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name: str) -> Union[str, Style]:
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if self.options_custom_styles and (
                opt in self.options_custom_styles.keys()
            ):
                return self.options_custom_styles[opt]
        return self.styles["options"]

    def _extract_metavar_choices(self, option_name: str) -> str:
        metavar = self.options_regex.sub("", option_name).replace(",", "").strip()

        if metavar == "/":
            return option_name
        else:
            return metavar

    def _write_definition(self, option_name: str) -> str:
        metavar = self._extract_metavar_choices(option_name)

        color = (
            self.styles["metavar"]
            if self.styles["metavar"] != "none"
            else self.styles["options"]
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

    def write_usage(self, prog: str, args: str = "", prefix: str = None) -> None:
        if not prefix:
            prefix = "Usage"
        colorized_prefix = _colorize(self.console, prefix, style="headers", suffix=": ")
        super(HelpStylesFormatter, self).write_usage(
            prog, args, prefix=colorized_prefix
        )

    def write_heading(self, heading: str) -> None:
        colorized_heading = _colorize(self.console, heading, style="headers")
        super(HelpStylesFormatter, self).write_heading(colorized_heading)

    def write_dl(
        self, rows: Sequence[Tuple[str, str]], col_max: int = 30, col_spacing: int = 2
    ) -> None:
        colorized_rows: Sequence[Tuple[str, str]] = [
            (
                self._write_definition(row[0]),
                _colorize(self.console, row[1], "doc_style"),
            )
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
        headers_style: str = None,
        options_style: str = None,
        metavar_style: str = None,
        doc_style: str = None,
        options_custom_styles: Dict[str, str] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.doc_style = doc_style
        self.options_custom_styles = options_custom_styles
        self.styles = styles
        self.theme = theme
        super(StyledGroup, self).__init__(*args, **kwargs)

    @classmethod
    def from_group(cls, group: click.Group) -> "StyledGroup":
        styled_group = cls()

        for key, value in group.__dict__.items():
            styled_group.__dict__[key] = value
        return styled_group

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_style=self.headers_style,
            options_style=self.options_style,
            metavar_style=self.metavar_style,
            doc_style=self.doc_style,
            options_custom_styles=self.options_custom_styles,
            styles=self.styles,
            theme=self.theme,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]:
        kwargs.setdefault("cls", StyledCommand)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("doc_style", self.doc_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        return super(StyledGroup, self).command(*args, **kwargs)

    def group(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Group]:
        kwargs.setdefault("cls", StyledGroup)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("doc_style", self.doc_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        return super(StyledGroup, self).group(*args, **kwargs)


class StyledCommand(click.Command):
    def __init__(
        self,
        headers_style: str = None,
        options_style: str = None,
        metavar_style: str = None,
        doc_style: str = None,
        options_custom_styles: Dict[str, str] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.doc_style = doc_style
        self.options_custom_styles = options_custom_styles
        self.styles = styles
        self.theme = theme
        super(StyledCommand, self).__init__(*args, **kwargs)

    @classmethod
    def from_command(cls, command: click.Command) -> "StyledCommand":
        styled_command = cls()
        for key, value in command.__dict__.items():
            styled_command.__dict__[key] = value
        return styled_command

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_style=self.headers_style,
            options_style=self.options_style,
            metavar_style=self.metavar_style,
            doc_style=self.doc_style,
            options_custom_styles=self.options_custom_styles,
            styles=self.styles,
            theme=self.theme,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")


class StyledMultiCommand(click.MultiCommand):
    def __init__(
        self,
        headers_style: str = None,
        options_style: str = None,
        metavar_style: str = None,
        doc_style: str = None,
        options_custom_styles: Dict[str, str] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.doc_style = doc_style
        self.options_custom_styles = options_custom_styles
        self.styles = styles
        self.theme = theme
        super(StyledMultiCommand, self).__init__(*args, **kwargs)

    def get_help(self, ctx: click.Context) -> str:
        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_style=self.headers_style,
            options_style=self.options_style,
            metavar_style=self.metavar_style,
            doc_style=self.doc_style,
            options_custom_styles=self.options_custom_styles,
            styles=self.styles,
            theme=self.theme,
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
            if not getattr(cmd, "headers_style", None):
                cmd.headers_style = self.headers_style
            if not getattr(cmd, "options_style", None):
                cmd.options_style = self.options_style
            if not getattr(cmd, "metavar_style", None):
                cmd.metavar_style = self.metavar_style
            if not getattr(cmd, "doc_style", None):
                cmd.doc_style = self.doc_style
            if not getattr(cmd, "options_custom_styles", None):
                cmd.options_custom_styles = self.options_custom_styles
            if not getattr(cmd, "styles", None):
                cmd.styles = self.styles
            if not getattr(cmd, "theme", None):
                cmd.theme = self.theme

        return cmd_name, cmd, args[1:]
