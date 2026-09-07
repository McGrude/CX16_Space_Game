# Phase 1 density trial v1

Experimental run, not Phase 1 acceptance. Input is the accepted 99-system Phase 0 catalog; seed **42**. No Phase 0 files or existing Phase 1 generator code were changed.

## Rules tested

Total represented natural-body probabilities: **0:10%, 1:35%, 2:35%, 3:15%, 4:4%, 5:1%**. Moons and represented parent bodies share this total budget. Sol retains the existing Earth/Luna/Mars/Ceres exception.

Composition uses existing planet-type, attribute, and moon probabilities. A primary is created, its drawn moons use available remaining slots, and generation continues until the budget is filled. This clips moon counts rather than adding them beyond the budget. An optional asteroid can replace a moonless primary when at least two primaries exist. This ordering is an experimental composition rule, not a final adopted model. Artificial satellites/stations and per-member stellar orbits are outside this trial.

## Result

| Total objects | All 99 systems | Excluding Sol (98 systems) | Configured probability |
|---|---:|---:|---:|
| 0 | 8 | 8 | 10% |
| 1 | 43 | 43 | 35% |
| 2 | 31 | 31 | 35% |
| 3 | 12 | 12 | 15% |
| 4 | 5 | 4 | 4% |
| 5 | 0 | 0 | 1% |

- **161 objects**, averaging **1.63 per system** (1.60 excluding Sol).
- **74 of 99 systems** have one or two objects (74.7%).
- **94 of 99 systems** have zero to three (94.9%).
- **125 planets, 29 moons, 7 large asteroids**. Planets include 14 gas giants.
- No system drew five bodies in this seed. Probabilities are not exact quotas.
- Existing generator on the **same 99 systems and seed** produces **308 objects**, averaging 3.11; the trial produces about 48% fewer. This comparison includes both the changed count weights and the shared moon budget.

Empty systems in this run: Van Maanen's Star, Nomad Reach-18, Luyten Reach-14, Velarn Reach-09, Tauven Cluster-71, Nomad Expanse-80, Nomad Sector-62, Draxis Sector-42.

## Verification and known issues

All object counts fit their drawn total budgets. Repeated generation matches; IDs, parent references, coordinate bounds, and attribute ranges pass trial checks. Focused tests exercise all budgets 0–5, Sol's exception, and repeatability. Full suite: **44 tests passed**.

The reused local-map layout has overlapping object cells in two systems: Struve 2398 (ID 91484), Vegaine Expanse-27 (ID 118447). These are explicitly recorded for follow-up; the trial is not a layout-validation pass or an accepted Phase 1 release. Stellar-member parent selection, composition weighting, and Sol's final contents still need review.

## Files and reproduction

- [Trial objects](../../universe_builder/results/phase1-density-trial-v1/system_objects.csv)
- [Counts and per-system summary](../../universe_builder/results/phase1-density-trial-v1/summary.json)
- [Config and provenance](../../universe_builder/results/phase1-density-trial-v1/manifest.json)

```sh
python3 -m universe_builder.analysis.phase1_density --config universe_builder/configs/phase1_density_trial.json --output /tmp/cx16-phase1-density-trial
```

Choose a new output directory. The manifest records config, input and implementation hashes, interpreter version, and output hashes. Phase 1 production code and historical data remain unchanged.
