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

Status: not yet performed. Follow `ROADMAP.md` before phase 3 implementation.

Known review items:

- Former phase 2 launcher misspelled `alien` as `alient`; the supported runner uses the actual implementation path.
- Former launchers required `python3.14` and a particular working directory; the runner uses the active interpreter and resolved paths.
- Earlier specifications and command defaults disagree on star radius/count; launch configuration uses radius 25 ly, maximum 300 candidates, and scale 0.5 ly/cell.
- Phase 2 code includes the seed in the hash key; an archived specification omits it.
- Projected coordinates do not encode true 3D pairwise distances.
- Existing implementation input validation and edge cases remain to be audited.

Record commands, interpreter, inputs, outcomes, and any baseline differences here when validation is performed. Preserve failure evidence and do not mark an implementation valid from syntax checks alone.
