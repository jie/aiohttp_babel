# -*- coding: utf-8 -*-
"""
    Babel localisation support for aiohttp
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name = "aiohttp-babel",
    version = "0.0.5",
    packages = find_packages(),

    install_requires = [
        "aiohttp",
        "babel",
        "speaklater",
    ],

    author = "zhouyang",
    author_email = "zhouyang@zhouyang.me",
    description = "Babel localisation support for aiohttp",
    license = "BSD",
    keywords = "aiohttp locale babel localisation",
    url = "https://github.com/jie/aiohttp_babel",
)
