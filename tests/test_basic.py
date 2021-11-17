import click

from click_rich_help import HelpColorsException, HelpColorsGroup


def test_basic_group(runner):
    @click.command(
        cls=HelpColorsGroup, help_headers_style="yellow", help_options_style="green"
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
        "  \x1b[32m--name TEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_basic_command(runner):
    @click.group(
        cls=HelpColorsGroup, help_headers_style="yellow", help_options_style="green"
    )
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
        "  \x1b[32m--name TEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_unknown_color(runner):
    @click.command(cls=HelpColorsGroup, help_headers_style="unknwnstyle")
    @click.option("--name", help="The person to greet.")
    def cli(count):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert result.exception
    assert isinstance(result.exception, HelpColorsException)
    assert str(result.exception) == "Unknown style unknwnstyle"


def test_env_no_color(runner):
    @click.command(
        cls=HelpColorsGroup, help_headers_style="yellow", help_options_style="green"
    )
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


def test_metavar_basic(runner):
    @click.command(
        cls=HelpColorsGroup,
        help_headers_style="yellow",
        help_options_style="green",
        help_metavar_style="red",
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
        cls=HelpColorsGroup,
        help_headers_style="yellow",
        help_options_style="green",
        help_metavar_style="red",
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
