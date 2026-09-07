# Phase 2 closeout — accepted production v1

Status: complete at the user's request. **M1 physical-universe generation is complete; Phase 3 initial-scenario design is next.**

## Accepted world

[Manifest](../universe_builder/results/physical-phase2-v1/manifest.json), [artifact catalog](../universe_builder/results/physical-phase2-v1/phase_2/system_objects.csv), [annotated text map](../universe_builder/results/physical-phase2-v1/phase_2/star_map.txt).

- 170 connected systems, 274 natural Spobs.
- Eight technology-associated sites, including Mars in Sol; all eight systems separated by at least three travel-graph jumps.
- 32 additional archaeological sites; 40 sites across 37 systems.
- Technology research is independently possible; artifact sites provide potential acceleration. Actual research effects and history are not simulated by Phase 2.
- Original Phase 0 and Phase 1 data remain unchanged. All existing source and baseline artifacts are preserved.

## Completion evidence

The standard cube pipeline now runs the promoted quota/spacing generator. A reusable independent Phase 2 validator checks input pass-through, site identities and eligibility, counts, Mars, graph separation, definitions, scenario boundaries, checksums, summary and map rendering.

All 63 tests passed, including production/trial parity, main-pipeline routing, invalid configuration, shortest-path thresholds, quota failure without relaxation, seed/order invariance and map-corruption rejection even after checksum replacement. Production artifact CSV matches the approved blue-noise trial exactly. Two full production runs match all twelve output files byte-for-byte. The seven Phase 0/1 output files match their accepted production artifact. All five preserved source/baseline files passed their hash check.

## Map interpretation

The map keeps X at Sol and uses T for other technology systems, A for archaeology-only systems and * for other systems. Technology takes priority over archaeology when both occur in a system. Counts are 1 X, 7 T, 29 A and 133 *. These represent systems; multiple archaeological sites can share one symbol. The map reveals hidden truth for developer inspection and must not seed actor knowledge.

## Phase 3 handoff

Use `physical-phase2-v1` as the current physical-world input. Its separate scenario handoff specifies Mars's pre-epoch discovery/exploitation, while leaving dates, discoverer and initial beneficiaries unspecified. Decide starting epoch, Earth factions, cultures, settlements, capacities, technology access and actor knowledge before generating the initial state.

Scope limits: no living aliens; no simulation of discoveries, interpretation, diffusion or technological benefits yet. Eight research associations are configured, but quantitative mechanics remain Phase 4 work. Full runtime artifact export, save loading, visibility filtering and emulator checks remain Phase 6 work.
