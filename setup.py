#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    version = Path(package, "__version__.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", version).group(1)


def get_long_description():
    """
    Return the README.
    """
    long_description = ""
    with open("README.md", encoding="utf8") as f:
        long_description += f.read()
    long_description += "\n\n"
    with open("CHANGELOG.md", encoding="utf8") as f:
        long_description += f.read()
    return long_description


setup(
    name="opentracing-decorator",
    python_requires=">=3.7",
    version=get_version("opentracing_decorator"),
    url="https://github.com/doughepi/opentracing-decorator",
    project_urls={
        "Documentation": "https://doughepi.github.io/opentracing-decorator/",
        "Source": "https://github.com/doughepi/opentracing-decorator",
    },
    description="A Python decorator for OpenTracing trace generation.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Piper Dougherty",
    author_email="doughertypiper@gmail.com",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    package_data={"opentracing_decorator": ["py.typed"]},
    license="MIT",
    keywords="tracing, opentracing, decorator",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["opentracing>=2.4.0,<3.0", "flatten-dict==0.3.0"],
    test_suite="tests",
    extras_require={"tests": []},
    zip_safe=False,
)
