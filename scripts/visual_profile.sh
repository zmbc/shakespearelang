#!/bin/bash

set -e

poetry run python3 scripts/profile_sierpinski.py
poetry run snakeviz profilestats
