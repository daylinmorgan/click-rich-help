import click
from rich.errors import StyleSyntaxError

from click_rich_help import StyledCommand, StyledGroup


def test_basic_group(runner):
    @click.command(cls=StyledCommand, styles={"header":"yellow", "option":"green"})
    @click.option("--name", help="The person to greet.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli [OPTIONS]",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--name \x1b[0m\x1b[32mTEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_basic_command(runner):
    @click.group(cls=StyledGroup, styles={"header":"yellow", "option":"green"})
    def cli():
        pass

    @cli.command()
    @click.option("--name", help="The person to greet.")
    def command(name):
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
        "  \x1b[32mcommand\x1b[0m",
    ]

    result = runner.invoke(cli, ["command", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli command [OPTIONS]",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--name \x1b[0m\x1b[32mTEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_unknown_color(runner):
    @click.command(cls=StyledGroup, styles={'header':"unknownstyle"})
    @click.option("--name", help="The person to greet.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert result.exception
    # assert isinstance(result.exception, HelpStylesException)
    assert isinstance(result.exception, StyleSyntaxError)
    # assert str(result.exception) == "Unknown style unknwnstyle"
    assert (
        str(result.exception)
        == "unable to parse 'unknownstyle' as color; 'unknownstyle' is not a valid color"
    )


def test_env_no_color(runner):
    @click.command(cls=StyledGroup, styles={"header":"yellow", "option":"green"})
    @click.option("--name", help="The person to greet.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True, env={"NO_COLOR": "1"})
    assert not result.exception
    assert result.output.splitlines() == [
        "Usage: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "Options:",
        "  --name TEXT  The person to greet.",
        "  --help       Show this message and exit.",
    ]


def test_basic_metavar(runner):
    @click.command(
        cls=StyledGroup,
        styles={
        "header":"yellow",
        "option":"green",
        "metavar":"red",
        }
    )
    @click.option("--name", help="The person to greet.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--name \x1b[0m\x1b[31mTEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_custom_metavar(runner):
    @click.command(
        cls=StyledGroup,
        styles={
        "header":"yellow",
        "option":"green",
        "metavar":"red",
        }
    )
    @click.option("--first-name", help="The person's first name.", metavar="<name>")
    @click.option("--last-name", help="The person's last name.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--first-name \x1b[0m\x1b[31m<name>\x1b[0m  The person's first name.",
        "  \x1b[32m--last-name \x1b[0m\x1b[31mTEXT\x1b[0m     The person's last name.",
        "  \x1b[32m--help\x1b[0m               Show this message and exit.",
    ]


def test_custom_metavar_choice(runner):
    @click.command(
        cls=StyledGroup,
        styles={
        "header":"yellow",
        "option":"green",
        "metavar":"red",
        }
    )
    @click.option(
        "--name",
        help="either billy or bob",
        type=click.Choice(["Billy", "Bob"]),
    )
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: cli [OPTIONS] COMMAND [ARGS]...",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--name \x1b[0m[\x1b[31mBilly\x1b[0m|\x1b[31mBob\x1b[0m]  either billy or bob",
        "  \x1b[32m--help\x1b[0m              Show this message and exit.",
    ]
