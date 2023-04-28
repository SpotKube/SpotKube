#! /bin/bash

virtualenv env
source env/bin/activate

pip install -r requirements1.txt

python3 -m uvicorn main:app --reload