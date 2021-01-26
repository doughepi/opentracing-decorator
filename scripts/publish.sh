#!/bin/sh -e

VERSION_FILE="opentracing_decorator/__version__.py"

if [ -d 'venv' ] ; then
    PREFIX="venv/bin/"
else
    PREFIX=""
fi

if [ ! -z "$GITHUB_ACTIONS" ]; then
  git config --local user.email "doughertypiper@gmail.com"
  git config --local user.name "Piper Dougherty"

  VERSION=`grep __version__ ${VERSION_FILE} | grep -o '[0-9][^"]*'`

  if [ "refs/tags/${VERSION}" != "${GITHUB_REF}" ] ; then
    echo "GitHub Ref '${GITHUB_REF}' did not match package version '${VERSION}'"
    exit 1
  fi
fi

set -x

${PREFIX}twine upload dist/*
${PREFIX}mkdocs gh-deploy --force