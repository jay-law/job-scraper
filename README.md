# Configure Environment

```bash
# Confirm Python 3 is installed
$ python3 --version

Python 3.8.10

# Install venv.  I thought this shipped with python?
$ sudo apt install python3.8-venv

# Install pip
$ sudo apt install python3-pip
```

# Contributing

```bash

# Clone repo
$ git clone git@github.com:jay-law/job-scraper.git
$ cd job-scraper/

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
$ python3 -m pip uninstall pylint

# Update requirements
$ python3 -m pip freeze > requirements.txt

# Add, commit, and push in git
$ git add *
$ git commit -m 'git commit message'
$ git push

```