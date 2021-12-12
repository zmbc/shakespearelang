#!/bin/bash

poetry run tatsu shakespearelang/shakespeare.ebnf -m shakespeare -o shakespearelang/_parser.py
poetry run black shakespearelang/_parser.py
