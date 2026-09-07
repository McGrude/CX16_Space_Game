# Offline universe generator

Implemented algorithms are in `phases/`; current contracts are in `../docs/phases/`. The supported command is `python3 -m universe_builder` from the repository root. Python 3.9+; standard library only.

`configs/baseline.json` records former launcher settings. `data/source/` holds the HYG input. `data/baseline/` preserves existing outputs for the next validation milestone. New generation always targets a fresh output directory.

Phases 3–6 are planned and deliberately have no placeholder generator that pretends to produce valid data. Use `list` to see status, and the roadmap to determine the next implementation task.
