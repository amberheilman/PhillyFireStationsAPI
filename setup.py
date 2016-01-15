#!/usr/bin/env python
import sys

from setuptools import setup, find_packages

from emswatch import __version__


if sys.version_info < (3, 0):
    raise Exception("This package requires Python 3 or higher.")

setup(
    name='emswatch',
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
    version=__version__,
    author='Amber Heilman',
    author_email='amber.l.heilman@gmail.com',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Operating System :: MacOS :: MacOS X'
    ],
    entry_points={
        'console_scripts': [
            'emswatch = emswatch.app:make_app'
        ]
    }
)
