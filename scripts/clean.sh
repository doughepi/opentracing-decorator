#!/bin/sh -e

if [ -d 'dist' ] ; then
    rm -r dist
fi
if [ -d 'site' ] ; then
    rm -r site
fi
if [ -d 'htmlcov' ] ; then
    rm -r htmlcov
fi
if [ -d 'opentracing_decorator.egg-info' ] ; then
    rm -r opentracing_decorator.egg-info
fi