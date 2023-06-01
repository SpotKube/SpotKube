#! /bin/bash

# Create virtual environment
python3 -m venv env

. env/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload