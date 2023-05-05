"""Separate file for config vars."""

import os

DEBUG = os.environ.get('DEBUG', 'False') in {'1', 'True', 'true'}
