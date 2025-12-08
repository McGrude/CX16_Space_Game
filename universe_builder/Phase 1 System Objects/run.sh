#!/usr/bin/env bash

python3.14 generate_system_objects.py --input-stars ../0_star_systems/star_catalog.csv --output-objects system_objects.csv --max-objects-per-system 5 --seed 42
