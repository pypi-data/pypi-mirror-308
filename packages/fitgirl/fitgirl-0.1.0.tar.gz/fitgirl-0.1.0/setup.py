from __future__ import annotations
from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()


setup(
    name="fitgirl",
    version="0.1.0",
    description="A small stack of functions that might help to scrap the most popular gaming website, fitgirl-repacks.",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Parth Mishra",
    author_email="halfstackpgr@gmail.com",
    maintainer="Parth Mishra",
    maintainer_email="halfstackpgr@gmail.com",
    url="https://www.github.com/halfstackpgr/fitgirl",
    packages=find_namespace_packages(include=["fitgirl*"]),
    install_requires=["httpx", "bs4"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
)