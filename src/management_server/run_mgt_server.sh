#! /bin/bash

virtualenv env
source env/bin/activate

pip install -r requirements.txt

mkdir -p logs
uvicorn main:app --reload