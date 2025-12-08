#!/usr/bin/env bash

python3.14 build_star_database.py --input-csv ./hygdata_v42.csv --radius-ly 25 --max-stars 300 --scale 0.5 --csv-out star_catalog.csv --map-out star_map.txt
