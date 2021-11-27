import click

from click_rich_help import StyledGroup


def test_basic_group(runner):
    @click.command(
        cls=StyledGroup, headers_style="yellow", options_style="green", doc_style="red"
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
        "  \x1b[32m--name \x1b[0m\x1b[32mTEXT\x1b[0m  \x1b[31mThe person to greet.\x1b[0m",
        "  \x1b[32m--help\x1b[0m       \x1b[31mShow this message and exit.\x1b[0m",
    ]
