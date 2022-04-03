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

See the [documentation](https://github.com/daylinmorgan/click-rich-help/blob/main/docs/usage.md) for more info

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
