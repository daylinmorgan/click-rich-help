import click

from click_rich_help import HelpStylesCommand


@click.command(
    cls=HelpStylesCommand, options_style="italic cyan", headers_style="bold yellow"
)
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()
