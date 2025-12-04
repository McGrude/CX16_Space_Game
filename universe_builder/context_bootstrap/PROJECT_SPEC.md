# Project Specification — Commander X16 Space-Trading RPG

This document defines the full multi‑phase universe generation pipeline and the data files shared between phases. It serves as the authoritative reference for how all generation stages interact.

---

# Phase 0 — Star System Generation  
**Output:** `star_catalog.csv`, `star_map.txt`

Phase 0 constructs the astronomical scaffold of the game universe:

- Selects ~80–150 nearby stars from the HYG catalog.
- Projects them into a deterministic 2D grid for the starmap.
- Removes collisions using brightness/name priority rules.
- Forces Sol (system_id 0) to exist and to sit at the grid center.
- Produces:
  - **star_catalog.csv** with columns:

    ```
    id, proper, dist_ly, grid_x, grid_y, spect
    ```

  - **star_map.txt** ASCII representation of the 100×100 starmap.

This file is the backbone for all later phases.

---

# Phase 1 — Natural Space Object Generation  
**Input:** `star_catalog.csv`  
**Output:** `system_objects.csv`

Phase 1 deterministically generates the natural celestial bodies for each star:

- 0–5 *primary* objects per system (planets + optional large asteroid)
- Moons for eligible primaries
- Fully deterministic seeding per system
- Special-case Sol with fixed Earth/Luna/Mars/Ceres

The output file **system_objects.csv** contains:

```
system_id
object_id
name
class
parent_object_id
is_moon
local_x
local_y
ore_richness
fuel_richness
habitability
risk
```

These values are pure data and contain no gameplay logic. Later phases build on top of them.

---

# Phase 2 — Civilization Expansion  
**Input:** `star_catalog.csv`, `system_objects.csv`  
**Output:** `civilization.csv` (planned)

Phase 2 populates the universe with human activity:

- Colonies on habitable worlds
- Mining and fuel installations
- Space stations
- Corporate, political, criminal, or rogue factions
- Abandoned sites, ruins, derelicts
- Founding dates, collapse dates, and historical events

This phase generates the *first layer* of lore.

---

# Phase 3 — Economy, Trade, and Missions  
**Input:** all prior CSVs  
**Output:** economic data files + mission templates

Includes:

- Commodity availability and pricing baselines
- Tech level per system
- Trade route hints
- Faction influence modeling
- Mission seeds tied to specific stars or objects

Spectral type, ore/fuel richness, and habitability may all influence this phase.

---

# Phase 4 — Historical Timeline  
**Input:** prior data outputs  
**Output:** timeline log

A compact chronological history including:

- System founding events
- Corporate mergers or collapses
- Wars, treaties, disasters
- Technology breakthroughs

Recorded as:

```
YYYY‑MM‑DD: event text...
```

---

# Data File Summary

| File | Source | Description |
|------|--------|-------------|
| **star_catalog.csv** | Phase 0 | Star list, names, positions, spectral types |
| **star_map.txt** | Phase 0 | ASCII 2D map of inhabited region |
| **system_objects.csv** | Phase 1 | Planets, moons, asteroids + resources & habitability |
| **civilization.csv** | Phase 2 | Colonies, stations, factions, abandoned sites |
| **economy.csv** | Phase 3 | Trade modifiers, tech levels, commodity availability |
| **timeline.txt** | Phase 4 | Complete historical log |

This specification is updated as new phases evolve and new gameplay systems are added.
