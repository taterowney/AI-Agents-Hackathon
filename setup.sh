#!/bin/bash

#python3 -m pip3.9 install --upgrade pip
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# pip freeze > requirements.txt