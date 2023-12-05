#!/usr/bin/env python

# Used to generate the screenshots for the README
# Requires rich>12.2 currently using development copy from github

import sys
from pathlib import Path
from textwrap import wrap

from rich.text import Text
from rich.console import Console
from rich.prompt import Confirm
from click.testing import CliRunner
from click_rich_help.example import cli as example_cli
from option_example import cli as option_cli

PAD = 2

# override svg format to remove background and have simple terminal window
CONSOLE_SVG_FORMAT = """\
<svg width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Regular"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
            font-style: normal;
            font-weight: 400;
        }}
        @font-face {{
            font-family: "{font_family}";
            src: local("FiraCode-Bold"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
            font-style: bold;
            font-weight: 700;
        }}
        .{classes_prefix}-terminal-wrapper span {{
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: {font_size}px;
            font-family:'{font_family}','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }}
        .{classes_prefix}-terminal-wrapper a {{
            text-decoration: none;
            color: inherit;
        }}
        .{classes_prefix}-terminal-body .blink {{
           animation: {classes_prefix}-blinker 1s infinite;
        }}
        @keyframes {classes_prefix}-blinker {{
            from {{ opacity: 1.0; }}
            50% {{ opacity: 0.3; }}
            to {{ opacity: 1.0; }}
        }}
        .{classes_prefix}-terminal-wrapper {{
            padding: {margin}px;
            padding-top: 100px;
        }}
        .{classes_prefix}-terminal {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: {theme_background_color};
            border-radius: 14px;
            outline: 1px solid #484848;
        }}
        .{classes_prefix}-terminal-header {{
            position: relative;
            width: 100%;
            background-color: #2e2e2e;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: {theme_foreground_color};
            font-size: 18px;
            box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                        inset 0px -4px 8px 0px #1a1a1a;
        }}
        .{classes_prefix}-terminal-title-tab {{
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 6px 6px 0 0;
            background-color: {theme_background_color};
            box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                        0px -4px 4px 0px #1e1e1e,
                        inset 1px 0px 0px 0px #4e4e4e,
                        inset -1px 0px 0px 0px #4e4e4e;
        }}
        .{classes_prefix}-terminal-traffic-lights {{
            position: absolute;
            top: 24px;
            left: 20px;
        }}
        .{classes_prefix}-terminal-body {{
            line-height: {line_height}px;
            padding: 14px;
        }}
        {stylesheet}
    </style>
    <foreignObject x="0" y="0" width="100%" height="100%">
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div class="{classes_prefix}-terminal-wrapper">
                <div class="{classes_prefix}-terminal">
                    <div class="{classes_prefix}-terminal-header">
                        <svg class="{classes_prefix}-terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                            <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                            <circle cx="62" cy="8" r="8" fill="#28c941"/>
                        </svg>
                        <div class="{classes_prefix}-terminal-title-tab">{title}</div>
                    </div>
                    <div class="{classes_prefix}-terminal-body">
                        {code}
                    </div>
                </div>
            </div>
        </body>
    </foreignObject>
</svg>
"""


def screenshot(cli,cmd,outfile):

    svg_console = Console(record=True)

    runner = CliRunner()
    result = runner.invoke(cli,cmd,color=True)
    rich_text = Text.from_ansi(result.output)
    max_cols = svg_console.measure(rich_text).maximum + PAD
    svg_console.width=max_cols

    printcmd = "\n\t".join(wrap(f"python -m click_rich_help.example {cmd}", max_cols))
    svg_console.print(f">>> {printcmd} \n")
    svg_console.print(rich_text)
    svg_console.save_svg(f"{outfile.with_suffix('.svg')}",title=f"click_rich_help.example",code_format=CONSOLE_SVG_FORMAT)


def main():
    outdir = Path("assets/screenshots")
    outdir.mkdir(exist_ok=True, parents=True)

    if not Confirm.ask(
        f"You are about to overwrite the screenshots in [cyan]{outdir}[/], proceed?"
    ):
        sys.exit()

    cmds = {
        **{
            f"-h": outdir / "base.png",
            f"src src": outdir / "src_src.png",
            (
                f"test"
                ' --string "[red]red [i]red italic[/red] just italic[/i]"'
                ' --style "magenta reverse"'
            ): outdir
            / "test_str_style.png",
        },
        **{
            f"{cmd} -h": outdir / f"{fname}.png"
            for cmd, fname in {
                "cmd1": "cmd1",
                "cmd2": "cmd2",
                "cmd3": "cmd3",
                "group": "group",
                "src": "src",
                "test": "test",
                "theme": "theme",
            }.items()
        },
    }

    for cmd, outfile in cmds.items():
        screenshot(example_cli,cmd,outfile)

    cmds = {
            "hello --help": outdir / "option_example.png",
            "inherit --help": outdir / "option_example_inherit.png",
        }

    for cmd,outfile in cmds.items():
        screenshot(option_cli,cmd,outfile)

    print("done")


if __name__ == "__main__":
    main()
