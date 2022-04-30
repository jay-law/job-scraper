# Introduction

Job boards (like LinkedIn) can be a good source for finding job openings.  Unfortunately the search results cannot always be filtered to a usable degree.  This application lets users scrape, parse, and filter jobs with more flexability provided by the default search.

Currently only LinkedIn is supported.

# Project Structure

Files:
- `main.py` - Application to be executed
- `README.md` - Documentation
- `.gitignore` - Git ignore
- `requirements.txt` - Requirements file for PIP 
- `creds.json` - Credential file 

Directories:
- `parsers` - Contains parser(s)
- `scrapers` - Contains scraper(s)
- `support` 
    - Contains `geckodriver` driver for FireFox which is used by Selenium
    - Download the latest driver from the [Mozilla GeckoDriver repo in GitHub](https://github.com/mozilla/geckodriver)
- `venv` 
    - Not in source control
    - Virtual environment for Python execution.  Gets created with `python3 -m venv venv` (see below)
- `data/html` 
    - Not in source control
    - Contains HTML elements for a specific job posting
    - Populated by a scraper
- `data/csv` 
    - Not in source control
    - Contains parsed information in a csv table
    - Populated by a parser
    - Also contains an error table
- `logs` 
    - Not in source control
    - Contains logs created during execution

## `creds.json` File

Syntax should be as follows:

```json
{
    "linkedin": {
        "username": "jay-law@gmail.com",
        "password": "password1"
    }
}
```

# Usage

## Configure Environment

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

## Execution

There are two phase.  First is scraping the postings.  Second is parsing the scraped information.  Therefore the scraping phase must occur before the parsing phase.

```bash
# Scrape linkedin
$ python3 src/job_scraper/go_module.py linkedin scrape

# Parse linkedin
$ python3 src/job_scraper/go_module.py linkedin parse
```

## Contributing

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
$ python3 -m pip install -r requirements.txt

########################
# make changes to code
########################

# Add modules as needed
$ python3 -m pip install SOME_NEW_MODULE

# Update requirements if modules were added
$ python3 -m pip freeze > requirements.txt

# Lint befor commiting
$ pylint *

# Add, commit, and push in git
$ git add *
$ git commit -m 'git commit message'
$ git push -u origin BRANCH_NAME

# Create a pull request
```

## Publishing

```bash
$ python3 -m pip install --upgrade build
$ python3 -m pip install --upgrade setuptools_scm
$ python3 -m pip install --upgrade twine

# Build 
$ python3 -m build

# Publish
$ python3 -m twine upload --repository testpypi --skip-existing dist/*
```

# Roadmap

* [ ] Write unit tests
* [ ] Improve secret handling
* [ ] Add packaging
* [x] Move paths to config file
* [x] Move keyword logic
* [x] Move keyword logic
