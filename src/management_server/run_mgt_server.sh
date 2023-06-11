#! /bin/bash

# Create virtual environment
python3 -m venv env

source env/bin/activate

# which python3
python3 -m pip install prophet

pip install -r requirements.txt

uvicorn main:app --reload