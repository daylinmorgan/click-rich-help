from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from click_rich_help import HelpStylesCommand, HelpStylesGroup

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def get_command_line_no():
    command, start, end = None, None, None
    blanks, cmd_lines = [], {}
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
            if end:
                cmd_lines[command] = (start, end)
                command, start, end = None, None, None
    cmd_lines["all"] = None

    return cmd_lines


console = Console()


def print_syntax(
    command,
    line_range=None,
    background_color=None,
    code_width=90,
    expand=False,
    theme="monokai",
):
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
    cls=HelpStylesGroup,
    headers_style="yellow bold",
    options_style="cyan italic",
    metavar_style="red bold",
    context_settings=CONTEXT_SETTINGS,
)
def cli():
    """[underline]Click-rich-help example[/]

    Welcome to click-rich-help, where we can
    leverage the great python app rich
    so we can improve the readability
    and usability of click-powered CLI's.

    Why?
    So we can make text [red]red[/], [yellow]yellow[/], or [green]green[/].

    Or maybe we want to [b]bold[/],[i]italic[/],[underline]underline[/],
    or [strike]strikethrough[/] our text?

    Let's do all of the above!

    [b i underline strike green]ALL[/]

    Checkout more examples, start with
    [yellow]python -m click_rich_help.examples cmd1 -h[/].

    Then test it for yourself!
    """
    pass


@cli.command()
@click.option("--count", default=1, help="some number")
@click.option("--pretty", help="[red][underline]underlined[/] red text", is_flag=True)
def cmd1(count, pretty):
    """[red bold]Command 1...try me[/]

    Look at that red text. CRAZY!
    Try [cyan]python -m click_rich_help.example cmd2[/cyan]!
    You won't believe what you see.
    """
    console.print("Try again with -h")


@cli.command(cls=HelpStylesCommand, options_style="green")
@click.option("--name", help="some string")
@click.option("--choices", help="make a choice", type=click.Choice(["yay", "nay"]))
@click.option("--shout/--no-shout", help="shout or don't")
def cmd2(name, choices, shout):
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
    cls=HelpStylesCommand,
    metavar_style="strike yellow",
    options_custom_styles={"--string": "bold red", "--style": "u green"},
)
@click.option("--string", help="markup string to test with rich (use quotes!)")
@click.option("--style", help="color/style to test")
def test(string, style):
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


@cli.command()
@click.argument("command")
@click.option(
    "--theme", help="pygments theme", default="monokai", metavar="<theme name>"
)
def src(command, theme):
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
