import click

from click_rich_help import StyledGroup, StyledMultiCommand


def test_multi_command(runner):
    @click.group()
    def cmd1():
        pass

    @cmd1.command()
    @click.option("--count", default=1, help="Some number.")
    def command1(count):
        click.echo("command 1")

    @click.group(cls=StyledGroup, styles={"header": "red", "option": "blue"})
    def cmd2():
        pass

    @cmd2.command()
    @click.option("--name", help="Some string.")
    def command2(name):
        click.echo("command 2")

    class MyCLI(StyledMultiCommand):
        def list_commands(self, ctx):
            return ["cmd1", "cmd2"]

        def get_command(self, ctx, name):
            commands = {"cmd1": cmd1, "cmd2": cmd2}
            return commands[name]

    @click.command(cls=MyCLI, styles={"header": "yellow", "option": "green"})
    def cli():
        pass

    result = runner.invoke(cli, ["--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: \x1b[1mcli\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[33mCommands\x1b[0m:",
        "  \x1b[32mcmd1\x1b[0m  ",
        "  \x1b[32mcmd2\x1b[0m  ",
    ]

    result = runner.invoke(cli, ["cmd1", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[33mUsage\x1b[0m: \x1b[1mcli cmd1\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[33mOptions\x1b[0m:",
        "  \x1b[32m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[33mCommands\x1b[0m:",
        "  \x1b[32mcommand1\x1b[0m  ",
    ]

    result = runner.invoke(cli, ["cmd2", "--help"], color=True)
    assert not result.exception
    assert result.output.splitlines() == [
        "\x1b[31mUsage\x1b[0m: \x1b[1mcli cmd2\x1b[0m \x1b[1m[OPTIONS] COMMAND [ARGS]...\x1b[0m",
        "",
        "\x1b[31mOptions\x1b[0m:",
        "  \x1b[34m--help\x1b[0m  Show this message and exit.",
        "",
        "\x1b[31mCommands\x1b[0m:",
        "  \x1b[34mcommand2\x1b[0m  ",
    ]
