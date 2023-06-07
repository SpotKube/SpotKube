#!/bin/bash

set -e 

# Create virtual environment
python3 -m venv env

. env/bin/activate

pip install -r requirements.txt
