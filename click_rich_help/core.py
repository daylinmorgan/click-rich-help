import re

import click

from .utils import _apply_rich, _colorize, _extend_instance


class HelpColorsFormatter(click.HelpFormatter):
    options_regex = re.compile(r"-{1,2}[\w\-]+")

    def __init__(
        self,
        headers_style=None,
        options_style=None,
        metavar_style=None,
        options_custom_styles=None,
        *args,
        **kwargs
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.options_custom_styles = options_custom_styles
        super(HelpColorsFormatter, self).__init__(*args, **kwargs)

    def _get_opt_names(self, option_name):
        opts = self.options_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name):
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if self.options_custom_styles and (
                opt in self.options_custom_styles.keys()
            ):
                return self.options_custom_styles[opt]
        return self.options_style

    def _extract_metavar_choices(self, option_name):
        metavar = self.options_regex.sub("", option_name).replace(",", "").strip()

        if metavar == "/":
            return option_name
        else:
            return metavar

    def _write_definition(self, option_name):
        metavar = self._extract_metavar_choices(option_name)
        if not metavar == option_name:
            if "[" in metavar and "]" in metavar:
                choices = metavar.split("[")[1].split("]")[0].split("|")
                colorized_metavar = "[{}]".format(
                    "|".join(
                        [
                            _colorize(
                                choice, (self.metavar_style or self.options_style)
                            )
                            for choice in choices
                        ]
                    )
                )
            else:
                colorized_metavar = _colorize(
                    metavar, (self.metavar_style or self.options_style)
                )

            term = option_name.replace(metavar, "")
            return _colorize(term, self._pick_color(term)) + colorized_metavar

        elif "/" in option_name:
            return " / ".join(
                [
                    _colorize(flag.strip(), self._pick_color(option_name))
                    for flag in option_name.split("/")
                ]
            )
        else:

            return _colorize(option_name, self._pick_color(option_name))

    def write_usage(self, prog, args="", prefix="Usage"):
        colorized_prefix = _colorize(prefix, style=self.headers_style, suffix=": ")
        super(HelpColorsFormatter, self).write_usage(
            prog, args, prefix=colorized_prefix
        )

    def write_heading(self, heading):
        colorized_heading = _colorize(heading, style=self.headers_style)
        super(HelpColorsFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [
            (self._write_definition(row[0]), _apply_rich(row[1])) for row in rows
        ]
        super(HelpColorsFormatter, self).write_dl(colorized_rows, **kwargs)

    def write_text(self, text):

        colorized_text = _apply_rich(text)
        super(HelpColorsFormatter, self).write_text(colorized_text)


class HelpColorsMixin(object):
    def __init__(
        self,
        help_headers_style=None,
        help_options_style=None,
        help_metavar_style=None,
        help_options_custom_styles=None,
        *args,
        **kwargs
    ):
        self.help_headers_style = help_headers_style
        self.help_options_style = help_options_style
        self.help_metavar_style = help_metavar_style
        self.help_options_custom_styles = help_options_custom_styles
        super(HelpColorsMixin, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        formatter = HelpColorsFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_style=self.help_headers_style,
            options_style=self.help_options_style,
            metavar_style=self.help_metavar_style,
            options_custom_styles=self.help_options_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")


class HelpColorsGroup(HelpColorsMixin, click.Group):
    def __init__(self, *args, **kwargs):
        super(HelpColorsGroup, self).__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        kwargs.setdefault("cls", HelpColorsCommand)
        kwargs.setdefault("help_headers_style", self.help_headers_style)
        kwargs.setdefault("help_options_style", self.help_options_style)
        kwargs.setdefault("help_metavar_style", self.help_metavar_style)
        kwargs.setdefault("help_options_custom_styles", self.help_options_custom_styles)
        return super(HelpColorsGroup, self).command(*args, **kwargs)

    def group(self, *args, **kwargs):
        kwargs.setdefault("cls", HelpColorsGroup)
        kwargs.setdefault("help_headers_style", self.help_headers_style)
        kwargs.setdefault("help_options_style", self.help_options_style)
        kwargs.setdefault("help_metavar_style", self.help_metavar_style)
        kwargs.setdefault("help_options_custom_styles", self.help_options_custom_styles)
        return super(HelpColorsGroup, self).group(*args, **kwargs)


class HelpColorsCommand(HelpColorsMixin, click.Command):
    def __init__(self, *args, **kwargs):
        super(HelpColorsCommand, self).__init__(*args, **kwargs)


class HelpColorsMultiCommand(HelpColorsMixin, click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super(HelpColorsMultiCommand, self).__init__(*args, **kwargs)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args[1:] = super(HelpColorsMultiCommand, self).resolve_command(
            ctx, args
        )

        if not isinstance(cmd, HelpColorsMixin):
            if isinstance(cmd, click.Group):
                _extend_instance(cmd, HelpColorsGroup)
            if isinstance(cmd, click.Command):
                _extend_instance(cmd, HelpColorsCommand)

        if not getattr(cmd, "help_headers_style", None):
            cmd.help_headers_style = self.help_headers_style
        if not getattr(cmd, "help_options_style", None):
            cmd.help_options_style = self.help_options_style
        if not getattr(cmd, "help_metavar_style", None):
            cmd.help_metavar_style = self.help_metavar_style
        if not getattr(cmd, "help_options_custom_styles", None):
            cmd.help_options_custom_styles = self.help_options_custom_styles

        return cmd_name, cmd, args[1:]
