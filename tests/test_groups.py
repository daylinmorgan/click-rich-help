import click
from rich.errors import StyleSyntaxError

from click_rich_help import StyledCommand, StyledGroup


def test_command_group(runner):
    @click.group(cls=StyledGroup, command_groups={"main": ["cmd1", "cmd2"]})
    def cli():
        pass

    @cli.command(cls=StyledCommand, styles={"header": "yellow", "option": "green"})
    @click.option("--name", help="The person to greet.")
    def cmd1(count):
        pass

    @cli.command()
    def cmd2():
        pass

    @cli.command()
    def othercmd():
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[1;3;38;2;241;250;140mUsage\x1b[0m: \x1b[1mcli\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[1;3;38;2;241;250;140mOptions\x1b[0m:",
        "  \x1b[1;38;2;80;250;123m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[1;3;38;2;241;250;140mmain\x1b[0m:",
        "  \x1b[1;38;2;80;250;123mcmd1\x1b[0m  ",
        "  \x1b[1;38;2;80;250;123mcmd2\x1b[0m  ",
        "",
        "\x1b[1;3;38;2;241;250;140mCommands\x1b[0m:",
        "  \x1b[1;38;2;80;250;123mothercmd\x1b[0m  ",
    ]


def test_unkown_command(runner):
    @click.group(cls=StyledGroup, command_groups={"main": ["cmd1", "unknowncmd"]})
    def cli():
        pass

    @cli.command(cls=StyledCommand, styles={"header": "yellow", "option": "green"})
    @click.option("--name", help="The person to greet.")
    def cmd1(count):
        pass

    @cli.command()
    def cmd2():
        pass

    @cli.command()
    def othercmd():
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert isinstance(result.exception, ValueError)
    assert (
        str(result.exception)
        == "Unable to find command 'unknowncmd' in list of commands"
    )


def test_option_group(runner):
    @click.group(cls=StyledGroup, styles={"header": "yellow", "option": "green"})
    def cli():
        pass

    @cli.command(option_groups={"Config": ["--config", "--save-config"]})
    @click.option("--name", help="The person to greet.")
    @click.option("--config", help="path to config")
    @click.option("--save-config", help="save config", is_flag=True)
    def command(name):
        pass

    result = runner.invoke(cli, ["command", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: \x1b[1mcli command\x1b[0m \x1b[1m[OPTIONS]\x1b[0m",
        "",
        "\x1b[33mConfig\x1b[0m:",
        "  \x1b[32m--config \x1b[0m\x1b[32mTEXT\x1b[0m  path to config",
        "  \x1b[32m--save-config\x1b[0m  save config",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--name \x1b[0m\x1b[32mTEXT\x1b[0m  The person to greet.",
        "  \x1b[32m--help\x1b[0m       Show this message and exit.",
    ]


def test_unknown_option(runner):
    @click.command(
        cls=StyledCommand, option_groups={"Config": ["--config", "--save-config","--unknown-option"]}
    )
    @click.option("--name", help="The person to greet.")
    @click.option("--config", help="path to config")
    @click.option("--save-config", help="save config", is_flag=True)
    def cli(name):
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert isinstance(result.exception, ValueError)
    assert (
        str(result.exception)
        == "Unable to find option '--unknown-option' in list of options"
    )