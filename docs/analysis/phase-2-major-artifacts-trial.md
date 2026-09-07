# Phase 2 — Major artifacts trial v1

Status: trial, not accepted Phase 2 completion. The user sees artifacts as a major force in history, requires a Sol artifact responsible for initial interstellar capability, and proposed 7–8 discoverable technologies with 3–5 times as many archaeological finds.

## Trial interpretation

Use exact quotas: **8 distinct technologies at 8 technology sites**, including the Sol origin, plus **32 additional archaeological sites** (4×). These categories are disjoint for counting; technology sites can still have archaeological interest. One site per natural Spob. This assumes technologies are represented once each; additional artifact sites or multiple finds contributing to research remain open design options. All eight technologies can also be developed independently; these sites provide potential acceleration, not exclusive access.

Mars is the provisional Sol location chosen for this trial, not an independently confirmed user choice. The other seven technology sites are outside Sol. Archaeological sites may occur on any remaining eligible Spob, including Sol. There is no per-system cap or clustering rule; multiple sites can occupy different Spobs in one system.

Eligible classes remain RP, DP, IC, RM, IM and AS; gas giants are excluded. Select without replacement by seeded SHA-256 ranking with stable source identities. Exact quotas replace per-object probability for this experiment; smaller worlds that cannot satisfy them are rejected. Quota selection is deterministic and row-order independent, but changes to the input world can change placements.

Technology sites use TEC. Archaeological forms are ARC relic, RUI ruins, FAC abandoned facility on the host body, and BEA beacon, equally weighted by deterministic hash. FAC does not generate an orbital station or additional Spob. Site form and strategic technology are distinct concepts.

## Result

40 sites across 36 of 170 systems, on 40 of 249 eligible Spobs (16.1%). All 274 input Spobs and their original fields are preserved. Hosts: 24 rocky planets, eight ice planets, two desert planets, three rocky moons, three icy moons; no asteroids were selected by this seed.

| Draft technology | Host |
|---|---|
| Initial interstellar propulsion | Mars, Sol |
| Advanced propulsion | Ran II |
| FTL communications | Pioneer Cluster-09 I |
| Advanced power | 268 G. Cet I-a |
| Advanced materials | Pioneer Arc-34 I |
| Closed ecological systems | Achird II |
| Advanced sensors | Luyten Reach-27 II |
| Automated industry | Kapteyn's Star II-a |

These technology names and qualitative roles are provisional. They are not implemented bonuses, dependencies or progression rules. Propulsion changes speed, never the fixed 9-ly route graph. Archaeological finds need not unlock major technology; their historical, cultural or economic value remains to be designed.

## Knowledge and scenario boundary

Physical placement is hidden world truth. `initial_scenario_handoff.json` separately proposes that Sol's origin site was discovered and exploited before the simulation epoch. Discoverer, date and initial beneficiaries are explicitly unspecified. Other sites remain hidden until exploration, research and propagation of knowledge occur. No initial factions were created and no history was simulated.

## Files and verification

[Output directory manifest](../../universe_builder/results/phase2-major-artifacts-trial-v1/manifest.json), [augmented objects](../../universe_builder/results/phase2-major-artifacts-trial-v1/system_objects.csv), [summary](../../universe_builder/results/phase2-major-artifacts-trial-v1/summary.json), [draft technologies](../../universe_builder/results/phase2-major-artifacts-trial-v1/technologies.json), and [scenario handoff](../../universe_builder/results/phase2-major-artifacts-trial-v1/initial_scenario_handoff.json).

New columns beyond the legacy artifact flag/type: `artifact_category`, `technology_id`, `artifact_site_id`. Site IDs use source `(system_id,object_id)` identity; no discovery state is placed in the physical object CSV. The runtime export has not been rebuilt and does not yet export these fields.

```sh
python3 -m universe_builder.analysis.phase2_major_artifacts --config universe_builder/configs/phase2_major_artifacts_trial.json --output /tmp/new-major-artifact-trial
```

All 58 tests passed. Tests cover exact counts, distinct technology identities, Sol origin, gas-giant exclusion, input pass-through, input-order independence, seed variation and invalid quotas/origins. All five output files match independent replay byte-for-byte. The standard Phase 2 generator remains the legacy probability model pending trial review and promotion.

## Subsequent clarification

The user confirmed that artifact-associated technologies are independently researchable. Interpret the trial’s eight sites as opportunities to accelerate those research paths. Sol’s find catalyzed interstellar development in this scenario; it was not a universal technological prerequisite. Quantitative research effects remain deferred. The original trial files are preserved as generated.
