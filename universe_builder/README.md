# Offline universe generator

Implemented algorithms are in `phases/`; current contracts are in `../docs/phases/`. The supported command is `python3 -m universe_builder` from the repository root. Python 3.9+; standard library only.

`configs/baseline.json` records former launcher settings. `data/source/` holds the HYG input. `data/baseline/` preserves existing outputs for the next validation milestone. New generation always targets a fresh output directory.

Phases 3–6 are planned and deliberately have no placeholder generator that pretends to produce valid data. Use `list` to see status, and the roadmap to determine the next implementation task.

Current Phase 0 uses `configs/grouped_systems.json` (schema 2) for grouping, name preference, fixed reach pruning and full membership/route outputs. See `../docs/analysis/phase-0-grouped-results.md` and the preserved reviewed output in `results/grouped-phase0-v1/`. `configs/baseline.json` is legacy single-entry mode; do not use it to reproduce the new rules.

## Compact runtime identity export

```sh
python3 -m universe_builder export-runtime --phase0 universe_builder/results/grouped-phase0-cube-v2 --phase1 universe_builder/results/phase1-cube-v3 --output /tmp/new-runtime-world
```

Exports byte indexes, source mappings, translated diagnostic CSVs, packed neighbor/Spob-reference tables, and world-version metadata. Output must be a new directory. See the Phase 6 contract for the binary layouts and future save compatibility rule. This is a physical-world subset, not a complete playable export.

## Accepted Phase 1 production run

The main generator now uses the curated total-body model (moons included in the cap), with explicit weights in `configs/grouped_systems_cube.json`. Accepted output: `results/physical-phase1-v1/`. Generate with `python3 -m universe_builder generate --config universe_builder/configs/grouped_systems_cube.json --output /tmp/new-world --through 1`; validate with `python3 -m universe_builder.validation.phase1 universe_builder/results/physical-phase1-v1`. See `docs/PHASE_1_CLOSEOUT.md`.
