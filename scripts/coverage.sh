#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="opentracing_decorator tests"

set -x

${PREFIX}coverage report --show-missing --skip-covered --fail-under=90