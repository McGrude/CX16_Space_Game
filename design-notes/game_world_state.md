# Game World State Summary

## Core Timekeeping
- **DA%** — Elapsed in-game days since the start of the game.
- No time-of-day tracking.

## Player Location
- **SY%** — Current star system ID.
- **LO%** — Current location within the current star system (planet, station, orbit, deep space, etc.).

## Randomness
- **RS%** — RNG seed used for deterministic behavior across save/load.

## Global Events
- **EV%(0..15)** — Array of global event flags.
  - Placeholder until mission and story systems are fully defined.

## Notes
- No global economic index. Economy is defined at the faction and system level.
- No global political index. Faction reputations and relationships appear in the faction model.
