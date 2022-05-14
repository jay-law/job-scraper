"""Set path for import
"""
import os
import sys

from setuptools_scm import get_version

sys.path.append(os.path.dirname(__file__))

__version__ = get_version()
