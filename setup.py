#!/usr/bin/python
from distutils.core import setup

config = {
    "description"     : "Utilities for polling a Sidekiq web server",
    "author"          : "Isaac Johnston",
    "url"             : None,
    "download_url"    : None,
    "author_email"    : "isaac@caplinked.com",
    "version"         : "0.1.0",
    "install_requires": [],
    "packages"        : ["sidekiqutils", "sidekiqutils.tests"],
    "scripts"         : ["bin/pollsidekiq.py"],
    "name"            : "sidekiqutils",
    "license"         : None,
    "long_description": open("README.txt").read()
}

setup(**config)
