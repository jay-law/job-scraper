
# Config Development Environment

## Install Python and Poetry

Tested on Ubuntu Ubuntu 20.04.4 LTS (64-bit) and Python 3.8.10.

[Poetry](https://python-poetry.org/docs/) is used for the virtual environment, building, and publishing.  Install and configure according to the official documentation.

## Clone Repo

```bash
# Clone repo
$ git clone git@github.com:jay-law/job-scraper.git
$ cd job-scraper/

# Create new branch
$ git checkout -b BRANCH_NAME

# Activate virtual env
$ poetry shell

# Install dependencies
$ poetry install 

########################
# make changes to code
########################

# Update version
$ poetry version patch

# Check linting and formatting before commit
$ pre-commit run --all-files

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

See the `.vscode/settings.json` file for details if desired.

## pre-commit

`pre-commit` is used to trigger linting and formatting during a git commit call.  Hooks are defined in `.pre-commit-config.yaml`.

### Usage

```bash
# Install
$ poetry add pre-commit --dev

# Add .pre-commit-config.yaml file

# Create hook
$ pre-commit install

# Remove hook
$ pre-commit uninstall

# Run hook without commit
$ pre-commit run --all-files
```

## GitHub Actions

See `.github/workflows/linters.yml` for details.

# Tools

Linters and formatters are listed below.

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
$ poetry add black --dev

# Run manually - Check if files will be changed
$ black --check exfill/

# Run manually - Make changes
$ black exfill/
```

## isort

`isort` is used to order import statements.

* [x] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [x] GitHub Actions (`.github/workflows/linters.yml`)

Settings - `pyproject.toml`

### Usage

```bash
# Install
$ poetry add isort --dev

# Run manually - See difference but don't make change
$ isort --check --diff .

# Run manually - settings are picked up from pyproject.toml
$ isort .
```

## flake8

`flake8` is used to lint code

* [x] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [x] GitHub Actions (`.github/workflows/linters.yml`)

Settings - None. Just using default config.

### Usage

```bash
# Install
$ poetry add flake8 --dev

# Run manually
$ flake8 exfill/
```

## mypy

`mypy` is used for static type checking.

* [ ] VSCode (`.vscode/settings.json`)
* [x] Git pre-commit hook
* [ ] GitHub Actions (`.github/workflows/linters.yml`)

[Settings](https://mypy.readthedocs.io/en/stable/config_file.html#example-pyproject-toml) - `pyproject.toml`

### Usage

```bash
# Install
$ poetry add mypy --dev

# Run manually
$ mypy
```

# Testing

```bash
# Clone repo
$ git clone git@github.com:jay-law/job-scraper.git
$ cd job-scraper/

# Install deps
$ poetry install

# Run tests (method 1)
$ poetry run pytest tests/

# Run tests (method 2)
$ poetry run script-tests
# script-tests is defined in pyproject.toml
```

# Publishing

## Automatic

Create a pull request to merge into the 'main' branch.  First `linters.yml` will be triggered.  Next `publish-prod.yml` will be triggered.

Check the [actions](https://github.com/jay-law/job-scraper/actions) page for progress. 

## Manual

It might be beneficial to manually publish a package.

```bash
# Update version
$ poetry version patch

# Build
$ poetry build

# Publish - test (might require you to add the test pypi repo)
$ poetry publish -r testpypi

# Publish
$ poetry publish
```

## Testing Published Package

```bash
# Create new project
$ poetry new python-test
$ cd python-test

# Activate virtual env 
$ poetry shell

# Install from TestPyPI
?

# Install from PyPI
$ poetry add exfill

# Ensure creds.json exists

# Execute - Scrape linkedin
$ python3 -m exfill.extractor linkedin scrape

# Execute - Parse linkedin
$ python3 -m exfill.extractor linkedin parse
```