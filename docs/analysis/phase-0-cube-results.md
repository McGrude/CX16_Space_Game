# Phase 0 — Cube v2 results

Status: generated and independently validated; ready for user review. Phase 0 was deliberately reopened. Spherical v1 and existing Phase 1 trial data remain preserved.

## Region and rules

Select primary-star positions inside a 50-light-year cube centered on Sol, aligned with HYG x/y/z axes: −25 ≤ each coordinate ≤ +25 ly. Group first and retain cataloged companions even outside the region. The theoretical corner distance is 43.30 ly; the farthest retained primary is 37.93 ly from Sol.

Travel uses true 3D distances and a fixed 9.0 ly reach. Technology affects travel time only. Retain Sol, prefer catalog-named systems, and prune systems to one connected graph with 1–6 neighbors. Keep every within-reach edge between retained systems. Eight deterministic pruning trials are evaluated. The heuristic does not establish a global optimum. The 300-system candidate cap was not reached.

## Summary

| Metric | Spherical v1 | Cube v2 |
|---|---:|---:|
| Candidate systems | 133 | 225 |
| Candidate cataloged stellar members | 167 | 274 |
| Retained destinations | 99 | 170 |
| Retained cataloged stellar members | 127 | 210 |
| Named destinations retained / candidates | 30 / 30 | 38 / 39 |
| Named members retained / candidates | 34 / 34 | 43 / 44 |
| Pruned candidate systems | 34 | 55 |
| Undirected travel routes | 188 | 321 |
| Mean neighbors | 3.80 | 3.78 |
| Neighbor range | 1–6 | 1–6 |
| Connected components | 1 | 1 |

Cube v2 contains 134 single-member destinations and 36 multiple-member destinations. These counts describe catalog records, not a complete inventory of all physical companions.

Compared with v1, 94 destinations remain, 76 are added, and five previously retained unnamed destinations are pruned: a net gain of 71 systems (71.7%). Re-running pruning on the larger graph can change retention inside the original sphere.

All previously retained named systems survive. Added named destinations: Chara, p Eridani, Vega, Fomalhaut, Tabit, Deltoton, Groombridge 1830, and Rana. One new named candidate, Añañuca, is pruned by the selected network heuristic; named preference is not a guarantee of retention.

| Direct neighbors | Systems |
|---|---:|
| 1 | 15 |
| 2 | 21 |
| 3 | 37 |
| 4 | 40 |
| 5 | 28 |
| 6 | 29 |

Sol connects to Alpha Centauri, Barnard's Star, Wolf 359, Lalande 21185, and Sirius.

## Map and quality limits

The [text map](../../universe_builder/results/grouped-phase0-cube-v2/phase_0/star_map.txt) is 100×100 characters: X is Sol, * is another destination, and dots are empty display cells. The circular mask is removed. Six symbols were moved to free cells; none were removed for display collisions. Sol remains at (50,50); the even-sized grid and rounding make the boundary representation approximate. Physical positions and routes are unaffected.

Four retained destinations carry source-quality flags: HYG 45211, 83882 and 118084 (p Eridani) have member-coordinate offsets over 1 ly; HYG 118187 has incomplete cataloged companion linkage. Two other flagged candidates were pruned. Raw records and flags remain in the exports; no astrometry or membership was invented or corrected.

## Files and reproduction

- [Configuration](../../universe_builder/configs/grouped_systems_cube.json)
- [Manifest](../../universe_builder/results/grouped-phase0-cube-v2/manifest.json)
- [System catalog](../../universe_builder/results/grouped-phase0-cube-v2/phase_0/star_catalog.csv)
- [Summary and quality flags](../../universe_builder/results/grouped-phase0-cube-v2/phase_0/selection_summary.json)
- [Travel routes](../../universe_builder/results/grouped-phase0-cube-v2/phase_0/routes.csv)

```sh
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems_cube.json --output /tmp/my-new-cube-run --through 0
python3 -m universe_builder.validation.phase0 universe_builder/results/grouped-phase0-cube-v2
python3 -m unittest discover -s universe_builder/tests -v
python3 -m universe_builder verify-baseline
```

Output directories must be new. Validation passed for geographic bounds, identities, members, all physical edges, connectivity, degree bounds, map placement, summary counts and output checksums. All 46 tests passed, including cube boundary/axis selection and configuration coverage. A second independent generation produced byte-identical copies of all six outputs. Spherical v1 output hashes and all five preserved source/baseline files remain unchanged.

Phase 1 has not been regenerated for these 170 systems; its prior 161-Spob trial still refers to spherical v1.
