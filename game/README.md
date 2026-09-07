# Commander X16 runtime

An early BASIC prototype for the eventual space RPG. See `../docs/DEVELOPMENT.md` for current limitations.

`src/` contains window frames, date conversion, error handling, and a ship-status layout. `tests/` contains manual BASIC test programs. `ui/` contains the interface design. `data/legacy/` retains an older 92-system game dataset with different identifiers and schemas from the universe builder; it is not current generated world data. `archive/` preserves older source/output.

A complete game build, world loader, save/load implementation, and playable loop remain future milestones. Do not mix symbolic preprocessor source with numbered BASIC without a supported build step.
