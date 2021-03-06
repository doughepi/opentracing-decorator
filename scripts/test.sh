#!/bin/sh

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -ex

if [ -z $GITHUB_ACTIONS ]; then
    scripts/check.sh
fi

${PREFIX}coverage run -m pytest

if [ -z $GITHUB_ACTIONS ]; then
    scripts/coverage.sh
fi