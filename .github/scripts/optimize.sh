#!/usr/bin/env bash

# exit when any command fails
set -e

isort .
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r ./pdfconduit
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r ./tests
black pdfconduit
black tests