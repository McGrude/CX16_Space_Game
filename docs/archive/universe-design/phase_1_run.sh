#!/usr/bin/env bash

python3.14 phase_1_system_objects.py --input-stars ../phase_0_star_catalog/star_catalog.csv --output-objects system_objects.csv --max-objects-per-system 5 --seed 42
