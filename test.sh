#!/usr/bin/env zsh
set -euo pipefail
export COLOR_GREEN='\e[0;32m'
export COLOR_NC='\e[0m' # No Color

echo "Run black"
poetry run black .

echo "Run isort"
poetry run isort .

#echo "Run mypy"
#poetry run mypy .
#
#echo "Run tests"
#python manage.py test

echo "${COLOR_GREEN}You are good to go!${COLOR_NC}"