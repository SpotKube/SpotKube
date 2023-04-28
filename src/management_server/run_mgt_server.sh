#! /bin/bash

python3 -m venv env

pip install -r requirements.txt

python3 -m uvicorn main:app --reload

