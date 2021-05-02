#!/bin/sh
set -e
appenv=local pipenv run python -m unittest discover -s test/e2e