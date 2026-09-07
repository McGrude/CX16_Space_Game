# Natural Space Object Generator — Specification & Documentation

This document defines the specifications, inputs, outputs, rules, and behavior of the **Natural Space Object Generator**, the second stage in the universe-generation pipeline for the Commander X16 space‑trading RPG.

This stage produces **natural celestial bodies** for each star system: planets, moons, and a single asteroid class, and decorates them with game-facing attributes.

---

## Overview

The Natural Space Object Generator:

1. Reads the **star_catalog.csv** file produced by the Star Map Generator (Phase 0).
2. For each system, deterministically generates between **0 and 5 primary natural objects** (planets and at most one large asteroid), except for Sol (ID 0), which is **fixed**.
3. Uses weighted probability distributions to create planet types and their moons.
4. Produces a second CSV file: **system_objects.csv**.
5. Uses deterministic seeding so all systems are stable and reproducible.
6. Adds game attributes for each object:
   - **Ore richness** (0–3)
   - **Fuel richness** (0–3)
   - **Habitability** (0–100)
   - **Risk** (0–100)
   - **Local map coordinates** (50×50 per-system grid)

This phase lays the astrophysical and resource foundation before Phase 2 adds alien artifacts, and before Phase 3's **civilization expansion** generator adds inhabited worlds, space stations, industrial sites, and human/civil names.

---

## Input Requirements

### Input file: `star_catalog.csv`

This file is produced by the Star Map Generator. Required columns:

```text
id, proper, spect
```

- **id** = system ID (integer, unique)
- **proper** = system name (real or synthetic)
- **spect** = stellar spectral type string (e.g. `G2V`, `K5III`, `M5Ve`)

All other `star_catalog.csv` columns (e.g. `dist_ly`, `grid_x`, `grid_y`) are ignored by this script.

---

## Output File: `system_objects.csv`

A CSV containing all natural objects across all star systems.

### Schema

```text
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

Meaning:

| Field | Description |
|-------|-------------|
| **system_id** | ID of the star system (matches `star_catalog.csv.id`) |
| **object_id** | Index of object within the system (0–N) |
| **name** | Generated natural object name |
| **class** | Object type code (RP, DP, IC, GG, RM, IM, AS) |
| **parent_object_id** | Index of parent planet for moons; blank otherwise |
| **is_moon** | 1 if moon, 0 otherwise |
| **local_x** | X coordinate (0–49) on the local 50×50 system map |
| **local_y** | Y coordinate (0–49) on the local 50×50 system map |
| **ore_richness** | 0–3 ore richness (0 = none, 3 = rich) |
| **fuel_richness** | 0–3 fuel richness (0 = none, 3 = rich) |
| **habitability** | 0–100 habitability score (higher is better) |
| **risk** | 0–100 environmental risk score (higher is more dangerous) |

Example:

```text
system_id,object_id,name,class,parent_object_id,is_moon,local_x,local_y,ore_richness,fuel_richness,habitability,risk
3,0,Helion Sector-17 I,RP,,0,30,22,2,1,68,45
3,1,Helion Sector-17 I-a,RM,0,1,31,22,3,1,55,52
3,2,Helion Sector-17 II,IC,,0,38,29,1,2,40,48
3,3,Helion Sector-17 Asteroid,AS,,0,42,35,3,0,25,60
```

---

## Sol System Special Case

System ID **0** is always Sol.

It always produces exactly four objects:

1. **0: Earth (RP)**  
2. **1: Luna (RM)** — moon of Earth  
3. **2: Mars (RP)**  
4. **3: Ceres (AS)**  

Rules:

- No randomization.  
- No naming changes.  
- No gas giants, outer planets, or belts are included.  
- All four objects still receive deterministically generated:
  - `local_x`, `local_y`
  - `ore_richness`, `fuel_richness`
  - `habitability`, `risk`

Civilization expansion may later rename or repurpose these objects.

---

## Natural Object Classes

The minimal taxonomy is intentionally simple and game‑friendly:

### Planets
- **RP** — Rocky Planet  
- **DP** — Desert Planet  
- **IC** — Ice Planet  
- **GG** — Gas Giant  

### Moons
- **RM** — Rocky Moon  
- **IM** — Icy Moon  

### Asteroids
- **AS** — Large Asteroid  

This is enough diversity for gameplay without overwhelming memory or complexity.

---

## Object Count Distribution (Primaries)

Each non-Sol system receives **0–5 primary natural objects** (planets and at most one large asteroid), chosen with:

| Primary Objects | Chance |
|-----------------|--------|
| 0 | 10% |
| 1 | 25% |
| 2 | 30% |
| 3 | 20% |
| 4 | 10% |
| 5 | 5%  |

These are **primary** objects only; **moons are generated on top of this count** according to the moon rules below.

The maximum number of primaries can be clamped at the command line via `--max-objects-per-system`.

---

## Planet Type Probability

Primary objects (before the asteroid replacement step) follow:

| Class | Probability |
|-------|-------------|
| RP | 60% |
| DP | 15% |
| IC | 15% |
| GG | 10% |

If a system has **two or more** primary objects, one may be replaced with a **Large Asteroid (AS)** with a 20% probability. This replacement ensures there is at most **one asteroid** per system (aside from Ceres in Sol).

---

## Moon Generation Rules

Only planets (RP, DP, IC, GG) may receive moons.

Maximum moons per class:

| Planet Type | Max Moons |
|-------------|-----------|
| RP | 1 |
| DP | 1 |
| IC | 1 |
| GG | 3 |

Moon **counts** per planet are chosen stochastically but deterministically:

- For **GG** (gas giants): 0–3 moons with a bias toward 1–2.  
- For **RP/DP/IC** (non-giant planets): 0 or 1 moon with roughly equal chance.

Moon type probabilities:

### For rocky parents (RP, DP, IC)
- **RM**: 70%  
- **IM**: 30%

### For gas giants (GG)
- **RM**: 50%  
- **IM**: 50%

Moon names are generated by appending:

```text
SystemName I-a
SystemName II-b
```

etc.

---

## Naming Rules

Names are based on the **system name** and the **ordering of primary objects**.

Primary objects use Roman numerals (except asteroids):

```text
Helion Sector-17 I
Helion Sector-17 II
Helion Sector-17 III
Helion Sector-17 Asteroid
```

Moons use alphabetical suffixes:

```text
Helion Sector-17 I-a
Helion Sector-17 I-b
```

Asteroids always end with the word `Asteroid` and do not receive a Roman numeral.

Sol is the only system where all four object names are fully fixed and bypass the generic naming rules.

---

## Local 50×50 System Map

Each system has a **local 2D map** of size **50×50** cells. The central star is *not rendered* on this map, but all natural objects are positioned on it.

- Grid coordinates:
  - `local_x`: 0–49 (left to right)
  - `local_y`: 0–49 (top to bottom)
- Conceptual star position is at the center: `(25, 25)`.

### Primary Objects

Primary objects (planets and asteroid) are placed on **concentric orbits** around the center:

- Orbit radii (in tiles): `[5, 8, 11, 14, 17, 20]`.
- The first primary uses the smallest radius, the second the next, and so on (clamped to the last radius if there are more primaries than radii).
- The angular position of each primary on its orbit is chosen deterministically via a hash of `(system_id, primary_index)`.

### Moons

Moons are placed **near their parent planet**:

- Start at the parent’s `(local_x, local_y)`.
- Apply a small deterministic offset (−1 to +2 tiles in both X and Y) based on a hash of `(system_id, object_id)`.
- Clamp the result to stay within the 0–49 map bounds.

This yields a consistent but slightly “noisy” layout where:

- Orbits are recognizable.
- Moons visibly cluster around their parents.
- No runtime randomness is needed in the game engine.

---

## Ore and Fuel Richness

Two resources can be scanned and collected later in gameplay:

- **Ore** — mined from rocky bodies and asteroids.
- **Fuel** — harvested from gas giants and, to a lesser extent, other bodies (e.g. trapped volatiles, He‑3).

Both are encoded as integer richness tiers:

- `0` = none / negligible  
- `1` = poor  
- `2` = normal  
- `3` = rich  

### Deterministic assignment

For each object, richness values are computed from:

- `system_id`
- `object_id`
- object `class`
- (indirectly) the star’s spectral type for flavor in other attributes

A 32-bit hash derived from `(system_id, object_id, class)` drives probabilistic-but-deterministic choices:

- **Ore:**
  - **RP, DP, RM, AS**: biased toward moderate-to-rich ore.
  - **IC, IM**: lower ore, but sometimes rich.
  - **GG**: ore richness forced to 0.
- **Fuel:**
  - **GG**: always at least normal (2) and often rich (3).
  - Other classes: more likely to be 0–1, with small chances of 2–3.

Because it is purely hash-based, **changing other aspects of object generation does not affect ore/fuel outputs** as long as `system_id`, `object_id`, and `class` remain stable.

---

## Habitability and Risk

Two scalar scores provide a compact summary of how suitable and how dangerous each body is for human activity:

- **habitability**: 0–100 (higher is better)
- **risk**: 0–100 (higher is more dangerous)

They are derived from:

1. The star’s **spectral type** (`spect` column → leading letter O/B/A/F/G/K/M).
2. The object’s **class** (RP/DP/IC/GG/RM/IM/AS).
3. A small deterministic jitter from the object’s hash.

### Habitability

Base habitability starts from:

- **Spectral type**:
  - O/B: very low base
  - A: low
  - F: moderate
  - G: high (best overall)
  - K: slightly lower than G
  - M: lower due to flare activity
- **Class modifier**:
  - RP: strongly positive
  - RM: positive
  - DP: mildly positive
  - IC, IM: neutral or low
  - GG, AS: strongly negative

A small deterministic offset (−8 to +7) is added to avoid all RP around G stars having identical scores. Final values are clamped to 0–100.

### Risk

Risk starts from:

- **Class base risk**:
  - GG and AS: high baseline risk
  - DP and IC: moderate-to-high
  - RP and RM: moderate
- **Spectral modifier**:
  - Hot stars (O/B/A): higher radiation → higher risk
  - Cooler K/M stars: slightly reduced risk

Again, a small deterministic jitter is applied and the result is clamped to 0–100.

The net effect:

- **Rocky planets/moons around G/K stars** are the sweet spot: higher habitability, moderate risk.
- **Gas giants around hot stars** are low habitability and very high risk.
- **Asteroids** are low habitability, moderate-to-high risk.
- **Ice worlds** tend to be low habitability, moderate risk.

Sol’s bodies are also run through this logic, giving Earth a high habitability score and a middling risk score.

---

## Deterministic Generation

Each system uses a deterministic RNG seed computed from:

```text
rng_seed = global_seed XOR (system_id * 0x9E3779B1)
```

This seed controls:

- The number of primary objects.
- Primary planet types.
- Which (if any) primary becomes an asteroid.
- The number and class of moons.

All *additional* per-object attributes (`local_x`, `local_y`, `ore_richness`, `fuel_richness`, `habitability`, `risk`) are derived from **hashes of stable identifiers**:

- `(system_id, primary_index)` for orbit placement.
- `(system_id, object_id)` for moon positions.
- `(system_id, object_id, class)` for environmental attributes.

This ensures:

- Same `star_catalog.csv` + same `--seed` → same `system_objects.csv` every run.
- Save games remain stable even if the generator is re-run.
- Future tweaks to distributions can be made without scrambling already-generated universes, as long as IDs and core rules remain stable.

---

## Command-Line Usage

Example:

```bash
python3 generate_system_objects.py   --input-stars star_catalog.csv   --output-objects system_objects.csv   --max-objects-per-system 5   --seed 42
```

### Arguments

| Argument | Description |
|----------|-------------|
| `--input-stars` | Path to `star_catalog.csv` |
| `--output-objects` | Output file path (default: `system_objects.csv`) |
| `--max-objects-per-system` | Max number of **primary** objects per system (default: 5) |
| `--seed` | Global deterministic seed offset |

---

## Role in the Universe Generator Pipeline

This script is **Phase 1** of the universe:

- Phase 0 → Star systems (`star_catalog.csv`)  
- **Phase 1 → Natural celestial objects (this script → `system_objects.csv`)**  
- Phase 2 → Alien ruins & artifacts (augments `system_objects.csv`)
- Phase 3 → Civilization expansion (colonies, stations, industrial sites)  
- Phase 4 → Trade networks, missions, NPCs  
- Phase 5 → History, factions, and timelines  

Later phases will rename or repurpose these objects and add alien artifacts, but will never delete the underlying natural bodies.

---

## Summary

The Natural Space Object Generator now provides:

- A deterministic astrophysical foundation with primary planets, moons, and asteroids.
- Resource fields for **ore** and **fuel** mining.
- Habitability and risk scores for colony viability and narrative hooks.
- Local 50×50 map coordinates for per-system UI rendering.
- Special handling for Sol.
- A universal `system_objects.csv` suitable for direct game import.

It serves as the stable bridge between the physical universe (Phase 0) and the later civilization, economy, and mission layers.
