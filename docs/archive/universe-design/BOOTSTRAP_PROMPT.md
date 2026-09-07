# BOOTSTRAP_PROMPT.md — Universe Generation Bootstrap Instructions

These instructions are used to initialize a new ChatGPT/LLM session so that it understands the universe‑generation pipeline and how to continue working within it.

This bootstrap MUST remain consistent with:
- `PROJECT_SPEC.md`
- `PHASE_0_STAR_SYSTEMS.md`
- `PHASE_1_SYSTEM_OBJECTS.md`
- `PHASE_2_ALIEN_ARTIFACTS.md`

---

# Universe Bootstrap Instructions

You are operating inside a multi‑phase deterministic universe generator for a Commander X16 space‑trading RPG.  
Your role is to load the existing data files and extend the universe according to the project specification.

When a session begins, ALWAYS load the following files:

- **star_catalog.csv** — Phase 0 star systems  
- **system_objects.csv** — Phase 1 & 2 combined output containing:  
  - Natural objects (planets, moons, asteroids)  
  - `local_x`, `local_y` (50×50 system map coordinates)  
  - `ore_richness`, `fuel_richness`  
  - `habitability`, `risk`  
  - `artifact_flag`, `artifact_type` (Phase 2 alien artifacts)
- **PROJECT_SPEC.md** — global definition of all phases

Do NOT regenerate Phase 0, Phase 1, or Phase 2 unless explicitly instructed.  
All later phases must treat their outputs as authoritative.

---

# Key Rules

1. **Determinism is mandatory.**  
   All results must be reproducible from existing CSV data and documented rules.

2. **Never invent missing columns.**  
   If data is required and not present, the correct step is to *extend a generation script*, not fabricate values.

3. **Star spectral class matters.**  
   Spectral types (O/B/A/F/G/K/M) influence:
   - Habitability baselines  
   - Risk baselines  
   - Potential future economic and hazard modeling

4. **System and object IDs are immutable.**  
   Never renumber, delete, or reorder existing systems or objects.

5. **No living aliens exist in the universe.**  
   Artifacts represent extinct civilizations only. All expansion is human.

6. **All additions must match PROJECT_SPEC.md.**

---

# Permitted Outputs in Future Phases

When continuing the project, you may generate:

- New CSVs for later phases (e.g., `civilization.csv`, `economy.csv`)
- New Markdown specifications for next phases (Phase 3+)
- Scripts (Python or BASIC) required to generate deterministic data
- Lore text grounded strictly in existing system/object/artifact data

---

# Forbidden Actions

- Do NOT regenerate Phase 0 (`star_catalog.csv`), Phase 1, or Phase 2 (`system_objects.csv` with artifacts) unless asked.  
- Do NOT invent new systems, new celestial objects, or modify their attributes.  
- Do NOT override previously-established deterministic rules.
- Do NOT introduce living alien civilizations.

---

# Phase Summary

- **Phase 0:** Star systems (astronomical foundation)
- **Phase 1:** Natural celestial objects (planets, moons, asteroids with resources)
- **Phase 2:** Alien artifacts (rare ancient structures)
- **Phase 3:** Civilization expansion (human colonies, stations, factions) — *next to implement*
- **Phase 4:** Economy, trade, missions
- **Phase 5:** Historical timeline

---

These instructions provide the minimal skeleton needed for future phases of the universe generator to continue reliably.
