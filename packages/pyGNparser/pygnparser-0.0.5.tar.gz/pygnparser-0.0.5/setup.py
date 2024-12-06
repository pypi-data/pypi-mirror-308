import codecs
from setuptools import setup
from setuptools import find_packages

with codecs.open("README.md", "r", "utf-8") as f:
    readme = f.read().replace("\r", '')

with codecs.open("CHANGELOG.md", "r", "utf-8") as f:
    changes = f.read().replace("\r", '')
changes = changes.replace(":issue:", "")
long_description = readme + "\n\n" + changes

setup(
    name="pyGNparser",
    version="0.0.5",
    description="Python client for GNparser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Geoff Ower",
    author_email="gdower@illinois.edu",
    url="http://github.com/gnames/pyGNparser",
    download_url="https://github.com/gnames/pyGNparser/archive/refs/tags/v0.0.5.tar.gz",
    license="MIT",
    packages=find_packages(exclude=["test-*"]),
    install_requires=[
        "requests>2.7"
    ],
    extras_require={
        "dev": [
            "codecov", 
            "pytest", 
            "pytest-cov", 
            "sphinx>7.2.0", 
            "sphinx_issues", 
            "sphinx-rtd-theme", 
            "twine", 
            "wheel"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords = ['biodiversity', 'scientific names', 'parser', 'nomenclature', 'taxonomy', 'API', 'web-services', 'species', 'natural history', 'taxonomists', 'biologists', 'Global Names'],
)
