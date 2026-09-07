# Phase 2 — Ancient artifacts

Status: **closed — accepted production v1** for physical placement, completing M1. See [closeout](../PHASE_2_CLOSEOUT.md). Phase 3 initial-scenario design is next.

Implementation: `universe_builder/phases/phase_2_artifact_sites.py`. The standard cube configuration uses `model: spaced_sites_v1`. The former probability model remains available only through historical configurations; it is not the current placement policy.

## Accepted rules

Input is validated Phase 1 natural Spobs plus the fixed Phase 0 travel graph. Preserve every input field and source-based `(system_id,object_id)` identity.

- Eight technology-associated sites, each associated with one distinct technology path; Mars `(0,2)` is the fixed initial interstellar-propulsion site.
- Other technology sites are outside Sol, in distinct systems at least three shortest-path jumps apart, including separation from Sol. Technology changes speed, never physical reach.
- Select eligible Spobs in deterministic seeded hash order, accepting each only if it meets separation from all selected sites. This is blue-noise-inspired graph exclusion, not optimal uniform coverage. More eligible Spobs give a system more selection opportunities. Fail if the greedy pass cannot meet the exact quota; do not silently relax spacing or counts.
- Place 32 additional archaeological sites without replacement among remaining eligible Spobs, using independent seeded hash ranking. No archaeology separation or per-system cap; several sites may share a system on different bodies.
- Eligible: RP, DP, IC, RM, IM, AS. Gas giants excluded. One site per Spob. No new Spobs or orbital stations are generated. Archaeological forms: ARC relic, RUI ruins, FAC facility on the host body, BEA beacon. Technology sites use TEC.

Every technology can also be developed independently. Sites may accelerate research, not monopolize access. The configured eight names describe research associations; quantitative effects and dependencies remain Phase 4 design work.

## Outputs

`phase_2/system_objects.csv` adds `artifact_flag,artifact_type,artifact_category,technology_id,artifact_site_id`. Category is technology, archaeology or empty. No-site rows have flag 0 and empty other added fields. Site identity is `site:<source-system-id>:<local-object-id>`.

Also emit `technologies.json`, `summary.json`, `initial_scenario_handoff.json` and `star_map.txt`. The parent run manifest records all output hashes and generator/configuration provenance.

The handoff records the Mars site as discovered and exploited before the simulation epoch. It does not invent a discoverer, date or initial beneficiaries. Other sites are hidden until explicit discovery and knowledge propagation. No placement record gives factions knowledge, deployed equipment or research bonuses automatically.

## Developer review map

100×100 text map, using Phase 0 display cells and background. X = Sol; T = a system with a technology site; A = a system with archaeological sites and no technology site; * = another system. Priority is X, then T, then A. One symbol represents a system, not each individual site. This omniscient review artifact is not a player/faction knowledge map.

Current symbols: 1 X, 7 T, 29 A, 133 *. Mars's technology is represented by Sol's X. Some archaeological sites share systems, so A symbols do not count individual sites.

## Verification and reproduction

```sh
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems_cube.json --output /tmp/new-physical-world --through 2
python3 -m universe_builder.validation.phase2 universe_builder/results/physical-phase2-v1
python3 -m unittest discover -s universe_builder/tests -v
```

Use a new output directory. Independent validation checks Phase 0/1, checksums, full input pass-through, identities, eligibility, quotas, origin, unique technology associations, graph separation, map contents, summary, definitions and scenario handoff. The accepted Phase 2 CSV matches the approved spacing trial exactly. Full reproduction matches all twelve Phase 0–2 output files. All 63 tests pass.

The previous runtime export remains a separate physical-ID subset; artifact data and this omniscient map have not been silently added to runtime/player data. A complete X16 snapshot and loader belong to Phase 6.
