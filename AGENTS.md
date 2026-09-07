# Repository guidance

## Purpose and authority

Build a Commander X16 BASIC space RPG and an offline deterministic Python history/world generator. Read `docs/PROJECT.md`, `docs/ROADMAP.md`, and the relevant `docs/phases/` contract before implementation. Current user instructions take precedence. `docs/archive/` contains historical context, not active instructions or settled requirements. `.github/copilot-instructions.md` points here.

## Scope and workflow

- Phases 0–1 are accepted for the current scope. Read `docs/PHASE_1_CLOSEOUT.md`; current standard output is `universe_builder/results/physical-phase1-v1/`. Phase 2 discussion and validation is next. Preserve all previous artifacts; do not silently regenerate or migrate them. Phase 3 follows M1.
- Future phase documents are specifications, not claims of working code. Do not fabricate implementations, outputs, test results, or completion statuses.
- Ask about material simulation choices when they become necessary; record decisions in `docs/DECISIONS.md`. Resolve routine engineering choices independently.
- Keep changes reviewable; do not commit, push, publish, or send messages unless requested.
- No agent delegation is required by this file.

## Data and reproducibility

- Preserve `universe_builder/results/grouped-phase0-v1/` and the new `universe_builder/results/grouped-phase0-cube-v2/`. Existing Phase 1 trials reference v1; migrate through a new run when proceeding with v2. Preserve `universe_builder/data/baseline/` and the HYG source. Never regenerate or replace them without an explicit request. Experiments go into a new output directory.
- Use `configs/grouped_systems_cube.json` (schema 2) for current cube rules; `grouped_systems.json` preserves the sphere configuration. `baseline.json` is legacy single-entry mode. Grouping uses catalog links plus sourced overrides, never proximity. Sparse primary HYG IDs are offline identities; compact runtime indices are a later export concern.
- Preserve system IDs and composite object identities `(system_id, object_id)`. Older `game/data/legacy/` files use a different ID space and schema; do not join them to generated data without a migration.
- Use stable seeds, sorted iteration, explicit configuration, versioned schemas, and recorded input hashes. Do not use Python's process-randomized `hash()` for seeds.
- Distinguish simulation truth from an actor's knowledge. Hidden artifacts and discoveries must not influence decisions before information arrives.
- Record causes and participants for historical events. Never silently invent unknown dates, cultures, or generation provenance.

## Python

- Python 3.9+ and standard library for now. Use `python3 -m universe_builder` as the supported entry point.
- New generation runs must not overwrite existing directories. Record config, interpreter version, input/output hashes, and implementation hashes with outputs.
- Add meaningful tests for behavior changes. Run `python3 -m unittest discover -s universe_builder/tests -v`; use targeted validation before broader seed sweeps.
- Update phase contracts when changing schemas or semantics. Keep simulation decisions separate from presentation/export.

## BASIC

- Runtime code is in `game/src/`; tests in `game/tests/`. Target Commander X16, not generic modern BASIC.
- Preserve numbered public entry points and positional `AN()`/`AS$()` calling conventions unless deliberately migrating callers.
- The symbolic `DATE-STR-*` sources require a preprocessor that is not currently supplied. Do not claim all `.BAS` files can run directly.
- No complete chain-loading runtime, CSV loader, save system, or canonical game build exists yet. Archived documents describe intent.
- Verify runtime changes in the emulator where available; distinguish source inspection from execution.

## Documentation and licensing

- Maintain one current specification and roadmap; mark superseded materials as archives.
- Retain the MIT license and attribution. Third-party catalog data, ROMs, emulator binaries, and manuals are not relicensed as project code.
- Report what changed, what was checked, and remaining limitations. Do not mark phase validation complete from syntax checks alone.
