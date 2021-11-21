import re
import sys
import click
from typing import List,Tuple,Dict,Optional,Sequence, Any,Union,Callable
from .utils import _apply_rich, _colorize

from click.core import Group, Context


class HelpStylesFormatter(click.HelpFormatter):
    options_regex = re.compile(r"-{1,2}[\w\-]+")

    def __init__(
        self,
        headers_style: str = None,
        options_style: str = None,
        metavar_style: str = None,
        options_custom_styles: Dict[str,str] = None,
        *args: Any,
        **kwargs: Any
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.options_custom_styles = options_custom_styles
        super(HelpStylesFormatter, self).__init__(*args, **kwargs)

    def _get_opt_names(self, option_name: str)-> List[str]:
        opts = self.options_regex.findall(option_name)
        if not opts:
            return [option_name]
        else:
            # Include this for backwards compatibility
            opts.append(option_name.split()[0])
            return opts

    def _pick_color(self, option_name:str)-> Optional[str]:
        opts = self._get_opt_names(option_name)
        for opt in opts:
            if self.options_custom_styles and (
                opt in self.options_custom_styles.keys()
            ):
                return self.options_custom_styles[opt]
        return self.options_style

    def _extract_metavar_choices(self, option_name:str)-> str:
        metavar = self.options_regex.sub("", option_name).replace(",", "").strip()

        if metavar == "/":
            return option_name
        else:
            return metavar

    def _write_definition(self, option_name:str)-> str:
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

    def write_usage(self, prog:str, args:str="", prefix:str=None)-> None:
        if prefix==None: prefix="Usage"
        colorized_prefix = _colorize(prefix, style=self.headers_style, suffix=": ")
        super(HelpStylesFormatter, self).write_usage(
            prog, args, prefix=colorized_prefix
        )

    def write_heading(self, heading:str)-> None:
        colorized_heading = _colorize(heading, style=self.headers_style)
        super(HelpStylesFormatter, self).write_heading(colorized_heading)

    def write_dl(self, rows: Sequence[Tuple[str,str]],col_max: int = 30,col_spacing: int = 2) -> None:
        colorized_rows: Sequence[Tuple[str,str]] = [
            (self._write_definition(row[0]), _apply_rich(row[1])) for row in rows
        ]
        super(HelpStylesFormatter, self).write_dl(colorized_rows, col_max,col_spacing)

    def write_text(self, text:str)-> None:

        colorized_text = _apply_rich(text)
        super(HelpStylesFormatter, self).write_text(colorized_text)


class HelpStylesGroup(click.Group):
    def __init__(self,  
        headers_style:str=None,
        options_style:str=None,
        metavar_style:str=None,
        options_custom_styles:Dict[str,str]=None,
        *args: Any,
        **kwargs: Any
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.options_custom_styles = options_custom_styles
        super(HelpStylesGroup, self).__init__(*args, **kwargs)

    @classmethod
    def from_group(cls, group: click.Group) -> "HelpStylesGroup":
        styled_group = cls()
        
        for key,value in group.__dict__.items():
            styled_group.__dict__[key] = value
        return styled_group


    def get_help(self, ctx: click.Context) -> str:
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

    def command(self, *args:Any, **kwargs:Any)->Callable[[Callable[...,Any]],click.Command]:
        kwargs.setdefault("cls", HelpStylesCommand)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        return super(HelpStylesGroup, self).command(*args, **kwargs)

    def group(self, *args:Any, **kwargs:Any) -> Callable[[Callable[...,Any]],click.Group]:
        kwargs.setdefault("cls", HelpStylesGroup)
        kwargs.setdefault("headers_style", self.headers_style)
        kwargs.setdefault("options_style", self.options_style)
        kwargs.setdefault("metavar_style", self.metavar_style)
        kwargs.setdefault("options_custom_styles", self.options_custom_styles)
        return super(HelpStylesGroup, self).group(*args, **kwargs)


class HelpStylesCommand(click.Command):
    def __init__(self,  
        headers_style:str=None,
        options_style:str=None,
        metavar_style:str=None,
        options_custom_styles:Dict[str,str]=None,
        *args: Any,
        **kwargs: Any
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.options_custom_styles = options_custom_styles
        super(HelpStylesCommand, self).__init__(*args, **kwargs)

    @classmethod
    def from_command(cls,command:click.Command) -> "HelpStylesCommand":
        styled_command = cls()
        for key,value in command.__dict__.items():
            styled_command.__dict__[key] = value
        return styled_command
        
    def get_help(self, ctx: click.Context) -> str:
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



class HelpStylesMultiCommand(click.MultiCommand):
    def __init__(self,  
        headers_style:str=None,
        options_style:str=None,
        metavar_style:str=None,
        options_custom_styles:Dict[str,str]=None,
        *args: Any,
        **kwargs: Any
    ):
        self.headers_style = headers_style
        self.options_style = options_style
        self.metavar_style = metavar_style
        self.options_custom_styles = options_custom_styles
        super(HelpStylesMultiCommand, self).__init__(*args, **kwargs)
        
    def get_help(self, ctx:click.Context) -> str:
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


    def resolve_command(self, ctx:click.Context, args:List[str])-> Tuple[Optional[str],Optional[click.Command],List[str]]:

        cmd_name, cmd, args[1:] = super(HelpStylesMultiCommand, self).resolve_command(
            ctx, args
        )

        if isinstance(cmd, click.Group):
            cmd = HelpStylesGroup.from_group(cmd)
        elif isinstance(cmd, click.Command):
            cmd = HelpStylesCommand.from_command(cmd)

        if cmd:
            if not getattr(cmd, "headers_style", None):
                cmd.headers_style = self.headers_style
            if not getattr(cmd, "options_style", None):
                cmd.options_style = self.options_style
            if not getattr(cmd, "metavar_style", None):
                cmd.metavar_style = self.metavar_style
            if not getattr(cmd, "options_custom_styles", None):
                cmd.options_custom_styles = self.options_custom_styles

        return cmd_name, cmd, args[1:]
