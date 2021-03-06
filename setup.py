#!/usr/bin/env python
import os
from setuptools import setup

README_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(README_PATH, "r") as readme_file:
    README = readme_file.read()

setup(
    name="kaizen",
    version="0.1.4",
    description=("A python client and cli to manage your projects on AgileZen"
                 " Kanban style."),
    long_description=README,
    packages=["kaizen"],
    author="Bertrand Vidal",
    author_email="vidal.bertrand@gmail.com",
    download_url="https://pypi.python.org/pypi/kaizen",
    url="https://github.com/bertrandvidal/kaizen",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    setup_requires=[
        "nose",
        "mock==1.0.1",
        "responses",
    ],
    install_requires=[
        "requests",
        "parse_this",
        "pyyaml"
    ],
    entry_points={
        # Console script entry points will result in commandline
        # calling specified python callable. If your package include
        # command line tools, add them here:
        'console_scripts': [
            'kaizen = kaizen.cli:run_cli',
            ],
    },
)
