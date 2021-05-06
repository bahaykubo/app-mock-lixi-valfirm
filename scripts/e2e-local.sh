#!/bin/sh
set -eux
timeout 20 bash -c \
    'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' http://localhost:8000)" != "404" ]]; do sleep 1; done'
appenv=local pipenv run python -m unittest discover -s test/e2e
