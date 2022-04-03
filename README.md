<div id="top"></div>

<!-- PROJECT SHIELDS -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![CircleCI][circleci-shield]][circleci-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/daylinmorgan/click-rich-help">
    <img src="https://raw.githubusercontent.com/daylinmorgan/click-rich-help/main/assets/logo.png" alt="Logo" width=400 >
  </a>

<h2 align="center">click-rich-help</h2>

  <p align="center">
    make a beautiful click app with rich
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project

I wanted a simple python package to make my click app's help more readable.

Since writing this package the more opinionated [rich-click](https://github.com/ewels/rich-click) has been written.
If that output is more your speed, go check it out! This project aims to provide a slightly different API and set of features.

![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/base.png)

## Getting Started

### Installation

with pip:
``` bash
pip install click-rich-help
```
with conda/mamba:
```bash
conda install -c conda-forge click-rich-help
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

As of `v22.1.0` you may no longer generate styles using named args.

At a minimum you should apply `StyledGroup` to your `click` group.
If you have only one `Command` or `Multicommand` you may also use the included `StyledCommand` or `StyledMultiCommand`.

```python
import click
from click_rich_help import StyledGroup

@click.group(
    cls=StyledGroup,
)
def cli():
    pass
```

```python
import click
from click_rich_help import StyledCommand

@click.command(
  cls=StyledCommand,
)
def cmd():
    pass
```

![screenshot](https://raw.githubusercontent.com/daylinmorgan/click-rich-help/main/assets/screenshots/base.png)

See the [documentation](https://github.com/daylinmorgan/click-rich-help/blob/main/docs/usage.md) for more info

You have several options for defining your own style.
You can pass a dictionary containing the key value pairs for styles you want included.
`Click-rich-help` defines the following base style which will be applied when no other arguments are provided to the helper classes.

```python
{
  "header": "bold italic cyan",
  "option": "bold yellow",
  "metavar": "green",
  "default": "dim",
  "required": "dim red",
}
```

Additionally, with `python -m click_rich_help.example cmd1 -h` you can see the remaining default theme styles in action.

![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/cmd1.png)

One additional `click_rich_help` specific style is `doc_style` which can be used to apply styling across long and short docstrings.

![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/cmd3.png)

You can also provide a `rich.theme.Theme` and define the style itself in a separate file:

`default.ini`:
````ini
[styles]
headers="green"
options="yellow"
metavar="red"
````

```python
@click.group(
    cls=StyledGroup,
    theme=Theme.read("default.ini")
)
def cli():
    pass
```

Style options are parsed by `styles` before `theme`. So you may define both depending on your needs.

Any styles passed to the helper classes will be accessible and can be applied using `rich` markup syntax


![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/theme.png)

If you define any styles and wish to apply them on top of the default style you can pass `"use_theme=default"`

```python
@click.command(cls=StyledCommand,
  styles={
    "header": "bold red underline reverse"
  }
)
@click.option("--count", default=1, help="[red]Number[/red] of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets [b yellow]NAME[/b yellow] for a total of [b yellow]COUNT[/b yellow] times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")
```

Without `use_theme="default"`:

![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/option_example.png)

With `use_theme="default"`:
![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/option_example_inherit.png)


You may also pass `command_groups` or `option_groups` to the helper classes in order to organize help output.

![screenshot](https://github.com/daylinmorgan/click-rich-help/blob/main/assets/screenshots/group.png)

Currently options are matched against long options. Use `--output` not `-o`. When defining your grouping dictionary.

To non-interactively preview the included example module in your own terminal you can run

W/ `click-rich-help`  and `curl`

```bash
curl -s https://raw.githubusercontent.com/daylinmorgan/click-rich-help/main/scripts/example.sh | bash
```

You can also run it yourself if you have installed `click-rich-help`. Which you should!

```bash
python -m click_rich_help.example -h
```

<p align="right">(<a href="#top">back to top</a>)</p>


## Contributing
To contribute please utilize `poetry` and `pre-commit`.

optionally manage python installation with `conda`:

```bash
conda create -p ./env python poetry
```

Then follow the below steps
1. Fork the Project
2. Install the package and dev dependencies w/poetry(`cd click-rich-help; poetry install`)
2. Create your Feature Branch (`git checkout -b feat/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Run the tests (`mypy click_rich_help; py.test tests`)
5. Push to the Branch (`git push origin feat/AmazingFeature`)
6. Open a Pull Request


<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

* [click](https://github.com/pallets/click)
* [rich](https://github.com/willmcgugan/rich)
* [click-help-colors](https://github.com/click-contrib/click-help-colors)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/daylinmorgan/click-rich-help.svg?style=flat
[contributors-url]: https://github.com/daylinmorgan/click-rich-help/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/daylinmorgan/click-rich-help.svg?style=flat
[forks-url]: https://github.com/daylinmorgan/click-rich-help/network/members
[stars-shield]: https://img.shields.io/github/stars/daylinmorgan/click-rich-help.svg?style=flat
[stars-url]: https://github.com/daylinmorgan/click-rich-help/stargazers
[issues-shield]: https://img.shields.io/github/issues/daylinmorgan/click-rich-help.svg?style=flat
[issues-url]: https://github.com/daylinmorgan/click-rich-help/issues
[license-shield]: https://img.shields.io/github/license/daylinmorgan/click-rich-help.svg?style=flat
[license-url]: https://github.com/daylinmorgan/click-rich-help/blob/main/LICENSE.txt
[circleci-shield]: https://img.shields.io/circleci/build/gh/daylinmorgan/click-rich-help?style=flat
[circleci-url]: https://img.shields.io/circleci/build/gh/daylinmorgan/click-rich-help
