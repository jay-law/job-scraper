# Introduction

Job boards (like LinkedIn) can be a good source for finding job openings.  Unfortunately the search results cannot always be filtered to a usable degree.  Exfill (short for extraction) lets users scrape and parse jobs with more flexability provided by the default search.

Currently only LinkedIn is supported.

# Project Structure

Directories:
- `src/exfill/parsers` - Contains parser(s)
- `src/exfill/scrapers` - Contains scraper(s)
- `src/exfill/support` 
    - Contains `geckodriver` driver for FireFox which is used by Selenium
    - Download the latest driver from the [Mozilla GeckoDriver repo in GitHub](https://github.com/mozilla/geckodriver)
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
        "username": "jay-law@protonmail.com",
        "password": "password1"
    }
}
```

# Usage

There are two `actions` required to generate usable data:

First is the scraping action.  When called, a browser will open and perform a job query on the specified `site`.  Each posting will be exported to the `data/html` directory.  

The second action is parsing.  Each job posting in `data/html` will be opened and analyzed.  Once all postings have been analyzed a single CSV file will be exported to `data/csv`.

The csv file provides a high-level overview of all the jobs returned during the query.  When imported to a spreadsheet, users can filter on fields not present in the original search options.  Examples include sorting by companies or excluding certain industries.

## Use as Code

```bash
# Install with git
$ git clone git@github.com:jay-law/job-scraper.git

# Create and populate creds.json.  Bash only:
cat <<EOF > creds.json
{
    "linkedin": {
        "username": "jay-law@protonmail.com",
        "password": "password1"
    }
}
EOF

# Activate virtual env
$ poetry shell

# Install dependencies
$ poetry install            # all deps
$ poetry install --no-dev   # don't install linters/formatters

# Execute - Scrape linkedin
$ python3 exfill/extractor.py linkedin scrape

# Execute - Parse linkedin
$ python3 exfill/extractor.py linkedin parse
```

## Use as Module

NOTE - This was broken during the implementation of poetry.  It will be fixed soon... Hopefully

```bash
# Install
$ python3 -m pip install --upgrade exfill

# Execute - Scrape linkedin
$ python3 -m exfill.extractor linkedin scrape

# Execute - Parse linkedin
$ python3 -m exfill.extractor linkedin parse
```

# Roadmap

* [x] Write unit tests
* [ ] Improve secret handling
* [x] Add packaging
* [x] Move paths to config file
* [x] Move keyword logic
* [x] Set/include default config.ini for users installing with PIP
* [x] Add CICD
* [x] Automate versioning
* [x] Add formatter (black module)
* [x] Add static type checking (mypy module)
* [x] Add import sorter (isort module)
* [x] Add linter (flake8 module)
* [x] Update string interpolation from %f to f-string
* [x] Replace sys.exit calls with exceptions
* [x] Update how the config object is accessed
* [x] Migrate to `poetry` for virtual env, building, and publishing
* [x] Replace os.path usage with pathlib
* [x] Replace pandas export with csv export
* [ ] Replace unittest with pytest