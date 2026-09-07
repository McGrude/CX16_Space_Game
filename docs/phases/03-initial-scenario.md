# Phase 3 — Initial Earth scenario

Status: planned, M2. No implementation yet.

## Purpose

Create an explicit starting state at the dawn of interstellar travel. Future political geography must emerge during phase 4, rather than be assigned in advance.

## Inputs

Accepted physical data: `universe_builder/results/physical-phase2-v1/`. Read its `phase_2/initial_scenario_handoff.json` for Mars’s pre-epoch role and explicitly unresolved starting beneficiaries. The artifact text map is omniscient and must not be imported as actor knowledge.

Validated phase 0–2 data; versioned scenario configuration with epoch, seed, initial Earth powers, starting settlements/assets, cultures/languages, and initial technology. Resolve exact identities, date, and Sol infrastructure with the user before defining the scenario.

## Proposed output

`initial_state.json`, carrying `schema_version`, simulation time, next-identity counters, factions, communities/cultures, settlements, assets, research capabilities, and actor knowledge. Keep a separate physical-world reference so initial actors do not automatically know artifact locations or unsurveyed resources.

Faction identity, cultural affiliation, government institutions, available capacity, and current knowledge are distinct fields. Multiple Earth powers share Sol; system ownership alone cannot represent the initial political state.

Use stable entity IDs. Reference natural objects with composite keys. Initial languages/name pools require attributed sources or explicitly authored data. Initial attitudes are configurable institutions and preferences, not immutable ethnic traits.

## Exit criteria

Scenario validation rejects invalid references, duplicate IDs, impossible resource amounts, and contradictory dates. Identical inputs produce identical initial states. Initial knowledge excludes undiscovered facts. A tiny scenario fixture initializes multiple powers in Sol without assigning future colonies. Document units, schemas, and chosen starting assumptions.
