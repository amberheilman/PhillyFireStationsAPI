#!/usr/bin/env python
import sys

from setuptools import setup, find_packages

from emswatch import __version__


if sys.version_info < (2, 7):
    raise Exception("This package requires Python 2.7 or higher.")

setup(
    name='Emergency Services Watch API',
    description='An API for Emergency Services data',
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'psycopg2',
        'queries',
        'tornado>=4.0.2'
    ],
    long_description='An API for Philadelphia Emergency Services data',
    dependency_links=['http://pypi.colo.lair/simple/'],
    version=__version__,
    author='Amber Heilman',
    author_email='amber.l.heilman@gmail.com'
)
