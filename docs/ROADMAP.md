# Milestone roadmap

Complete milestones in order. Every milestone ends with evidence and an updated status; scope can be revised with the user. Later milestones are plans, not implemented functionality.

| Milestone | Status | Deliverable and completion gate |
|---|---|---|
| M0 — Repository foundation | Complete | Separate game/generator/docs; preserve prior files; document phases, decisions, license scope, and commands; verify organization and runner plumbing |
| M1 — Validate physical universe | Next | Audit phases 0–2 against contracts; validate schemas, IDs, references, ranges, Sol behavior, artifact eligibility and pass-through; establish replay results and explain every baseline difference |
| M2 — Initial Earth scenario | Planned | Phase 3: versioned initial factions, cultures, assets, knowledge, configuration, and schema; resolve epoch/identities with user; deterministic initialization tests |
| M3 — First interstellar settlements | Planned | Phase 4 foundation: clock, faction decisions, exploration, expeditions, arrival, supplies, settlement survival; a small scenario yields an explainable chronology |
| M4 — Research and delayed knowledge | Planned | Propulsion research, construction/refits, message transport, dated local knowledge, discoveries; no actor reacts before learning; old/new ships coexist |
| M5 — Political change | Planned | Satisfaction, autonomy, alliances, conflict, secession, merger and extinction with resource costs and inertia; settlements survive ownership transitions; adverse scenarios tested |
| M6 — Cultural and communication history | Planned | Cultural continuity/mixing, naming and renaming records, research/artifact communication unlock and deployment; test language/ownership independence and network reach |
| M7 — World inspection and balance | Planned | Phase 5: histories, charts or reports, snapshot and grounded opportunity seeds; reproducible multi-seed sweeps and agreed health ranges; diagnose extremes rather than hide them |
| M8 — X16 world export | Planned | Phase 6: versioned compact files and IDs, export validator, memory/load budgets and date mapping; minimal loader exercised on X16 emulator |
| M9 — First playable route | Planned | Dock, buy cargo, travel, encounter, sell, save/load using one exported world; add combat/crew depth incrementally |

## Immediate next step: Phase 0 design review

The repository foundation is complete. Before executing M1 validation, discuss Phase 0 in detail with the user: intended stellar neighborhood, catalog selection, treatment of multiple stars, 2D projection and cell collisions, travel-distance geometry, naming, and identifier stability. Distinguish existing behavior from proposed changes, and record agreed decisions in `DECISIONS.md` and the phase contract.

Then validate Phase 0, followed by phases 1 and 2 in dependency order. Preserve the baseline, record discrepancies, and make targeted fixes with regression checks. Begin Phase 3 scenario implementation only after the physical foundation is reviewed and validated.

## M1 validation checklist

1. Inventory input/output schemas, source attribution, generator settings, and interpreter assumptions.
2. Run each phase in a fresh disposable directory. Compare repeated runs with the same seed and implementation.
3. Compare results against preserved baseline; classify byte formatting versus semantic differences and investigate causes. Do not replace the baseline to make a check pass.
4. Test Sol, grid boundaries/collisions, missing catalog fields, object caps, moons/parents, and empty systems.
5. Test artifact rates 0 and 1, ineligible objects, stable assignment after row reordering, and preservation of phase 1 fields.
6. Check invalid-input behavior and document fixes with focused regression tests.
7. Record findings in `docs/VALIDATION.md`. Agree readiness before implementing phase 3.

## M3 minimum scope

Use a few nearby systems and a small scenario. Begin with population, industrial capacity, and supplies rather than a detailed commodity market. Actors choose among exploration, settlement, resupply, and investment. Chronology must explain departures, arrivals, costs, failures, and colony status. Initial cultures can provide names before advanced cultural change is modeled.

## Later model health checks

Track population, viable settlements, factions, territory concentration, resource shortages, expedition losses, research progress, political transitions, and event frequency. Include fixed illustrative scenarios and multiple seeds. Determine useful ranges through review; do not impose an arbitrary faction count by silently spawning or deleting governments.
