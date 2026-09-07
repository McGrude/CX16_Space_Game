# Development guide

## Python universe generator

Use Python 3.9+ from the repository root. No package installation is required.

```sh
python3 -m universe_builder list
python3 -m universe_builder verify-baseline
python3 -m unittest discover -s universe_builder/tests -v
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems.json --output /tmp/cx16-world-001 --through 0
```

`generate` requires a new output directory and runs the implemented dependency chain, phases 0–2. Use `--through 0` or `--through 1` for earlier stopping points. Paths in configuration are resolved relative to that configuration file. Copy the configuration and adjust its source path when moving it elsewhere. Seeds and settings are explicit; no original dataset is overwritten.

Each run records its configuration, Python version, input hashes, implementation hashes, output hashes, and completion status in `manifest.json`. A failed run retains its manifest and partial outputs for diagnosis; retry in a new directory. A manifest establishes provenance, not correctness or cross-version reproducibility.

Baseline verification checks that files match preserved SHA-256 hashes. Full phase validation is a separate milestone. The baseline settings were recovered from the old shell scripts, not proven as the exact provenance of the saved CSVs. Phase 0 has since changed to preserve map collisions and prefer catalog names, so its revised output intentionally differs from the historical baseline.

## BASIC game

- `game/src/`: numbered BASIC libraries and screen prototype; symbolic date-library experiments.
- `game/tests/`: small manual BASIC tests.
- `game/data/legacy/`: early game tables; not connected to the new generator.
- `game/ui/Interfaces.graffle`: interface design.
- `game/archive/`: prior source and generated output retained for reference.

No supported end-to-end game build is supplied. `DATE-STR-LIB.BAS` and its symbolic test need a preprocessor that is absent. The numbered main program references separately stored window routines and is not a standalone complete game. The optional ignored `EMU/` directory remains in place for local emulator use. Do not infer an emulator test passed from a source check.

## Working conventions

See `AGENTS.md`. Keep new experiment output outside source/baseline paths, use explicit configuration, and update current docs as contracts evolve. See `docs/MIGRATION.md` for old paths. Archived launch scripts are historical records and no longer supported commands.

## Grouped Phase 0

Schema 2 groups HYG components, applies sourced overrides, evaluates fixed-reach pruning, and preserves member stars and physical positions. The checked-in `universe_builder/results/grouped-phase0-v1/` is a reviewed generation artifact, separate from the historical baseline. Its manifest records every output hash. Use the command above with a new output path to reproduce it. `baseline.json` remains schema 1 legacy mode.

Grouped IDs are primary HYG IDs and therefore sparse. Do not join the new catalog to old object/artifact files. New downstream runs can consume the leading catalog columns, but phase 1 still models natural objects from the primary spectral type; member-star orbital generation remains future work.

Phase 0 is closed at accepted v1. Validate the handoff without regeneration using:

```sh
python3 -m universe_builder.validation.phase0 universe_builder/results/grouped-phase0-v1
```

See `PHASE_0_CLOSEOUT.md` for documented limitations and the Phase 1 input contract.
