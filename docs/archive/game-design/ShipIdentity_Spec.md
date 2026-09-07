# Commander X16 Space RPG — Ship Identity & Ship Type Database Specification

This document defines the **runtime Ship Identity model** and the corresponding **static Ship Type CSV format**, incorporating the latest design decisions.  
It reflects that *ship type data must be loaded into RAM at runtime* for fast access, but *does not need to be saved* in save‑game files because it is static.

---

# 1. Overview

A player’s ship consists of:

- **Static ship type data** (class, fuel cap, cargo cap, builder, etc.), loaded from CSV once at startup.
- **Dynamic ship instance data** (name, fuel level, registration ID), stored in the save game.

To avoid repeated CSV lookups during gameplay, **all static ship type fields are copied into arrays in RAM** at startup.

Only the *ship instance fields* are saved.

---

# 2. Ship Identity (Dynamic, Stored in Save Game)

These values represent the *player’s specific ship*.

```
SH%   ' Ship Type ID (index into type arrays)
SH$   ' Ship name (string)
SR$   ' Registration / transponder ID (string)
FL    ' Current fuel level (float)
```

Derived values **not saved**, but always looked up from static ship type arrays:
- Maximum fuel  
- Maximum cargo  
- Equipment capacity  
- Ship class / weight  
- Builder / manufacturer ID  

---

# 3. Ship Type Data (Static, Loaded from CSV Into RAM)

At startup, the game reads a CSV file such as:

```
shiptypes.csv
```

Each row corresponds to a **Ship Type ID** (row index).

These values are copied into RAM arrays and remain constant for the entire game session.

### **RAM Arrays**

```
DIM ST_NAME$(MAX_ST)     ' Ship type name string
DIM ST_CLASS(MAX_ST)     ' Weight class (int)
DIM ST_FUELM(MAX_ST)     ' Max fuel (float or int)
DIM ST_CARGOM(MAX_ST)    ' Max cargo capacity
DIM ST_EQP(MAX_ST)       ' Equipment slot / capacity rating
DIM ST_BUILD(MAX_ST)     ' Builder / company ID
```

Other derived/statistical fields may be added later, but these form the core.

---

# 4. CSV Specification (Static Ship Type Database)

The CSV should follow a consistent column layout.  
You can reorder or add fields later, but for now we use the following:

```
TYPE_ID, NAME, CLASS, FUEL_MAX, CARGO_MAX, EQP_CAP, BUILDER_ID
```

### Column Meanings

| Column       | Description |
|--------------|-------------|
| `TYPE_ID`    | Integer ID, 0-based or 1-based depending on your scheme. |
| `NAME`       | Ship class name (e.g., SCOUT, CORVETTE, HEAVY FREIGHTER). |
| `CLASS`      | Weight class (1=light, 2=medium, 3=heavy…). Used for equipment gating. |
| `FUEL_MAX`   | Maximum fuel capacity for the type. |
| `CARGO_MAX`  | Maximum cargo capacity (units). |
| `EQP_CAP`    | Equipment capacity budget or slot count. |
| `BUILDER_ID` | Manufacturer/company ID; ties into factions, missions, legality, etc. |

### Example CSV

```
0,SCOUT,1,100,40,10,2
1,CORVETTE,2,200,80,18,3
2,HEAVY FREIGHTER,3,300,260,24,4
```

---

# 5. Runtime Lookup Model

At runtime:

1. The game reads `shiptypes.csv`.
2. For each row, it populates the arrays:

```
ST_NAME$(id)
ST_CLASS(id)
ST_FUELM(id)
ST_CARGOM(id)
ST_EQP(id)
ST_BUILD(id)
```

3. During gameplay, the ship instance uses `SH%` to access all static stats.

### Example:

```
PRINT "Fuel:", FL, "/", ST_FUELM(SH%)
PRINT "Cargo Cap:", ST_CARGOM(SH%)
IF NEW_EQUIP_CLASS > ST_CLASS(SH%) THEN PRINT "Cannot install"
```

No CSV access occurs during play.

---

# 6. Save Game Behavior

**Saved:**
- `SH%`
- `SH$`
- `SR$`
- `FL`

**Not saved:**
- Any ST_* fields (reloaded from CSV on startup)
- Fuel/cargo capacity (derived)
- Weight class
- Builder ID
- Equipment capacity

This keeps save files small and guarantees consistency with updated data files.

---

# 7. Future Extensions (Optional)

Later additions to the CSV could include:
- Crew capacity
- Base hull integrity
- Base price
- Turn rate / thrust rating
- Sensor strength
- Flavor text
- Variant IDs (e.g., Mk II, Mk III)

These will follow the same pattern: stored in arrays, not saved in game state.

---

**This document captures the finalized design for ship identity and ship type storage.**  
You can continue iterating equipment, crew, cargo, and factions using this as the foundation.
