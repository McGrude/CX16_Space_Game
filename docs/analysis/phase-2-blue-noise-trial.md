# Phase 2 — Graph spacing trial v1

Status: tested proposal; no Phase 2 promotion or closeout implied. Mars, eight technology-associated sites and scattered distribution are user-approved. This experiment tests the proposed three-jump spacing rule. The 32 archaeological finds retain the previous trial quota.

## Algorithm

Compute shortest unweighted hop distances on the accepted 170-system travel graph, including transit systems without Spobs. Keep Mars fixed. Visit eligible non-Sol Spobs in seeded SHA-256 order and accept a technology site only if its system is at least three jumps from every already selected technology system, including Sol. Stop at eight sites; if the greedy pass cannot meet the quota, fail explicitly without changing spacing or counts. Failure would not prove no feasible placement exists.

This is a graph-distance exclusion rule inspired by blue noise, not a claim of spectral blue-noise properties or globally optimal coverage. Candidates are ranked per eligible Spob, so systems with more eligible Spobs receive more opportunities; no equal-per-system weighting is claimed. The other seven draft technologies are assigned in configuration order to accepted sites. Technologies remain independently researchable; sites accelerate rather than monopolize access.

Select 32 archaeology-only Spobs from remaining eligible objects using the existing independent seeded ordering. These sites have no minimum spacing and may share systems with each other or technology sites. No extra Spobs are generated.

## Result at seed 1

| Measure | Original scattering | Three-jump trial |
|---|---:|---:|
| Technology sites | 8 | 8 |
| Archaeology-only sites | 32 | 32 |
| Systems containing any site | 36 | 37 |
| Minimum technology pair separation | 1 jump | 3 jumps |
| Mean nearest technology-site separation | 2.625 jumps | 3.625 jumps |

Distances from Sol to the other technology systems: **4, 5, 5, 7, 8, 9, 11 jumps**. The farthest system from its nearest technology site is eight jumps away: exclusion spacing does not guarantee uniform coverage. All 274 natural objects and original fields are preserved.

[Site-by-site summary](../../universe_builder/results/phase2-blue-noise-trial-v1/summary.json), [augmented Spobs](../../universe_builder/results/phase2-blue-noise-trial-v1/system_objects.csv), [manifest](../../universe_builder/results/phase2-blue-noise-trial-v1/manifest.json).

## Verification

All 32 seeds from 0 through 31 placed eight distinct technology-bearing systems with every pair at least three jumps apart, kept Mars as origin, and retained 32 archaeological sites. Reversing input object order preserved identity-based placement for every seed. Across these seeds, the nearest non-Sol technology site was 3–5 jumps from Sol.

All 60 tests passed, including known shortest paths, exact threshold behavior, unsatisfied-quota rejection without relaxation, and disconnected-graph rejection. A separate run reproduced all five files byte-for-byte. The manifest records the route hash as well as input, configuration and implementation hashes.

```sh
python3 -m universe_builder.analysis.phase2_major_artifacts --config universe_builder/configs/phase2_blue_noise_trial.json --output /tmp/new-spacing-trial
```

Recommendation: adopt three-jump technology-site separation for the current world size. Retain loose archaeological scattering to preserve occasional clusters. Research effects, detailed discovery histories and full Phase 2 production promotion remain separate work.
