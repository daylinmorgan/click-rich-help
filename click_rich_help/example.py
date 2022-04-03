from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.theme import Theme

from click_rich_help import StyledCommand, StyledGroup

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=90)


def get_command_line_no() -> Dict[Optional[str], Optional[Tuple[int, int]]]:
    """get line numbers of commands for use in 'src'"""
    command: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    blanks: List[int] = []
    cmd_lines: Dict[Optional[str], Optional[Tuple[int, int]]] = {}
    with Path(__file__).open("r") as f:
        for line_no, line in enumerate(f):
            if line == "\n":
                blanks.append(line_no)
            if not start:
                if line.startswith("@cli"):
                    start = line_no
            if start and not command:
                if line.startswith("def "):
                    command = line[4:].split("(", 1)[0]
            if start and command:
                if [line_no - 1, line_no] == blanks[-2:]:
                    end = line_no
            if start and end:
                cmd_lines[command] = (start, end)
                command, start, end = None, None, None

    cmd_lines["all"] = None

    return cmd_lines


console = Console()


def print_syntax(
    command: str,
    line_range: Tuple[int, int] = None,
    background_color: str = None,
    code_width: int = 90,
    expand: bool = False,
    theme: str = "monokai",
) -> None:
    console.print(
        Panel(
            Syntax.from_path(
                __file__,
                line_range=line_range,
                background_color=background_color,
                code_width=code_width,
                line_numbers=True,
                theme=theme,
            ),
            expand=False,
            title=f"Source code for {command}",
        )
    )


@click.group(
    cls=StyledGroup,
    use_theme="default",
    context_settings=CONTEXT_SETTINGS,
)
def cli() -> None:
    """[underline]Click-rich-help example[/]

    Welcome to [info]click-rich-help[/], where we can
    leverage the great python app rich
    so we can improve the readability
    and usability of click-powered CLI's.

    Why?
    So we can make text [red]red[/], [yellow]yellow[/], or [green]green[/].

    Or maybe we want to [b]bold[/], [i]italic[/], [underline]underline[/],
    or [strike]strikethrough[/] our text?

    Let's do all of the above!

    [b i strike green]ALL[/]

    Checkout more examples, start with
    [yellow]python -m click_rich_help.examples cmd1 -h[/].

    Then test it for yourself!
    """
    pass


@cli.command()
@click.option("--count", default=1, help="some number", show_default=True)
@click.option(
    "--pretty", help="[underline]underlined[/] [magenta]magenta text[/]", is_flag=True
)
@click.option("--name", help="a name to print", required=True)
def cmd1(count: int, pretty: bool, name: str) -> None:
    """Command 1...try me :+1:

    Below you can see the rest of the default styles.

    You can also set the color of default and required args:

    \b
    styles={
        "default":"[dim]dim[/]",
        "required":"[dim red]dim red[/]",
    }

    Try [cyan]python -m click_rich_help.example cmd2[/cyan]!
    You won't believe what you see.
    """
    console.print("Try again with -h")


@cli.command(styles={"option": "green"})
@click.option("--name", help="some string")
@click.option("--choices", help="make a choice", type=click.Choice(["yay", "nay"]))
@click.option("--shout/--no-shout", help="shout or don't")
def cmd2(name: str, choices: str, shout: bool) -> None:
    """A command of the second variety

    You should never do this in a help message but you [b i cyan]could[/]
    get wild and include emoji :wink:.

    Did you notice these options are green!

    Next try [yellow]python -m click_rich_help.example test[/]!

    \f
    secret text click doesn't want you to see
    """
    console.print("Try again with -h")


@cli.command(
    cls=StyledCommand,
    styles={"header": "bold blue underline", "option": "italic"},
    theme=Theme(
        {
            "headers": "yellow",
            "code": "cyan reverse",
            "info": "dim cyan",
            "warning": "magenta",
            "danger": "bold red",
        }
    ),
)
@click.option(
    "--option", help="[headers]header color[/],[code]code[/],[danger]DANGER[/]"
)
def theme(option: str) -> None:
    """Color commands and help strings with themes

    If you already make use of [code]rich.theme.Theme[/code]
    then it's simple to include additional styles.

    \b
    For instance:
    Theme({
        "headers": "yellow",
        "info": "dim cyan",
        "warning": "magenta",
        "danger": "bold red"
    })

    You can add styles for use in doc strings and help text.
    While also updating the styles used for headers, options, metavars, etc.

    [headers]Headers![/]
    [info]INFO[/]
    [warning]WARNING[/]
    [danger]DANGER[/]

    Use [yellow]python -m click_rich_help.example src theme[/] to view
    the [code]Theme[/code] style applied to this command.

    """
    console.print("Try again with -h")


@cli.command(
    styles={"metavar": "strike green"},
    option_custom_styles={"--string": "bold red", "--style": "reverse green"},
)
@click.option("--string", help="markup string to test with rich (use quotes!)")
@click.option("--style", help="color/style to test")
def test(string: str, style: str) -> None:
    """Test a markup string or color/style

    Use [yellow]python -m rich.color [/]for full list of options

    Or [yellow]python -m rich[/] for an idea of what you can do.

    [i]Note[/]: that support is terminal dependent, so use complex styles sparingly

    I made those metavars with a strikethrough...don't do that please.

    Also those options have custom colors..cool!
    """
    console.print("[b blue]Testing...")
    if not string and not style:
        console.print(
            "I want to help you test it but you need to give me a string or style to try."
        )
        console.print("\ncheck the help for more info")

    if string:
        console.print("[u]string:[/]")
        console.print(f">>> {string}")
    if style:
        console.print("[u]style:")
        console.print(">>>", end="")
        console.print("This is a text string for the style:", style=style, end="")
        console.print(f' "{style}" ')


@cli.command(
    cls=StyledCommand,
    styles={"header": "green", "doc_style": "green"},
)
@click.option("--name", help="some string")
def cmd3(name: str) -> None:
    """why is doc_style important?

    The main reason this parameter exists is to apply a default
    styling across both short and long form doc strings in your app.

    Importantly one can still colorize the docstring by using the
    [bold italic red]markup style of rich[/].
    """

    console.print("Try again with -h")


@cli.command(option_groups={"Group": ["--option-1", "--option-2"]})
@click.option("--option-1", help="first option")
@click.option("--option-2", help="second option")
@click.option("--name", help="some string")
def group(option_1: str, option_2: str, name: str) -> None:
    """Group commands and options

    Generate lists of option groups by passing a dictionary to your command decorator

    \b
    Example:
    [cyan]@click.command(
        cls=StyledCommand,
        option_groups={
            "Group":["--option-1","--option-2"]
        }
    )[/cyan]

    \b
    Or do the same with commands for a StyledGroup:
    Example:
    [cyan]@cli.group(
        cls=StyledGroup,
        command_groups={
            "general":["cmd1","cmd2"],
            "database":["load","save"]
        }
    )[/cyan]

    All remaining options will be appended in a separate "Options" or "Commands" group.
    """
    console.print("Try again with -h")


@cli.command()
@click.argument("command")
@click.option(
    "--theme",
    help="pygments theme",
    default="monokai",
    metavar="<theme name>",
    show_default=True,
)
def src(command: str, theme: str) -> None:
    """View the source code for a given [yellow]COMMAND[/]

    [i]HINTS[/]:

    - view the entire src code with "all"

    - view the main entrypoint with "cli"

    see [link]https://pygments.org/docs/styles/#getting-a-list-of-available-styles[/]
    for available styles to provide [yellow]--theme[/].
    """

    if command:
        cmd_lines = get_command_line_no()
        print_syntax(command, cmd_lines[command], theme=theme)


if __name__ == "__main__":
    cli()
