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

## Add Creds File

This is required for all usage.

```bash
# Create and populate creds.json.  Bash only:
cat <<EOF > creds.json
{
    "linkedin": {
        "username": "jay-law@users.noreply.github.com",
        "password": "password1"
    }
}
EOF
```

## Execute

```bash
# Install with git
git clone git@github.com:jay-law/job-scraper.git

# Install dependencies
$ poetry install

# Ensure creds.json exists (see above)

# Execute - Scrape linkedin
python3 exfill/extractor.py linkedin scrape

# Execute - Parse linkedin
$ python3 exfill/extractor.py linkedin parse



poetry run script-run -c config.ini scrape
```