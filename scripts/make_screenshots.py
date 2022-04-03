#!/usr/bin/env python

# Used to generate the screenshots for the README
# Depends on several subprocess calls to imagemagick and wmctrl.


import shlex
import subprocess
import sys
import time
from pathlib import Path
from textwrap import wrap

from rich.console import Console
from rich.prompt import Confirm

PAD = 2

console = Console()

WINDOW_TITLE = "click_rich_help demo"


def setup_term():
    subprocess.run(shlex.split(f'echo -e "\033]0;{WINDOW_TITLE}\007"'))
    term_dim = {"width": console.width + 1, "height": console.height + 1}

    term_dim_px = {}

    result = subprocess.run(shlex.split("wmctrl -lG "), capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if WINDOW_TITLE in line:
            window_id = line.split()[0]
            term_dim_px["width"] = int(line.split()[4])
            term_dim_px["height"] = int(line.split()[5])

    return window_id, {
        dim: term_dim_px[dim] / term_dim[dim] for dim in ["width", "height"]
    }


def screenshot(cmd, window_id, ratios, outfile):

    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    columns = len(max(result.stdout.splitlines(), key=len)) + PAD + 10
    width = round(columns * ratios["width"])
    height = round(
        (len(result.stdout.splitlines()) + PAD + 2 + (1 if len(cmd) > columns else 0))
        * ratios["height"]
    )

    # deal with long commands

    printcmd = "\n\t".join(wrap(cmd, columns))
    print(f">>> {printcmd} \n")
    subprocess.run(shlex.split(cmd))
    # print(''.join(["\n"]*(4 if "\t" in printcmd else 3)))
    print("\n\n\n")
    time.sleep(1)
    subprocess.run(
        shlex.split(f"import -window {window_id} -crop {width}x{height}+0+0 {outfile}")
    )
    console.clear()


base_cmd = "python -m click_rich_help.example"


def main():
    console = Console()

    window_id, ratios = setup_term()
    outdir = Path("assets/screenshots")
    outdir.mkdir(exist_ok=True, parents=True)

    if not Confirm.ask(
        f"You are about to overwrite the screenshots in [cyan]{outdir}[/], proceed?"
    ):
        sys.exit()

    cmd = "python -m click_rich_help.example -h"
    cmds = {
        **{
            f"{base_cmd} -h": outdir / "base.png",
            f"{base_cmd} src src": outdir / "src_src.png",
            (
                f"{base_cmd} test"
                ' --string "[red]red [i]red italic[/red] just italic[/i]"'
                ' --style "magenta reverse"'
            ): outdir
            / "test_str_style.png",
        },
        **{
            f"{base_cmd} {cmd} -h": outdir / f"{fname}.png"
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
        **{
            "python scripts/option_example.py --help": outdir / "option_example.png",
            "python scripts/option_example.py inherit --help": outdir
            / "option_example_inherit.png",
        },
    }

    console.clear()
    time.sleep(1)
    for cmd, outfile in cmds.items():
        screenshot(cmd, window_id, ratios, outfile)
    console.print("done")


if __name__ == "__main__":
    main()
