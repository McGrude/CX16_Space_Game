# Phase 2 — Ancient artifacts

Status: major-artifact trial generated for review; Phase 2 acceptance pending (M1). The standard implementation below remains the legacy probability model.
Implementation: `universe_builder/phases/phase_2_alien_artifacts.py`.

## Inputs and configuration

Accepted input: `universe_builder/results/physical-phase1-v1/phase_1/system_objects.csv`. Phase 2 design discussion is next; no artifact run has been accepted for this dataset.

Phase 1 objects. Artifact rate is a probability in [0,1], not a guaranteed fraction or exact count. Preserved launcher settings: rate 0.03 and seed 1; script defaults are rate 0.02 and seed 0.

## Output and algorithm

`phase_2/system_objects.csv` preserves all phase 1 fields and adds:

```text
artifact_flag,artifact_type
```

Eligible classes: RP, DP, IC, RM, IM, AS. Gas giants excluded.
Types/weights: ARC relic/crystal 40; RUI ruins 25; FAC abandoned facility 15; BEA beacon 10; ENG energy node 7; TEC technology cache 3.

The current code hashes `f"{seed}:{system_id}:{object_id}:artifact"` with SHA-256. The first four bytes determine presence; the next four select the weighted type. A no-artifact row has flag 0 and an empty type.

## Visibility and later interpretation

Placement is hidden physical truth. A flag does not imply anybody has discovered, accessed, decoded, or exploited a site. Phase 4 must explicitly model discovery and the arrival of news. No living alien factions exist.

## Validation gate

Check pass-through equality with phase 1, rates 0/1, gas-giant exclusion, valid types, repeatability, independence from row ordering, changed seeds, malformed inputs, and actual baseline differences. Do not fail a run simply because a small sample's artifact percentage differs from the configured probability.

## Current design direction and trial

Artifacts are a major force in history. Sol must have an origin artifact that enabled interstellar travel before the simulation begins. The user proposed 7–8 discoverable technologies and 3–5 times as many archaeological finds. [Trial v1](../analysis/phase-2-major-artifacts-trial.md) interprets this as 8 unique technology sites (including Sol) plus 32 archaeological sites, producing 40 sites across 36 systems. Mars, the eight technology names, unique-source placement and exact quotas are trial assumptions for discussion, not final accepted design. Discovery and exploitation remain separate from physical placement.

## Independent research and artifact acceleration

Every artifact-associated technology can also be developed through independent research. Sites can accelerate progress toward that technology; they are not exclusive sources or mandatory prerequisites. Discovery alone does not automatically grant mastery, deployment or shared faction knowledge. The magnitude and mechanism of acceleration remain to be designed.

The trial’s one-site-per-technology placement counts research opportunities, not exclusive sources of technology. Sol’s artifact historically accelerated the development of interstellar propulsion before the simulation epoch; it was the catalyst in this scenario, not the only theoretically possible route to interstellar travel. Existing trial placements and versioned artifacts remain unchanged.

## Technology-site spacing experiment

The user confirmed Mars, eight technology-associated sites and scattering, then requested a blue-noise-inspired trial. [Three-jump trial](../analysis/phase-2-blue-noise-trial.md) places all eight technology sites at least three travel-graph jumps apart, including Sol, while keeping 32 archaeological sites loosely scattered. All 32 tested seeds satisfy the rule; the current seed has 40 sites across 37 systems. The user approved the spacing direction after review; production promotion and final validation remain.
