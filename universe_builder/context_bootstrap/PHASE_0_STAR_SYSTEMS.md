
# External Resources Used : 

	 HYG 4.2: Current version (2025), containing all stars in
	 Hipparcos, Yale Bright Star, and Gliese catalogs (almost
	 120,000 stars, 14 MB), CC BY-SA-4.0 license
	 From :  https://astronexus.com/projects/hyg





# Star Map Generator — Specification & Documentation

This document defines the **input**, **output**, and **behavioral specifications** for the **Star Map Generator**, a Python tool that converts HYG star catalog data into a compressed, game‑ready 2D star map with synthetic sector/cluster naming.

---

## Overview

The generator:

1. **Loads a local HYG star catalog CSV** (any recent version: 4.x recommended).
2. **Filters stars** within a configurable radius from Sol (in light‑years).
3. **Selects a maximum number of stars** (nearest first).
4. **Projects 3D Cartesian coordinates** (x,y,z in parsecs) into a **2D 100×100 grid**.
5. **Prunes**:
   - Stars outside the 100×100 map
   - Collisions (multiple stars in same cell), using a priority rule
6. **Generates proper names**:
   - Uses real catalog names when available
   - Uses **synthetic sector/cluster names** otherwise (deterministic based on original catalog ID)
7. **Writes two outputs**:
   - A **clean CSV** of final stars
   - A **100×100 ASCII map** of the projected region

The output is stable, deterministic, and suitable for use as a canonical in‑game dataset.

---

## Input Requirements

### **Primary Input**
A local HYG star catalog file, for example:

```
hyg_v4.csv
hygdata_v3.csv
HYG-Database-4.2.csv
```

The file must contain at minimum:
- `dist` or `dist_pc` or `Distance`
- `x`, `y`, `z` (parsec coordinates)
- Optional: `proper`, `mag`, `lum`, `spect`

Missing coordinates are handled gracefully.

---

## Command-Line Usage

```
python3 build_star_database.py     --input-csv HYG.csv     --radius-ly 50     --max-stars 150     --scale 1.0     --csv-out star_catalog.csv     --map-out star_map.txt
```

### **Required Argument**

| Argument | Description |
|---------|-------------|
| `--input-csv` | Path to local HYG CSV |

### **Optional Arguments**

| Argument | Default | Description |
|----------|----------|-------------|
| `--radius-ly` | `50.0` | Only stars within radius (ly) are included |
| `--max-stars` | `150` | Maximum stars kept before projection |
| `--scale` | `1.0` | Light‑years per grid cell |
| `--csv-out` | stdout | Output CSV path |
| `--map-out` | `star_map.txt` | ASCII map output path |

### Exit Behavior
If no stars remain after filtering and projection, the script terminates with an error message.

---

## Data Processing Pipeline

### 1. **Distance Filtering**
Only stars with:
```
dist_ly <= radius_ly
```
are retained.

### 2. **Nearest Star = Sol**
The nearest star (distance 0–0.01 ly) is labeled as Sol and forced to remain.

### 3. **3D → 2D Projection**
Coordinates:

```
grid_x = round(50 + x_ly / scale)
grid_y = round(50 + y_ly / scale)
```

Stars outside `0–99` are **pruned**, not clamped.

### 4. **Collision Resolution**
If two or more stars land in the same cell:

Priority order:
1. Sol (if present)
2. Named stars (real catalog names)
3. Largest star by:
   - Luminosity (higher wins)
   - Apparent magnitude (lower wins)
   - Distance (closer wins)

Only one survives; others are pruned.

---

## Output Files

### 1. **CSV Output (“star_catalog.csv”)**

Sorted by `dist_ly` ascending (Sol first).

#### **CSV Columns**

```
id, proper, dist_ly, grid_x, grid_y, spect
```

| Column | Meaning |
|--------|---------|
| `id` | Monotonic integer: 0 = Sol |
| `proper` | Real name or synthetic sector/cluster name |
| `dist_ly` | Distance from Sol, in light‑years |
| `grid_x` | 0–99 projected X position |
| `grid_y` | 0–99 projected Y position |
| `spect` | Spectral class (string) |

### **Synthetic Naming System**

If a star has no catalog proper name, it receives a deterministic name:

Examples:
```
Helion Sector-17
Koros Cluster-03
Velarn Arc-81
Nadir Reach-22
Triarch Expanse-04
```

Names are derived from:
- Prefix bank  
- Sector type bank  
- Number 01–99  
- RNG seeded using the original catalog ID  

Names remain stable across runs.

---

### 2. **ASCII Map Output (“star_map.txt”)**

A 100×100 grid of characters:

```
X  = Sol
*  = Star
.  = Empty cell inside radius
␣  = Space (outside radius)
```

The map is useful for debugging or display.

---

## Example Region (excerpt)

```
.................................................          
.......................*.........................          
....................*...........*................          
.......................X........................          
....................*............................          
```

---

## Error Conditions

The tool terminates with an explanatory message if:

- Input CSV is missing or unreadable
- No stars fall within the radius
- All stars are pruned during projection
- Map cannot be written to disk

---

## License & Use

The script is free for use in game development, research, or modification.  
HYG database license may apply depending on version downloaded.

---

## Summary

This generator turns raw astronomical data into:

- A clean, **collided-pruned**, **scaled**, **projected**, **named** dataset
- A stable, deterministic 2D star map
- A minimal CSV that is compact enough for retro hardware or game engines

It forms the foundation for your in‑game star system registry.

