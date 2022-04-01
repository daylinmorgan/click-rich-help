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
    term_dim = {"width": console.width, "height": console.height}

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

    # check the width and height of the output
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    columns = len(max(result.stdout.splitlines(), key=len)) + PAD
    width = int(columns * ratios["width"])
    height = int((len(result.stdout.splitlines()) + PAD + 2) * ratios["height"])
    # deal with long commands
    printcmd = "\n\t".join(wrap(cmd,columns))

    console.clear()
    print(f">>> {printcmd} \n")
    subprocess.run(shlex.split(cmd))
    print("\n\n")
    time.sleep(1)
    subprocess.run(
        shlex.split(f"import -window {window_id} -crop {width}x{height}+0+0 {outfile}")
    )


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
                ' --string "[red]REDTEXT [i]REDITALIC[/red] JUSTITALIC[/i]"'
                ' --style "magenta reverse"'
            ): "test_str_style.png",
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
    }

    for cmd, outfile in cmds.items():
        screenshot(cmd, window_id, ratios, outfile)
    console.print("done")


if __name__ == "__main__":
    main()
