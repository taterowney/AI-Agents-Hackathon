#!/bin/bash

python3 -m pip install --upgrade pip
python3 -m venv venv
source venv/bin/activate

# pip freeze > requirements.txt