#! /bin/bash

# Create virtual environment
python3 -m venv env

source env/bin/activate

# which python3

pip install -r requirements.txt

uvicorn main:app --reload