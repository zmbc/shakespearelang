set -e

poetry run python3 profile_sierpinski.py
poetry run snakeviz profilestats
