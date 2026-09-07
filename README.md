# Commander X16 Space Game

A space trading, exploration, and turn-based ship-command RPG for the Commander X16, supported by an offline Python universe generator.

The generator starts humanity at the dawn of slow interstellar travel. Earth-based powers explore, settle, research, cooperate, fragment, merge, and disappear. The player enters the resulting world after its history has unfolded. Culture, language, and naming preserve traces of that history.

## Current state

The BASIC runtime is an early UI and utility prototype, not a playable game. Universe phases 0–2 have Python implementations and preserved outputs; their full validation is the next milestone. Historical simulation and game export are planned, not implemented.

## Start here

- [Project specification](docs/PROJECT.md): accepted direction and architecture.
- [Milestone roadmap](docs/ROADMAP.md): sequence, status, and completion criteria.
- [Generation phases](docs/phases/README.md): contracts for implemented and planned stages.
- [Development guide](docs/DEVELOPMENT.md): commands and verification.
- [Decisions](docs/DECISIONS.md): agreed principles and questions for future milestones.
- [Repository guidance](AGENTS.md): instructions for contributors and coding agents.

## Layout

```text
game/                  BASIC source, tests, UI design, older game data
universe_builder/      Python phase implementations, configuration, baseline data
docs/                  Current specifications, roadmap, archived design material
EMU/                   Optional local emulator files (ignored; not distributed)
```

## Quick start

Python 3.9+; the current generator uses only the standard library. Run from the repository root:

```sh
python3 -m universe_builder list
python3 -m universe_builder verify-baseline
python3 -m unittest discover -s universe_builder/tests -v
```

To generate a separate experimental world from the existing scripts:

```sh
python3 -m universe_builder generate --config universe_builder/configs/baseline.json --output /tmp/cx16-world-001
```

The output directory must not already exist. This command runs only phases 0–2 and never replaces the preserved baseline. The configuration records the former launch-script settings; exact reproduction of the saved outputs has not yet been established.

Project code is under the existing [MIT license](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for external data and local tools.
