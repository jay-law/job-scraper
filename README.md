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
$ pip install -r requirements.txt

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

## Execution

There are two phase.  First is scraping the postings.  Second is parsing the scraped information.  Therefore the scraping phase must occur before the parsing phase.

```bash
# Scrape linkedin
$ python3 main.py linkedin scrape

# Parse linkedin
$ python3 main.py linkedin parse
```

# Other

## Improvements

### Write Tests

Write some unit tests.

###  Move Keyword Logic

The `linkedin_parser.py` file has logic to identify key terms like "on-call rotation" or industries like "Staffing and Recruiting".  

Ideally the GUI front-end would handle this type of functionality.  Until a GUI option is available, the logic should probably be moved to a seperate function.

### Add File Args to Scraper/Parser

The import and export file paths are set in each method/module.  This adds bloat to each module as much of the code is reusable.  File handling can be moved to the main controller or a new module, file names would be passed to the scraper/parser functions.

### Improve Secret Handling

The current implementation of importing credentials is almost certainly insecure.

### Setup Packaging

This script has only been used locally as the job postings generated can be pasted into a browser.  If this program was to be "productionized" then proper packaging should be implemented.