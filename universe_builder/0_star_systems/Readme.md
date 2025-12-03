
# External Resources Used : 

	 HYG 4.2: Current version (2025), containing all stars in
	 Hipparcos, Yale Bright Star, and Gliese catalogs (almost
	 120,000 stars, 14 MB), CC BY-SA-4.0 license
	 From :  https://astronexus.com/projects/hyg




# Star Catalog Generator  
### Local Sector Map Builder for the Commander X16 Space Game

This tool generates a **game-ready star catalog** and a **100×100 ASCII stellar map** from a real astronomical dataset (HYG 4.x or later).  
It serves as the first stage of the game’s universe-generation pipeline.

The script:

- Loads a HYG star catalog CSV (local file).
- Filters stars within a configurable radius from Sol (in light-years).
- Projects 3D coordinates (x,y,z) into a 2D 100×100 sector map.
- Prunes off-map stars.
- Handles collisions: when multiple stars map to the same grid cell, it:
  1. Prefers the star with a real proper name.
  2. If none have proper names, keeps the brightest/largest star.
  3. Ensures Sol always wins.
- Synthesizes **sector/cluster style star names** for unnamed stars.
- Outputs:
  - A compact CSV database suitable for loading into the game.
  - A 100×100 ASCII sector grid for human reference.

---

## Table of Contents

1. [Requirements](#requirements)  
2. [Input Dataset](#input-dataset)  
3. [Program Usage](#program-usage)  
4. [Processing Stages](#processing-stages)  
5. [Output Files](#output-files)  
6. [CSV Output Specification](#csv-output-specification)  
7. [ASCII Map Specification](#ascii-map-specification)  
8. [Synthetic Star Naming Scheme](#synthetic-star-naming-scheme)  
9. [Collision Resolution Rules](#collision-resolution-rules)  
10. [Known Limitations](#known-limitations)  

---

## Requirements

- Python 3.8+  
- A local copy of the HYG star database (version 4.x or later recommended).  
  Download from:  
  https://astronexus.com/projects/hyg

---

## Input Dataset

The program expects a **HYG database CSV file** containing at least the following fields:

- `id` or `ID`
- `hip` (optional)
- `proper` (optional)
- `x`, `y`, `z` (Cartesian coordinates in parsecs)
- `dist` or `dist_pc`  
- `spect`, `mag`, `lum`, `absmag` (optional but used if present)

### Required coordinate system
Coordinates must be centered on **Sol at (0,0,0)** in parsecs.  
HYG already provides this.

### Required distance units
- Input distance is in **parsecs**.  
- Program converts to **light-years** automatically.

---

## Program Usage

