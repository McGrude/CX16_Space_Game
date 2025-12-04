# PROJECT_SPEC.md — Universe Generator Master Specification
Version 1.0 (Consolidated)

This file contains the authoritative, condensed specification for the multi‑phase universe generator.  
It is designed so any new ChatGPT session can load it to regain the entire project context.

---

# PHASE 0 — STAR GENERATION SYSTEM
(Complete)

See the bootstrap prompt for details, or the dedicated README for implementation notes.

Output:
- `stars.csv`
- `star_map.txt`

---

# PHASE 1 — NATURAL SPACE OBJECT GENERATION
(Complete)

Generates up to 5 natural objects per star system using probabilistic distributions.

Sol uses fixed objects (Earth, Luna, Mars, Ceres).

Output:
- `space_objects.csv`

---

# PHASE 2 — COLONIZATION & CIVILIZATION SIMULATION
(Current Phase to Develop)

## Purpose
Simulate 350 years of human expansion from Sol outward, producing:
- Factions
- Corporations
- Criminal Syndicates
- Colonies & Stations
- Historical timeline
- Emergent political landscape
- Trade networks
- Technology progression
- Disasters, wars, reforms, revolutions

This simulation uses the star map and natural-object data as scaffolding.

---

# ERA FRAMEWORK

### Era 1 — 2100–2200: First Expansion
- FTL Generation 1  
- Slow, careful colonization  
- 5–15 systems settled  
- Earth‑centric government  
- Early disasters, early breakthroughs  

### Era 2 — 2200–2300: Colonial Period
- FTL Gen2  
- Factions form  
- Corporations consolidate  
- 40–70 systems settled  
- Conflicts begin  

### Era 3 — 2300–2400: Consolidation & Conflict
- FTL Gen3  
- The Great War  
- Refugees, famine, systemic collapse  
- 80–120 systems inhabited  
- Some systems abandoned  

### Era 4 — 2400–2450: Modern Era
- FTL Gen4  
- Cold wars, espionage, black markets  
- Mature economy and political map  

---

# ENTITY MODELS

## Factions (6)
Types:
- Utopian Democracy  
- Corporate Oligarchy  
- Military Hegemony  
- Technocratic Collective  
- Frontier Confederacy  
- Dystopian Autocracy  

Each faction tracks:
- name, government, ideology  
- capital system  
- territory list  
- military strength  
- economic strength  
- relationships to other factions  
- historical evolution  

---

## Corporations (10)
Industries:
- Shipbuilding, Mining, Energy, Weapons, High‑Tech, Logistics, Biotech, Luxury, Finance, Terraforming  

Track:
- name  
- sector  
- HQ system  
- market share  
- alignments  
- history  
- events  

---

## Criminal Syndicates (3–5)
Types:
- Pirates  
- Drug cartels  
- Cybercrime networks  
- Smuggling cartels  
- Organized crime families  

Track:
- operations  
- bases  
- revenue  
- hostilities  
- major events  

---

# COLONY & INSTALLATION TYPES

## Inhabited types
- Core world  
- Industrial world  
- Agricultural world  
- Mining colony  
- Tech hub  
- Military base  
- Trade station  
- Refinery  
- Research station  
- Frontier colony  
- Corporate HQ  
- Luxury resort  
- Prison colony  
- Freeport  

## Uninhabited types
- Barren outpost  
- Abandoned colony  
- Derelict station  
- Ancient alien ruins  

---

# TECHNOLOGY SYSTEM

FTL progression:
1. Gen1 — dangerous, slow  
2. Gen2 — practical  
3. Gen3 — commercial  
4. Gen4 — ubiquitous  

Diffusion mechanics:
- open vs proprietary  
- embargoes  
- espionage  
- regression in isolated systems  

---

# EVENT ENGINE

Event categories:
- Political upheaval  
- War  
- Corporate drama  
- Syndicate activity  
- Natural disasters  
- Discoveries  
- Population shocks  

Each event has:
- cause  
- participants  
- systems affected  
- consequences  
- long‑term effects  
- timeline insertion  

---

# OUTPUT OF FULL SIMULATION

Top‑level file: `universe.json`

Plus multiple CSVs:
- systems.csv  
- installations.csv  
- uninhabited_resources.csv  
- factions.csv  
- corporations.csv  
- syndicates.csv  
- trade_routes.csv  
- commodity_prices.csv  
- history.csv  
- relationships.csv  

Plus human‑readable:
- summary.txt
- history_timeline.log (ISO date + single-line event summary, one event per line)

Plus visualization:
- star_map.svg  

This master specification is intended for use across multiple scripts and multiple ChatGPT sessions.  
Always load this file (or paste relevant sections) before asking the model to continue development.
