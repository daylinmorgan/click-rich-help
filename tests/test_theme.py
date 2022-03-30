import click
from rich.theme import Theme

from click_rich_help import StyledGroup


def test_theme(runner):
    @click.group(
        cls=StyledGroup,
        styles={"header": "red", "option": "green"},
        option_custom_styles={"command1": "bold italic blue"},
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
        "\x1b[31mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "\x1b[31mOptions\x1b[0m:",
        "  \x1b[32m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[31mCommands\x1b[0m:",
        "  \x1b[1;3;34mcommand1\x1b[0m",
        "  \x1b[32mcommand2\x1b[0m",
    ]
