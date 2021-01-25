#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from setuptools import setup, find_packages

version = None
with open("opentracing_decorator/__init__.py", "r") as f:
    for line in f:
        m = re.match(r'^__version__\s*=\s*(["\'])([^"\']+)\1', line)
        if m:
            version = m.group(2)
            break

assert (
    version is not None
), "Could not determine version number from opentracing_decorator/__init__.py."

setup(
    name="opentracing-decorator",
    version=version,
    url="https://github.com/doughepi/opentracing-decorator",
    description="A Python decorator for OpenTracing trace generation.",
    author="Piper Dougherty",
    author_email="doughertypiper@gmail.com",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT License",
    keywords="tracing, opentracing, decorator",
    classifiers=[],
    install_requires=["opentracing>=2.4.0,<3.0", "flatten-dict==0.3.0"],
    test_suite="tests",
    extras_require={"tests": []},
)
