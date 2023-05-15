
# Config Development Environment

## Install Python and Poetry

Tested on Ubuntu Ubuntu 20.04.4 LTS (64-bit) and Python 3.8.10.

[Poetry](https://python-poetry.org/docs/) is used for the virtual environment, building, and publishing.  Install and configure according to the official documentation.

## Example

This is a basic workflow of what a contribution might look like. 

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
$ poetry run pre-commit run --all-files

# Add, commit, and push in git
$ git add *
$ git commit -m 'git commit message'
$ git push -u origin BRANCH_NAME

# Create a pull request
```

---

# Linting and Formatting Enforcement

Linting is enforced with pre-commit hooks locally.

See LINTING.md for more details.

---

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

---

# Publishing

Packages can be published manually (locally) or automatically with GitHub Actions.  Both methods are described below.

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