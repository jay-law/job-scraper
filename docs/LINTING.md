
# Overview

Linters and formatters are "enforced" with IDE settings (VSCode), pre-commit hooks, GitHub Actions.  Each tool (black, isort, etc.) can be triggered in the following situations:
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

## VSCode Settings

See the `.vscode/settings.json` file for details.

---

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

# Run manually.  This will produce different results from running in
# the pre-commit hook
$ mypy
```