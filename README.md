# Poetry pre-commit Plugin

[![PyPI](https://img.shields.io/pypi/v/poetry-pre-commit-plugin?color=blue)](https://pypi.org/project/poetry-pre-commit-plugin/)

A [Poetry](https://python-poetry.org/) plugin for automatically installing git
pre-commit hooks whenever `pre-commit` is specified as a dependency of the
project.

## Motivation

Personally I find that running `pre-commit install` every time I start working
on a new repository is very easy to forget - there have been numerous occasions
where I'd forget this step, commit some changes only to be surprised later on
by failing CI checks 😅 This plugin aims to solve this issue by doing
this small step for me automatically behind the scenes.

## Installation

The plugin requires Poetry version `1.2.0b1` or above. Since this is still a
pre-release version, you have to specify it explicitly when installing:

```
curl -sSL https://install.python-poetry.org | python3.9 - --version 1.2.0b3
```

Once a valid version of Poetry is set up, you can install the plugin like so:

```
poetry self add poetry-pre-commit-plugin
```

For more in-depth information, please refer to
[Poetry's docs](https://python-poetry.org/docs/master/plugins/).

## Usage

There's no way to use this plugin explicitly - it will work behind the scenes
after you run either `poetry install` or `poetry add`. In either of those cases,
the plugin will check the following conditions:

1. Is the project inside a git repository?
2. Is `pre-commit` listed as a dependency of the project (or, in the case of
   `poetry add` - was it just added)?
3. Has the pre-commit hook **not** been activated yet (i.e. the file
   `.git/hooks/pre-commit` does not exist)?

If all conditions are met, the plugin will run `pre-commit install` for you.
