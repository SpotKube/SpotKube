#! /bin/bash

virtualenv env
source env/bin/activate

pip install -r requirements1.txt

uvicorn main:app --reload