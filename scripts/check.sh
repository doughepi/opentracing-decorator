#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="opentracing_decorator tests"

set -x

${PREFIX}black --check --diff -l 120 $SOURCE_FILES
${PREFIX}flake8 $SOURCE_FILES
${PREFIX}mypy $SOURCE_FILES
${PREFIX}isort --check --diff --project=opentracing_decorator $SOURCE_FILES