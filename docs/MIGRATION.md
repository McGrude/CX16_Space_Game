# Repository reorganization

The reorganization preserves existing source, data, designs, and prior outputs. No simulation phase was regenerated. `reorganization-manifest.json` maps moved files and records their pre-move SHA-256 hashes.

| Previous path | New location |
|---|---|
| `SRC/`, `TESTS/` | `game/src/`, `game/tests/` |
| `DATA/` | `game/data/legacy/` |
| `OLD/`, `OUT/` | `game/archive/source/`, `game/archive/output/` |
| `UI/`, `Interfaces.graffle` | `game/ui/` |
| `DESIGN-NOTES/` (tracked as `design-notes/`) | `docs/archive/game-design/` |
| `universe_builder/notes/` | `docs/archive/universe-design/` |
| Phase 0–2 Python scripts | `universe_builder/phases/` |
| Phase 0 HYG input | `universe_builder/data/source/` |
| Phase 0–2 generated files | `universe_builder/data/baseline/phase_0/` through `phase_2/` |
| Former phase specs and launch scripts | `docs/archive/universe-design/` |
| Former phase 3 civilization specification | `docs/archive/universe-design/PHASE_3_CIVILIZATION_EXPANSION.md` |

`EMU/` remains local and ignored. Archived links and commands are preserved as historical text and may reference old paths. Current commands live in `DEVELOPMENT.md`.

## Phase numbering

Phases 0–2 keep their established meanings. The old broad civilization phase is now phase 3 scenario initialization plus phase 4 historical simulation. Economy operates inside the simulation and is exported through phases 5–6. History is recorded as events occur, not invented afterward in a separate timeline generation pass. Former references to phases 3–5 are superseded by `phases/README.md`.
