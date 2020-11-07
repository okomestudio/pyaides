#!/usr/bin/env python
import codecs
import os
import re

from setuptools import find_packages
from setuptools import setup


def meta(category, fpath="src/pyaides/__init__.py"):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, fpath), "r") as f:
        package_root_file = f.read()
    matched = re.search(
        r"^__{}__\s+=\s+['\"]([^'\"]*)['\"]".format(category), package_root_file, re.M
    )
    if matched:
        return matched.group(1)
    raise Exception("Meta info string for {} undefined".format(category))


requires = []
aws_requires = ["boto3>=1.14.20"]

setup_requires = ["pytest-runner==5.2"]

dev_requires = [
    "black>=19.10b0",
    "flake8>=3.8.3",
    "isort>=5.0.9",
    "pre-commit>=2.6.0",
] + aws_requires

tests_require = [
    "coverage>=5.2",
    "moto>==1.3.14",
    "pytest>=5.4.3",
    "pytest-cov>=2.10.0",
    "pytest-mock>=3.2.0",
] + aws_requires

setup(
    name="pyaides",
    version=meta("version"),
    description="Light-weight Python 3 utilities",
    author=meta("author"),
    author_email=meta("author_email"),
    license=meta("license"),
    url="https://github.com/okomestudio/pyaides",
    platforms=["Linux"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    scripts=[],
    install_requires=requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        "aws": aws_requires,
        "dev": dev_requires + tests_require,
        "tests": tests_require,
    },
    entry_points={
        "console_scripts": ["sqs-delete-queues=pyaides.aws.sqs.sqs:CLI.delete_queues"]
    },
)
