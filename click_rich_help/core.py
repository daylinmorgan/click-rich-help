import re

import click

from .utils import _apply_rich, _colorize, _extend_instance


class HelpStylesFormatter(click.HelpFormatter):
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
        super(HelpStylesFormatter, self).__init__(*args, **kwargs)

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
        super(HelpStylesFormatter, self).write_usage(
            prog, args, prefix=colorized_prefix
        )

    def write_heading(self, heading):
        colorized_heading = _colorize(heading, style=self.headers_style)
        super(HelpStylesFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows, **kwargs):
        colorized_rows = [
            (self._write_definition(row[0]), _apply_rich(row[1])) for row in rows
        ]
        super(HelpStylesFormatter, self).write_dl(colorized_rows, **kwargs)

    def write_text(self, text):

        colorized_text = _apply_rich(text)
        super(HelpStylesFormatter, self).write_text(colorized_text)


class HelpStylesMixin(object):
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
        super(HelpStylesMixin, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        formatter = HelpStylesFormatter(
            width=ctx.terminal_width,
            max_width=ctx.max_content_width,
            headers_style=self.headers_style,
            options_style=self.options_style,
            metavar_style=self.metavar_style,
            options_custom_styles=self.options_custom_styles,
        )
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")


class HelpStylesGroup(HelpStylesMixin, click.Group):
    def __init__(self, *args, **kwargs):
        super(HelpStylesGroup, self).__init__(*args, **kwargs)

    def command(self, *args, **kwargs):
        kwargs.setdefault("cls", HelpStylesCommand)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        return super(HelpStylesGroup, self).command(*args, **kwargs)

    def group(self, *args, **kwargs):
        kwargs.setdefault("cls", HelpStylesGroup)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        return super(HelpStylesGroup, self).group(*args, **kwargs)


class HelpStylesCommand(HelpStylesMixin, click.Command):
    def __init__(self, *args, **kwargs):
        super(HelpStylesCommand, self).__init__(*args, **kwargs)


class HelpStylesMultiCommand(HelpStylesMixin, click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super(HelpStylesMultiCommand, self).__init__(*args, **kwargs)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args[1:] = super(HelpStylesMultiCommand, self).resolve_command(
            ctx, args
        )

        if not isinstance(cmd, HelpStylesMixin):
            if isinstance(cmd, click.Group):
                _extend_instance(cmd, HelpStylesGroup)
            if isinstance(cmd, click.Command):
                _extend_instance(cmd, HelpStylesCommand)

        if not getattr(cmd, "headers_style", None):
            cmd.headers_style = self.headers_style
        if not getattr(cmd, "options_style", None):
            cmd.options_style = self.options_style
        if not getattr(cmd, "metavar_style", None):
            cmd.metavar_style = self.metavar_style
        if not getattr(cmd, "options_custom_styles", None):
            cmd.options_custom_styles = self.options_custom_styles

        return cmd_name, cmd, args[1:]
