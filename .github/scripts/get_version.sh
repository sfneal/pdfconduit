#!/usr/bin/env bash

# exit when any command fails
set -e

python - << EOF
import os
with open(os.path.join(os.path.dirname(__file__), 'pdfconduit', '_version.py'), 'rb') as fp:
    print(fp.read().decode('utf8').split('=')[1].strip(" \n'").replace('"', ''))

EOF