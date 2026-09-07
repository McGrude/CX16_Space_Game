# Validation record

## M0: repository organization

Scope: relocation integrity, command-line plumbing, baseline hash verification, configuration validation, and runner tests. This is not validation of the astronomical model or historical simulation.

Baseline inventory: 136 stars, 405 phase 1 objects, 405 phase 2 objects, seven artifact sites. No generation was used to replace these files during organization.

Checks completed with Python 3.9.6:

- All 53 relocated tracked files match their pre-move SHA-256 hashes.
- `python3 -m universe_builder verify-baseline`: all five source/baseline files match preserved hashes.
- `python3 -m unittest discover -s universe_builder/tests -v`: 10 runner tests passed, covering configuration, dependency wiring, provenance, overwrite protection, phase bounds, and failure records.
- Actual phase 0–2 scripts completed through the runner using a disposable two-star fixture. This confirms command wiring, not model correctness or baseline reproduction.
- Python sources compile; current documentation links resolve; `git diff --check` passes.
- Existing BASIC code and generator algorithms were preserved unchanged. No BASIC emulator validation was performed.

## M1: phases 0–2

Current status: **Phase 0 closed and accepted; Phase 1 next; Phase 2 pending.** Earlier entries below are historical validation records. See `PHASE_0_CLOSEOUT.md` for the current Phase 0 gate. M1 as a whole is not yet complete.

Known review items:

- Former phase 2 launcher misspelled `alien` as `alient`; the supported runner uses the actual implementation path.
- Former launchers required `python3.14` and a particular working directory; the runner uses the active interpreter and resolved paths.
- Earlier specifications and command defaults disagree on star radius/count; launch configuration uses radius 25 ly, maximum 300 candidates, and scale 0.5 ly/cell.
- Phase 2 code includes the seed in the hash key; an archived specification omits it.
- Projected coordinates do not encode true 3D pairwise distances.
- Existing implementation input validation and edge cases remain to be audited.

Record commands, interpreter, inputs, outcomes, and any baseline differences here when validation is performed. Preserve failure evidence and do not mark an implementation valid from syntax checks alone.

## Phase 0 reachability design analysis

Read-only analysis has matched all 136 preserved entries uniquely to HYG coordinates and calculated 3D distance graphs. No radius can retain all entries with both full connectivity and a six-neighbor cap. With user-permitted system pruning, a deterministic heuristic sweep found a valid 108-system subset at 9.4 ly. See `analysis/phase-0-reachability.md` and its JSON for method, limitations, candidate identities, and statistics.

All 20 current unit tests pass, including graph-boundary/connectivity and pruning checks; baseline/source hashes are unchanged. This design analysis does not complete M1 or adopt a new production catalog.

## Phase 0 display preservation and named preference

Implemented selection preference for catalog names and non-pruning display placement. A disposable real-source Phase 0 run produced 167 entries in unique cells, with Sol first, instead of deleting colliding entries. Physical coordinates stay unchanged through projection. All 26 tests pass; baseline hashes remain unchanged. `analysis/phase-0-current-candidates.md` records the separate current-pool reachability experiment. Fixed reach and multiple-star grouping remain design decisions, and full M1 is incomplete.

## Grouped Phase 0 rule application

Schema 2 now groups catalog systems, retains source identities/member records, applies named-preferred fixed-distance pruning, and exports physical routes and display positions. `analysis/phase-0-grouped-results.md` summarizes 99 destinations at 9.0 ly with all named systems preserved.

37 tests pass. Two independent runs produced identical bytes for all six phase-output files. A separate CSV/JSON audit verified route completeness, 1–6 degree bounds, Sol connectivity, unique members, Alpha Centauri grouping, display uniqueness, and output hashes. Baseline/source hashes remain unchanged. Three retained groups have source astrometry discrepancy flags; one unselected secondary has incomplete catalog linkage. Full M1 source-quality and downstream validation are still pending.

## Phase 0 closeout — accepted v1

Closed for the agreed game-generation scope on user request. The accepted dataset is `universe_builder/results/grouped-phase0-v1/`. The fixed result is 99 destinations, 127 cataloged components, 188 routes, 9.0 ly reach, one connected graph, degrees 1–6, all 30 named destinations and 34 named member labels retained.

- Reusable artifact validator: passed (`python3 -m universe_builder.validation.phase0 universe_builder/results/grouped-phase0-v1`).
- Test suite: 41 passed, including checksum, omitted-edge, and duplicate-member corruption detection.
- Reproduction: prior two-run comparison produced byte-identical six-file Phase 0 outputs; no generator/config/input changes since that comparison.
- Source, override and generator implementation hashes: still match accepted manifest.
- Historical source/baseline hashes: unchanged.
- Whitespace and current documentation links: checked.

Three retained catalog association/astrometry discrepancies and one excluded incomplete secondary linkage are recorded limitations. Primary-coordinate travel, catalog-limited member completeness, heuristic pruning, and sparse offline IDs are explicit conventions. These do not block the agreed game dataset; orbital realism, new association evidence, or source upgrades require a future revision.

Phase 1 review/validation is next. Do not claim all of M1 complete or reuse historical object/artifact rows with the new IDs.

## Phase 0 cube v2

User-authorized cube revision: 170 destinations / 210 members, fixed 9 ly reach, 321 routes, one component and 1–6 neighbors. Independent artifact validation passed; 46 tests passed; all six outputs match a second generation byte-for-byte. Spherical v1 and source/baseline hashes remain preserved. See [cube results](analysis/phase-0-cube-results.md) for names, quality flags and reproduction. Phase 1 trial remains on v1.

## Phase 1 local-coordinate correction

Cube Phase 1 v3 contains the same 274 Spobs as v2, with only three moon coordinates moved one cell each. No duplicate local cells remain. All other CSV fields match v2. All 48 tests pass, including parent priority, deterministic tie ordering, input-order independence, idempotence and map-edge collisions. A fresh run matches CSV, summary and manifest bytes. Full Phase 1 acceptance remains open.

## Phase 1 production acceptance

See [Phase 1 closeout](PHASE_1_CLOSEOUT.md). All 55 tests passed; independent Phase 1 artifact validation passed; production output equals corrected trial v3; all seven Phase 0/1 outputs match independent replay. Cube Phase 0 data and five preserved source/baseline files remain unchanged. Phase 2 is next.
