# Phase 2 — Ancient artifacts

Status: existing implementation, validation pending (M1).
Implementation: `universe_builder/phases/phase_2_alien_artifacts.py`.

## Inputs and configuration

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
