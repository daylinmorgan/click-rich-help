import re
from gettext import gettext as _
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union, overload

import click
from click.formatting import wrap_text
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

from .utils import _colorize

CLICK_STYLES = ["header", "option", "metavar", "doc_style", "default"]

THEMES = {
    "default": Theme(
        {
            "header": "bold italic cyan",
            "option": "bold yellow",
            "metavar": "green",
            "default": "dim",
            "required": "dim red",
        },
        inherit=False,
    )
}


class HelpStylesFormatter(click.HelpFormatter):
    option_regex = re.compile(r"-{1,2}[\w\-]+")
    defaults_regex = re.compile(r"  \[default: (.*)\]")
    required_regex = re.compile(r"  \[required\]")

    def __init__(
        self,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        option_custom_styles: Dict[str, str] = None,
        use_theme: str = None,
        *args: Any,
        **kwargs: Any,
    ):
        base_theme: Optional[Theme]

        if not any([styles, theme]):
            theme = THEMES["default"]
        if use_theme:
            try:
                base_theme = THEMES[use_theme]
            except KeyError:
                raise click.BadParameter(f"{use_theme} isn't one of {THEMES.keys()}")
        else:
            base_theme = None

        self.styles = self._get_styles(styles, theme, base_theme=base_theme)
        self.option_custom_styles = option_custom_styles
        self.console = self._load_console()
        super(HelpStylesFormatter, self).__init__(*args, **kwargs)

    def _get_styles(
        self,
        user_styles: Optional[Dict[str, Union[str, Style]]],
        theme: Optional[Theme],
        base_theme: Optional[Theme],
    ) -> Dict[str, Union[str, Style]]:

        styles: Dict[str, Union[str, Style]] = {k: "none" for k in CLICK_STYLES}
        additions: Dict[str, Union[str, Style]] = {}
        if base_theme:
            additions.update(base_theme.styles)
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

    def _extract_extras(self, help_txt: str) -> str:
        extras = []
        text = help_txt

        default = self.defaults_regex.findall(help_txt)
        default = default[0] if default else None

        if default:
            extras.append(rf"[default]\[default: {default}][/]")
            text = self.defaults_regex.sub("", text).rstrip()

        required = self.required_regex.findall(help_txt)
        required = required[0] if required else None

        if required:
            extras.append(r"[required]\[required][/]")
            text = self.required_regex.sub("", text).rstrip()

        return f"{text} {' '.join(extras)}"

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
        return _colorize(self.console, self._extract_extras(help_txt), "doc_style")

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
        use_theme: str = None,
        command_groups: Dict[str, str] = None,
        option_groups: Dict[str, str] = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.styles = styles
        self.theme = theme
        self.use_theme = use_theme
        self.command_groups = command_groups
        self.option_groups = option_groups
        self.option_custom_styles = option_custom_styles
        super(StyledGroup, self).__init__(*args, **kwargs)

    @classmethod
    def from_group(cls, group: click.Group) -> "StyledGroup":
        styled_group = cls()

        for key, value in group.__dict__.items():
            styled_group.__dict__[key] = value
        return styled_group

    def get_help(self, ctx: click.Context) -> str:

        # override click's default max width of 80
        if ctx.max_content_width is None:
            max_width = 100
        else:
            max_width = ctx.max_content_width

        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=max_width,
            styles=self.styles,
            theme=self.theme,
            use_theme=self.use_theme,
            option_custom_styles=self.option_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def _write_command_groups(
        self, cmds: List[Tuple[str, str]], formatter: click.HelpFormatter
    ) -> List[Tuple[str, str]]:

        grouped_cmds: List[Tuple[str, str]] = []
        if self.command_groups:
            for group, commands in self.command_groups.items():
                write_cmds: List[Tuple[str, str]] = []
                if not isinstance(commands, list):
                    raise ValueError(
                        f"Expected list of commands, group: {group}, commands: {commands}"
                    )
                for command in commands:
                    try:
                        cmd = [cmd for cmd in cmds if command in cmd[0]][0]
                    except IndexError:
                        raise ValueError(
                            f"Unable to find command '{command}' in list of commands"
                        )
                    write_cmds.append(cmd)
                grouped_cmds.extend(write_cmds)
                with formatter.section(_(group)):
                    formatter.write_dl(write_cmds)

        return grouped_cmds

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            grouped_cmds = self._write_command_groups(rows, formatter)

            rows = (
                [row for row in rows if row not in grouped_cmds]
                if grouped_cmds
                else rows
            )
            if rows:
                with formatter.section(_("Commands")):
                    formatter.write_dl(rows)

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command:
        ...

    @overload
    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]:
        ...

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Union[Callable[[Callable[..., Any]], click.Command], click.Command]:
        kwargs.setdefault("cls", StyledCommand)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        kwargs.setdefault("use_theme", self.use_theme)
        kwargs.setdefault("option_custom_styles", self.option_custom_styles)
        return super(StyledGroup, self).command(
            group_styles=self.styles, *args, **kwargs
        )

    @overload
    def group(self, __func: Callable[..., Any]) -> click.Group:
        ...

    @overload
    def group(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Group]:
        ...

    def group(
        self, *args: Any, **kwargs: Any
    ) -> Union[Callable[[Callable[..., Any]], click.Group], click.Group]:
        kwargs.setdefault("cls", StyledGroup)
        kwargs.setdefault("styles", self.styles)
        kwargs.setdefault("theme", self.theme)
        kwargs.setdefault("use_theme", self.use_theme)
        kwargs.setdefault("option_custom_styles", self.option_custom_styles)
        return super(StyledGroup, self).group(*args, **kwargs)


class StyledCommand(click.Command):
    def __init__(
        self,
        group_styles: Dict[str, Union[str, Style]] = None,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        use_theme: str = None,
        option_groups: Dict[str, str] = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):

        self.styles = {
            **(group_styles if group_styles else {}),
            **(styles if styles else {}),
        }
        self.theme = theme
        self.use_theme = use_theme
        self.option_groups = option_groups
        self.option_custom_styles = option_custom_styles
        super(StyledCommand, self).__init__(*args, **kwargs)

    @classmethod
    def from_command(cls, command: click.Command) -> "StyledCommand":
        styled_command = cls()
        for key, value in command.__dict__.items():
            styled_command.__dict__[key] = value
        return styled_command

    def get_help(self, ctx: click.Context) -> str:

        # override click's default max width of 80
        if ctx.max_content_width is None:
            max_width = 100
        else:
            max_width = ctx.max_content_width

        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=max_width,
            styles=self.styles,
            theme=self.theme,
            use_theme=self.use_theme,
            option_custom_styles=self.option_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def _write_option_groups(
        self, opts: List[Tuple[str, str]], formatter: click.HelpFormatter
    ) -> Union[List[Tuple[str, str]], None]:
        grouped_opt: List[Tuple[str, str]] = []

        if self.option_groups:
            for group, params in self.option_groups.items():
                write_params: List[Tuple[str, str]] = []

                for param in params:
                    try:
                        opt = [opt for opt in opts if param in opt[0]][0]
                    except IndexError:
                        raise ValueError(
                            f"Unable to find option '{param}' in list of options"
                        )
                    write_params.append(opt)

                grouped_opt.extend(write_params)

                with formatter.section(_(group)):
                    formatter.write_dl(write_params)

        return grouped_opt

    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []

        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        grouped_opt = self._write_option_groups(opts, formatter)

        opts = [opt for opt in opts if opt not in grouped_opt] if grouped_opt else opts

        if opts:
            with formatter.section(_("Options")):
                formatter.write_dl(opts)


class StyledMultiCommand(click.MultiCommand):
    def __init__(
        self,
        styles: Dict[str, Union[str, Style]] = None,
        theme: Theme = None,
        use_theme: str = None,
        option_custom_styles: Dict[str, str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.styles = styles
        self.theme = theme
        self.use_theme = use_theme
        self.option_custom_styles = option_custom_styles
        super(StyledMultiCommand, self).__init__(*args, **kwargs)

    def get_help(self, ctx: click.Context) -> str:

        # override click's default max width of 80
        if ctx.max_content_width is None:
            max_width = 100
        else:
            max_width = ctx.max_content_width

        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=max_width,
            styles=self.styles,
            theme=self.theme,
            use_theme=self.use_theme,
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
            if not getattr(cmd, "use_theme", None):
                cmd.use_theme = self.use_theme
            if not getattr(cmd, "option_custom_styles", None):
                cmd.option_custom_styles = self.option_custom_styles

        return cmd_name, cmd, args[1:]
