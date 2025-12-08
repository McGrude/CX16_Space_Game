# Project Specification — Commander X16 Space-Trading RPG

This document defines the full multi‑phase universe generation pipeline and the data files shared between phases. It serves as the authoritative reference for how all generation stages interact.

---

# Core Universe Rules

**No Living Aliens**  
The game universe contains no living alien civilizations. All alien artifacts represent ancient, abandoned, enigmatic structures from an extinct civilization. Human expansion occurs in a universe rich with mystery but absent of active alien presence.

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

# Phase 2 — Alien Ruins & Artifacts  
**Input:** `system_objects.csv` (Phase 1)  
**Output:** `system_objects.csv` (augmented with artifact fields)

Phase 2 deterministically places ancient alien structures on eligible natural objects:

- Approximately 1.5–3% of eligible objects receive artifacts
- Only rocky planets, desert planets, ice planets, rocky moons, icy moons, and large asteroids are eligible
- Gas giants are excluded from artifact placement
- Six artifact types: ARC (relic/crystal), RUI (ruins), FAC (facility), BEA (beacon), ENG (energy node), TEC (tech cache)

The augmented **system_objects.csv** adds two fields:

```
artifact_flag     # 0 or 1
artifact_type     # ARC/RUI/FAC/BEA/ENG/TEC or empty
```

All Phase 1 fields remain intact and unmodified. Artifacts are rare, high-value locations that drive exploration, technological advancement, and later historical developments.

---

# Phase 3 — Civilization Expansion  
**Input:** `star_catalog.csv`, `system_objects.csv` (with artifacts)  
**Output:** `civilization.csv` (planned)

Phase 3 populates the universe with human activity:

- Colonies on habitable worlds
- Mining and fuel installations
- Space stations
- Corporate, political, criminal, or rogue factions
- Abandoned sites, ruins, derelicts
- Founding dates, collapse dates, and historical events

Artifact presence influences colony placement and faction interests. This phase generates the *first layer* of human lore.

---

# Phase 4 — Economy, Trade, and Missions  
**Input:** all prior CSVs  
**Output:** economic data files + mission templates

Includes:

- Commodity availability and pricing baselines
- Tech level per system (influenced by artifact access)
- Trade route hints
- Faction influence modeling
- Mission seeds tied to specific stars or objects
- Artifact-related missions (salvage, research, covert operations)

Spectral type, ore/fuel richness, habitability, and artifact presence all influence this phase.

---

# Phase 5 — Historical Timeline  
**Input:** prior data outputs  
**Output:** timeline log

A compact chronological history including:

- System founding events
- Discovery of major artifacts
- Corporate mergers or collapses
- Wars, treaties, disasters
- Technology breakthroughs (especially propulsion advances from artifact research)

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
| **system_objects.csv** | Phase 1 & 2 | Planets, moons, asteroids + resources, habitability, and artifacts |
| **civilization.csv** | Phase 3 | Colonies, stations, factions, abandoned sites |
| **economy.csv** | Phase 4 | Trade modifiers, tech levels, commodity availability |
| **timeline.txt** | Phase 5 | Complete historical log |

This specification is updated as new phases evolve and new gameplay systems are added.
