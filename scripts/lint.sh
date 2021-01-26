#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi
export SOURCE_FILES="opentracing_decorator tests"

set -x

${PREFIX}autoflake --in-place --recursive $SOURCE_FILES
${PREFIX}isort --project=opentracing_decorator $SOURCE_FILES
${PREFIX}black --target-version=py36 $SOURCE_FILES