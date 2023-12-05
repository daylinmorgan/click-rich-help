import sys

import click

from click_rich_help import StyledCommand

@click.group()
def cli():
    pass


@cli.command(cls=StyledCommand, styles={"header": "bold red underline"})
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")


@cli.command(
    cls=StyledCommand,
    styles={"header": "bold red underline"},
    use_theme="default",
)
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def inherit(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")

if __name__ == "__main__":
    cli()

# if __name__ == "__main__":
#     if sys.argv[1] == "inherit":
#         hello_inherit()
#     else:
#         hello()
