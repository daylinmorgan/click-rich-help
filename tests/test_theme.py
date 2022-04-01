import click
from rich.theme import Theme

import click_rich_help.core
from click_rich_help import StyledGroup

# set a "default" theme for testing
click_rich_help.core.THEMES = {
    "default": Theme(
        {
            "header": "bold italic cyan",
            "option": "bold yellow",
            "metavar": "green",
            "default": "dim",
            "required": "dim red",
        },
        inherit=False,
    )
}


def test_defaults(runner):
    @click.group(
        cls=StyledGroup,
    )
    def cli():
        pass

    @cli.command()
    @click.option("--name", help="name to print", required=True)
    @click.option("--count", help="times to print name", default=5, show_default=True)
    def command1(name):
        pass

    @cli.command()
    def command2(name):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[1;3;36mUsage\x1b[0m: \x1b[1mcli\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[1;3;36mOptions\x1b[0m:",
        "  \x1b[1;33m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[1;3;36mCommands\x1b[0m:",
        "  \x1b[1;33mcommand1\x1b[0m  ",
        "  \x1b[1;33mcommand2\x1b[0m  ",
    ]

    result = runner.invoke(cli, ["command1", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[1;3;36mUsage\x1b[0m: \x1b[1mcli command1\x1b[0m \x1b[1m[OPTIONS]\x1b[0m",
        "",
        "\x1b[1;3;36mOptions\x1b[0m:",
        "  \x1b[1;33m--name \x1b[0m\x1b[32mTEXT\x1b[0m      name to print \x1b[2;31m[required]\x1b[0m",
        "  \x1b[1;33m--count \x1b[0m\x1b[32mINTEGER\x1b[0m  times to print name \x1b[2m[default: 5]\x1b[0m",
        "  \x1b[1;33m--help\x1b[0m           Show this message and exit.",
    ]


def test_defaults_inherit(runner):
    @click.group(cls=StyledGroup, styles={"header": "blue"}, use_theme="default")
    def cli():
        pass

    @cli.command(styles={"option": "red"})
    @click.option("--name", help="name to print", required=True)
    @click.option("--count", help="times to print name", default=5, show_default=True)
    def command1(name):
        pass

    @cli.command()
    def command2(name):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[34mUsage\x1b[0m: \x1b[1mcli\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[34mOptions\x1b[0m:",
        "  \x1b[1;33m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[34mCommands\x1b[0m:",
        "  \x1b[1;33mcommand1\x1b[0m  ",
        "  \x1b[1;33mcommand2\x1b[0m  ",
    ]

    result = runner.invoke(cli, ["command1", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[34mUsage\x1b[0m: \x1b[1mcli command1\x1b[0m \x1b[1m[OPTIONS]\x1b[0m",
        "",
        "\x1b[34mOptions\x1b[0m:",
        "  \x1b[31m--name \x1b[0m\x1b[32mTEXT\x1b[0m      name to print \x1b[2;31m[required]\x1b[0m",
        "  \x1b[31m--count \x1b[0m\x1b[32mINTEGER\x1b[0m  times to print name \x1b[2m[default: 5]\x1b[0m",
        "  \x1b[31m--help\x1b[0m           Show this message and exit.",
    ]


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
        "\x1b[31mUsage\x1b[0m: \x1b[1mcli\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[31mOptions\x1b[0m:",
        "  \x1b[32m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[31mCommands\x1b[0m:",
        "  \x1b[1;3;34mcommand1\x1b[0m  ",
        "  \x1b[32mcommand2\x1b[0m  ",
    ]
