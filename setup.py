#!/usr/bin/env python
import os

from setuptools import setup

setup(
    name="func2pipe",
    version="0.2.0",
    description="Convert functions into generators",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="profesor Hrbolek",
    author_email="profesor@hrbolek.cz",
    packages=["func2pipe"],
    install_requires=["setuptools"],
)
