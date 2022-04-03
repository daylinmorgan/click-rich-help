import sys

import click

from click_rich_help import StyledCommand


@click.command(cls=StyledCommand, styles={"header": "bold red underline reverse"})
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")


@click.command(
    cls=StyledCommand,
    styles={"header": "bold red underline reverse"},
    use_theme="default",
)
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello_inherit(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    if sys.argv[1] == "inherit":
        hello_inherit()
    else:
        hello()
