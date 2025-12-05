# Alien Ruins & Artifacts Generator — Phase 2 Specification

This document defines Phase 2 of the universe generation pipeline:  
**Alien Ruins & Artifacts**, a deterministic layer placed on top of the natural objects generated in Phase 1.

There are **no living aliens** in the game universe.  
Artifacts represent ancient, abandoned, enigmatic structures that once belonged to an extinct civilization.  
Their presence influences technological advancement, exploration value, and later historical developments.

---

## Overview

Phase 2:

1. Reads the **Phase‑1 system_objects.csv** (natural bodies only).
2. Determines, **deterministically**, whether each eligible object hosts alien structures.
3. Assigns an **artifact type** to each selected object.
4. Outputs an **augmented system_objects.csv** with two added fields:
   - `artifact_flag`
   - `artifact_type`

All Phase‑1 fields remain intact and unmodified.

Artifact placement is extremely rare:  
**Approximately 1.5–3% of eligible objects** receive them.

---

## Input Requirements

### Input File: `system_objects.csv` (Phase 1)

Required columns:

```
system_id
object_id
class
```

Other fields (name, ore, habitability, local_x/y, etc.) are passed through unchanged.

---

## Eligibility Rules

Alien artifacts may appear on:

- **RP** — Rocky Planet  
- **DP** — Desert Planet  
- **IC** — Ice Planet  
- **RM** — Rocky Moon  
- **IM** — Icy Moon  
- **AS** — Large Asteroid  

Excluded:

- **GG** — Gas Giants (too volatile and inhospitable to retain artifacts)

---

## Artifact Rarity

Each *eligible* natural object has a **deterministic probability** of hosting artifacts.

Default probability:

```
artifact_rate = 0.02    # 2%
```

Over a full dataset, this results in:

- ~1.5–3% artifacts overall  
- Typically **6–12 artifacts** in a 400–500 object galaxy

Artifacts are meant to be **rare**, **high-impact**, and **lore-rich**.

---

## Artifact Types

If an object is selected to host alien structures, it receives one of the following codes:

| Code | Meaning                       | Frequency |
|------|-------------------------------|-----------|
| ARC  | Alien Relic / Data Crystal    | 40% |
| RUI  | Ruined Surface Complex        | 25% |
| FAC  | Abandoned Orbital Facility    | 15% |
| BEA  | Beacon / Signal Source        | 10% |
| ENG  | Exotic Energy Node            | 7% |
| TEC  | Technology Cache (ultra‑rare) | 3% |

These types influence later phases but have no gameplay interaction at this stage.

---

## Output Schema (Augmented)

`system_objects.csv` gains two new fields:

```
artifact_flag   # 0 or 1
artifact_type   # ARC/RUI/FAC/BEA/ENG/TEC or empty
```

Examples:

```
artifact_flag = 0   artifact_type = ""
artifact_flag = 1   artifact_type = "RUI"
```

All rows receive these fields.

---

## Deterministic Assignment Logic

Artifact generation is *fully deterministic*, using a SHA‑256 hash of object identity.

Process:

1. Build key:

```
key = f"{system_id}:{object_id}:artifact"
```

2. Compute SHA‑256(key), take first 4 bytes → `h32`.

3. Convert to probability:

```
p = h32 / 2**32
```

4. Artifact decision:

- If `class` is not eligible → no artifact.
- If eligible and `p < artifact_rate` → artifact assigned.

5. Artifact type selection:

- Use next 4 bytes of the hash as a deterministic chooser.
- Weighted selection across the six artifact types.

This ensures:

- Reproducibility  
- Stability independent of Phase‑1 RNG  
- No ordering dependence  

---

## Role in Later Phases

Phase 2's outputs are essential inputs for:

### Phase 3 — Civilization Expansion
Artifacts drive:
- Early colony attempts  
- Faction conflict  
- Tech acceleration events (especially propulsion breakthroughs)

### Phase 4 — Economy & Missions
Artifacts become:
- High‑value salvage targets  
- Scientific or covert mission locations  
- Strategic positions in trade networks  

### Phase 5 — Historical Timeline
Artifacts anchor key lore moments:
- "Discovery of the Helios Node"
- "Decoding of the Proxima Crystal"
- "Collapse of the Beacon Wars"

---

## Summary

Phase 2 overlays scarce, high‑value alien structures onto natural objects.

It provides:
- Deterministic artifact placement  
- Compact 8‑bit‑friendly encoding (`artifact_flag`, `artifact_type`)  
- A narrative & mechanical backbone for future expansion phases  

Artifacts are rare, mysterious, and powerful — exactly the sparks of advancement you want in your universe.

