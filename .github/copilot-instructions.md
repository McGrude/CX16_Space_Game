# CX16_Space_Game — Copilot instructions

Purpose: give an AI coding agent the minimal, practical context needed to be productive in this codebase.

Quick summary (what to know first)
- Repo is a multi-module BASIC game (Commander X16) split across several numbered program files in `SRC/`. Modules chain-load: MAIN → DOCKED → SPACE → COMBAT → MISSION.
- Data is data-driven: CSV files in `DATA/` provide ships, systems, ports, factions, commodities, equipment. Expect CSV parsing routines and on-demand loader patterns.
- Program state persists through `SAVES/GAMESTATE.DAT`. Modules save on exit and `RUN` the next module.
- Emulator and tools live in `EMU/`. `TOOLS/bin/basic_rem_strip.sh` cleans REM comments and normalizes numbered BASIC lines for build output.

Where to start (in order)
1. `README.md` and `DESIGN-NOTES/space-trader-design-notes.md` — high level architecture, game loops, save format, intended flow. Read these first.
2. `DATA/*` — inspect CSVs to understand fields & game data (e.g., `DATA/systems.csv`, `DATA/ships.csv`).
3. `SRC/` modules: look for `REM === START ... LIBRARY` and `REM === PUBLIC INTERFACES` blocks. Public interfaces are typically implemented as `GOSUB <nnnnn> : RETURN` and correspond to subroutines inside the module.
4. `TESTS/` — small, runnable BASIC tests (e.g., `TESTS/ERROR-MGR-TEST.BAS`) to exercise and validate modules.

Essential patterns (do not break these unless asked explicitly)
- Module boundaries: each module acts as a separate BASIC program with its own entry points; modules chain via `GOSUB SAVE_STATE` and `RUN "OTHERMODULE.BAS"`.
- Save/load pattern: `SAVE_STATE`/`LOAD_STATE` write/read `SAVES/GAMESTATE.DAT` with a fixed layout (see design notes). Keep the order & types unchanged unless migrating the save format in a backward-compatible way.
- Public interfaces: modules expose small public entry points near top via `GOSUB <sub>`+`RETURN`. Use these as the stable API for other parts of the program.
- Passing parameters: small arrays (e.g., `AN()`, `AS$()`, `WD()`) commonly carry positional parameters between code and library routines. Follow array indices used in calling sites.
- Naming conventions: variables with `%` suffix are integers, `$` suffix for strings. Error manager conventions use `ER%`, `ER$`, `EL%`, `EM$`.
- UI primitives: `LOCATE`, `PRINT`, `COLOR`, `CHR$` with `SW=80`/`SH=60` are used to produce text UI. `WINFRAME` library uses `AN()`/`AS$()` patterns to draw windows.
- Line numbers: code is numeric and arranged by number groups (e.g., 50000–50999 libraries). Do not change line numbers without renumbering the entire module and validating all GOSUB/JMP targets.

Build & test rules
- Output files in `BUILD/` are generated and gitignored. Do not commit assembled `.BAS`, `.PRG`, or `.BIN` files.
- Use `TOOLS/bin/basic_rem_strip.sh` to strip REM comments from numbered BASIC source before building final `.BAS` outputs. Typical assembly/concatenate pattern:

  ```bash
  # Example (adapt to available module filenames):
  cat SRC/common.bas SRC/docked_main.bas | TOOLS/bin/basic_rem_strip.sh > BUILD/DOCKED.BAS
  # Repeat for SPACE/COMBAT/MISSION etc.
  ```

- The repo includes an emulator in `EMU/x16emu` and SD tools (`makecart`, `sdcard.img.zip`). Check `EMU/README.pdf` for the emulator flags and how to attach the SD disk image.
- To run a unit test, generate a cleaned BASIC file and load it into the emulator; `TESTS/` includes small tests (e.g., `ERROR-MGR-TEST.BAS`) which use `GET KY$` to pause interactions.

Conventions when editing code
- Keep `REM`-block header comments: they explain public interface & side effects. The `basic_rem_strip.sh` is for build-time removal only; retain comments in `SRC/`.
- Keep public interface stubs (the `GOSUB...:RETURN : REM` lines) intact if you add subroutines to modules; they are the public API other modules call.
- When adding new code: place it inside the proper numeric-range group (e.g., 50000–50999 for libraries, 51000–51999 for UI). Add a `REM === PUBLIC INTERFACES` block near the top with a stable interface and doc comment lines.
- For functions that will be used across multiple modules, prefer `common` style (intended `COMMON.BAS`) or add to an existing shared-number range. Keep names and array argument patterns consistent.

When writing tests
- Each module should have a `TESTS/` entry that is runnable without full game state. Use a minimal `AN()` or `AS$()` config and assert expected visual and numeric outputs.
- Pause waits: `GET KY$` is used to pause test sequences — fill with `GET` loops for input-driven test flow.

Integration & external deps
- Assembly/Build: There is no canonical `Makefile` currently in repo — the design notes lay out a typical `cat`-and-build pattern. Avoid pushing built files to git.
- Emulator: Use `EMU/x16emu` to run tests; `EMU/makecart` can be used to produce a cartridge image; SD card support is used by `SAVES/` and `DATA/` lookups.
- CSV data: `CSV` files under `DATA/` are loaded on-demand; do not modify field order unless updating CSV loaders and the design-docs.

What to avoid (quick list)
- Don’t renumber lines without updating all references and testing all GOSUBs and RUN targets.
- Don’t commit generated files in `BUILD/` or `EMU/` output; they are ignored by git.
- Don’t remove or change save/load order (GAMESTATE layout) without a migration plan.

Common search targets for quick navigation
- `REM === START`, `REM === PUBLIC INTERFACES` (find module boundaries)
- `GOSUB 50`, `GOSUB 51`, `GOSUB 10` groups (API entrypoints)
- `OPEN 1,8,2,"SAVES/GAMESTATE.DAT,S,W"` and `INPUT#`/`PRINT#` (save/load implementation)
- `TOOLS/bin/basic_rem_strip.sh` (build pre-processing)

How to validate changes
- Use `TESTS/` scripts to confirm expected behavior; open with emulator.
- Validate UI by running the modules involved using `EMU/x16emu` — check `EMU/README.pdf` for options.
- If you change CSV fields or save structure, update `DESIGN-NOTES` and add migration code.

If anything’s unclear — ask a human
- Ask which modules are considered stable and which are in-progress.
- Confirm decisions to change the `GAMESTATE.DAT` layout or global variable names.

---

If you'd like, I can now:
- Add a short `Makefile` example for the repository that uses `basic_rem_strip.sh` and produces `BUILD/` outputs (recommended).
- Add a PR checklist for tests to run before merging.

Please let me know any clarifications or extra content you'd like to include in these instructions (e.g., emulator usage examples, additional tests, or a build script template).