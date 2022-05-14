
# Config Development Environment

## Install Python

Tested on Ubuntu Ubuntu 20.04.4 LTS (64-bit) and Python 3.8.10.

```bash
# Confirm Python 3 is installed
$ python3 --version

Python 3.8.10

# Install venv
$ sudo apt install python3.8-venv

# Install pip
$ sudo apt install python3-pip
```

## Clone Repo

```bash
# Clone repo
$ git clone git@github.com:jay-law/job-scraper.git
$ cd job-scraper/

# Create new branch
$ git checkout -b BRANCH_NAME

# Create venv
$ python3 -m venv venv

# Activate venv
$ source venv/bin/activate

# Install requirements
$ pip install -r requirements.txt

########################
# make changes to code
########################

# Update version in pyproject.toml

# Add modules as needed
$ pip install --upgrade SOME_NEW_MODULE

# Update requirements if modules were added
$ pip freeze > requirements.txt

# Lint befor commiting
$ pylint *

# Add, commit, and push in git
$ git add *
$ git commit -m 'git commit message'
$ git push -u origin BRANCH_NAME

# Create a pull request
```

# Linting and Formatting Enforcement

Linters and formatters are "enforced" with pre-commit hooks and GitHub Actions.  Each tool (black, isort, etc.) can be triggered in the following situations:
- Automatically in VSCode
  - See `.vscode/settings.json` for settings.  Plugins might be required
- Manually at the tool level
  - See the 'Usage' section for each tool below
- Manually with pre-commit hooks
  - Run `pre-commit run --all-files` from the CLI
- Automatically with pre-commit hooks
  - See `.pre-commit-config.yaml` 
- Automatically in GitHub Actions
  - See `.github/workflows/`

## VSCode Settings

todo

## pre-commit

`pre-commit` is used to trigger linting and formatting during a git commit call.  Hooks are defined in `.pre-commit-config.yaml`.

### Usage

```bash
# Install
$ python3 -m pip install --upgrade pre-commit

# Add .pre-commit-config.yaml file

# Create hook
$ pre-commit install

# Remove hook
$ pre-commit uninstall

# Run hook without commit
$ pre-commit run --all-files
```

## GitHub Actions

todo

# Tools

## black

`black` is used to format code.

* [x] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [x] GitHub Actions (`.github/workflows/linters.yml`)

Settings - `pyproject.toml`

If changes are not made on save, there might be a problem with `pyproject.toml`.

### Usage

```bash
# Install
$ python3 -m pip install --upgrade black

# Run manually - Check if files will be changed
$ black --check src/

# Run manually - Make changes
$ black src/
```

## isort

`isort` is used to order import statements.

* [ ] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [x] GitHub Actions (`.github/workflows/linters.yml`)

### Usage

```bash
# Install
$ python3 -m pip install --upgrade isort

# Run manually - See difference but don't make change
$ isort --check --diff .

# Run manually - settings are picked up from pyproject.toml
$ isort .
```

## mypy

`mypy` is used for static type checking.

Settings can be found in `pyproject.toml` ([toml example](https://mypy.readthedocs.io/en/stable/config_file.html#example-pyproject-toml)).

* [ ] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [ ] GitHub Actions (`.github/workflows/linters.yml`)

### Usage

```bash
# Install
$ python3 -m pip install --upgrade mypy

# Run manually
$ mypy
```

# Publishing

## Automatic

Merge your branch into the `test` branch.  GitHub actions will build and publish the package to [Test PyPI](https://test.pypi.org/project/exfill/).

If there are no errors, a second merge request can be created from `test` into `main` branch.  This workflow will publish to [PyPI](https://pypi.org/project/exfill/)

## Manual

It might be beneficial to manually publish a package.

```bash
# Install required tools
$ python3 -m pip install --upgrade build
$ python3 -m pip install --upgrade setuptools_scm
$ python3 -m pip install --upgrade twine

# Build 
$ python3 -m build

# Publish - test
$ python3 -m twine upload --repository testpypi --skip-existing dist/*

# Publish - prod
$ python3 -m twine upload --repository pypi --skip-existing dist/*
```

## Testing Published Package

```bash
$ mkdir python_test
$ cd python_test

# Create venv
$ python3 -m venv venv

# Activate venv
$ source venv/bin/activate

# Install from TestPyPI
# --extra-index-url helps with packages in prod but not test pypi
$ python3 -m pip install --extra-index-url https://test.pypi.org/simple/ exfill -U

# Or install from PyPI
$ python3 -m pip install --upgrade exfill

# Execute as mentioned in the README
```