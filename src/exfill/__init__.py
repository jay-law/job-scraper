"""Set path for import
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

from setuptools_scm import get_version

__version__ = get_version()

# __version__ = "1.1.2"
