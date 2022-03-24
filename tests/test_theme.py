import click
import pytest

from click_rich_help import StyledCommand, StyledGroup
from rich.theme import Theme


def test_styles(runner):
    @click.group(cls=StyledGroup, headers_style="yellow", options_style="green")
    def cli():
        pass

    @cli.command(cls=StyledCommand, styles={"headers": "red", "options": "blue"})
    @click.option("--name", help="The person to greet.")
    def command(name):
        pass

    result = runner.invoke(cli, ["command", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[31mUsage\x1b[0m: cli command [OPTIONS]",
        "",
        "\x1b[31mOptions\x1b[0m:",
        "  \x1b[34m--name \x1b[0m\x1b[34mTEXT\x1b[0m  The person to greet.",
        "  \x1b[34m--help\x1b[0m       Show this message and exit.",
    ]


def test_theme(runner):
    @click.group(
        cls=StyledGroup,
        headers_style="red",
        options_style="green",
        options_custom_styles={"command1": "red"},
        styles={'headers':'bold'},
        theme=Theme({"headers": "yellow"}),
    )
    def cli():
        pass

    @cli.command()
    def command1(name):
        pass

    @cli.command()
    def command2(name):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[33mCommands\x1b[0m:",
        "  \x1b[31mcommand1\x1b[0m",
        "  \x1b[32mcommand2\x1b[0m",
    ]
