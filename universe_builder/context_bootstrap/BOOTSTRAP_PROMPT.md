# Universe Generator BOOTSTRAP PROMPT v1.0

This prompt is designed to initialize a fresh ChatGPT session with all essential context required to continue developing the multi‑phase Universe Generation System. It distills the large project specification into a concise but complete control prompt.

## PURPOSE
Load this prompt at the beginning of any new conversation to restore the model’s understanding of:
- The star catalog generator
- The natural space‑object generator
- The upcoming civilization/colonization simulation
- The architectural principles of the overall universe generator

This avoids long‑thread context loss and keeps the LLM aligned with the project’s design rules.

---

# CORE SYSTEM SUMMARY

## 1. STAR DATABASE GENERATOR (Phase 0)
Produces the foundational 2D mapped starfield.

### Input
- HYG 4.x star catalog (CSV)
- Parameters: radius (LY), max-stars, scale, output CSV, ASCII map

### Process
- Convert RA/Dec/pc to Cartesian (x,y,z)
- Filter stars within radius of Sol
- Project 3D → 2D while preserving general structure
- Scale to 100×100 grid
- Resolve grid collisions:
  1. Prefer stars with real proper names
  2. Otherwise keep the brightest
- Generate:
  - id : canonical star id (0 = Sol)
  - proper : proper name or synthetic sector name
  - dist_ly : distance in light years
  - grid_x : grid position x coordinate
  - grid_y : grid position y coordinate
  - spect : spectral class

### Output
- CSV sorted by distance from Sol
- ASCII star map with:
  - “X” = Sol  
  - “*” = star  
  - “.” = empty in-bounds  
  - “ ” = out-of-bounds / pruned  

---

## 2. NATURAL SPACE OBJECT GENERATOR (Phase 1)
For each star system, generate 0–5 natural objects.

### Object Types
- Rocky Planet  
- Ice Planet  
- Gas Giant  
- Large Moon  
- Large Asteroid  

### Sol Override
Sol always gets:
- Earth (rocky)
- Luna (moon)
- Mars (rocky)
- Ceres (large asteroid)

### Output CSV
- object_id  
- star_id  
- name (temporary or real for Sol only)  
- type  
- mass_estimate  
- orbital_distance_au  
- notes  

---

## 3. EXPANSION & CIVILIZATION MODEL (Phase 2–4)
This phase (up next) will simulate:
- Human expansion between 2100–2450  
- Faction formation and divergence  
- Colony founding, failures, migrations  
- Corporate rise, criminal syndicates, black markets  
- Technology diffusion (FTL Gen1–4)
- Disasters, wars, revolutions
- Trade networks and economic interdependence  

This bootstrap prompt does **not** include full details (those live in PROJECT_SPEC.md), but it instructs the LLM:

→ Always treat Sol as origin of civilization  
→ Always respect phased historical eras  
→ Always maintain deterministic state transitions  
→ Always simulate cause → effect chains  

---

# NEXT‑PHASE OBJECTIVE
We are now preparing to implement:

### **Phase 2: Civilization Expansion & Colonization**
The next scripts will:
- read the star CSV
- read the natural‑object CSV
- simulate colonization waves
- generate inhabited locations (cities, stations, colonies)
- assign factions, corporations, governments
- generate events chronologically

This bootstrap prompt ensures the model will remember how to proceed.

Additionally, the full simulation must maintain a **history event timeline log**:
- File: `history_timeline.log`
- Format: one event per line
- Each line: `YYYY-MM-DD <single-line event summary>` using ISO 8601 date format.

---

# WORKING RULES FOR FUTURE SESSIONS

1. Never contradict prior structure.  
2. Keep outputs deterministic if seeds are provided.  
3. Keep data formats compatible with previous phases.  
4. If asked to expand functionality, propose schema updates rather than breaking existing formats.  
5. When generating large code, include comments and deterministic parsing behavior.  
6. When continuing this project, always load or reference:
   - star_catalog.csv  
   - space_objects.csv  
   - PROJECT_SPEC.md  

---

Use this exact prompt at the beginning of any new conversation to fully re‑hydrate context with minimal tokens.
