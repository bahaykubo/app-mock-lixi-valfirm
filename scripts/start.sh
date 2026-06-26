#!/bin/sh
set -e
poetry run python -m manage runserver 0.0.0.0:8000
