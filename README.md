# Configure Environment

```bash

# Confirm Python 3 is installed
$ python3 --version

Python 3.8.10

# Install venv.  I thought this shipped with python?
$ sudo apt install python3.8-venv

# Install pip.  All other components will be installed with pip
$ sudo apt install python3-pip


# Create venv
$ python3 -m venv venv

# Activate venv
$ source venv/bin/activate

# Install beautifulsoup4, selenium, and pandas
$ python3 -m pip install beautifulsoup4 selenium pandas
```

# Contributing

```bash

# update requirements
$ python3 -m pip freeze > requirements.txt

```