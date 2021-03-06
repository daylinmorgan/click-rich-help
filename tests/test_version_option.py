import click

from click_rich_help import version_option


def test_message_color(runner):
    @click.group()
    @version_option(version="1.0", prog_name="example", message_style="green")
    def cli():
        pass

    result = runner.invoke(cli, ["--version"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[32mexample\x1b[0m\x1b[32m, version \x1b[0m\x1b[32m1.0\x1b[0m"
    ]


def test_version_and_prog_name_color(runner):
    @click.group()
    @version_option(
        version="1.0",
        prog_name="example",
        version_style="green",
        prog_name_style="yellow",
    )
    def cli():
        pass

    result = runner.invoke(cli, ["--version"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mexample\x1b[0m, version \x1b[32m1.0\x1b[0m"
    ]


def test_custom_message(runner):
    @click.group()
    @version_option(
        version="1.0",
        prog_name="example",
        version_style="green",
        prog_name_style="white",
        message="%(prog)s %(version)s\n   python=3.7",
        message_style="bright_black",
    )
    def cli():
        pass

    result = runner.invoke(cli, ["--version"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[37mexample\x1b[0m\x1b[90m \x1b[0m\x1b[32m1.0\x1b[0m",
        "\x1b[90m   python=3.7\x1b[0m",
    ]
