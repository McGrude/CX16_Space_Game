# Phase 0: no map pruning, named-star preference

## Revised selection

The 25 ly source neighborhood contains **167 eligible entries**, of which **34 have catalog proper names**, including Sol. The 300-entry candidate budget does not bind. The former display-pruned baseline contains 136 entries. A separate run of the updated phase 0 command retained all 167 entries, with 32 symbols moved to free cells and no physical coordinates changed by layout.

Map collisions and off-map projection no longer remove stars. Display coordinates are approximate. Named-star preference means actual HYG proper names, not generated names. Sol is mandatory; other names are preferred, not guaranteed.

## Exploratory reachability results

The standalone `current_candidates` analysis computes original 3D distances and tests seven reach values, with eight deterministic trials per value. Removal choices prefer fewer lost named entries (including any disconnected branches), followed by excess-degree reduction per lost entry. Feasible named entries are reinserted first. Trial selection prioritizes named entries retained, then total entries. These are heuristics, not proven optimal subsets.

| Reach (ly) | Total retained | Named retained (of 34) | Neighbor range |
|---|---:|---:|---|
| 8.0 | 91 | 26 | 1–6 |
| 8.5 | 87 | 27 | 1–6 |
| 9.0 | 107 | 33 | 1–6 |
| 9.4 | 108 | 32 | 1–6 |
| 9.5 | 105 | 32 | 1–6 |
| 10.0 | 100 | 30 | 1–6 |
| 10.3 | 94 | 30 | 1–6 |

All listed candidates form one component containing Sol and include every within-range connection among retained entries. The **9.0 ly** candidate is preferable under named-retention priority in this limited search: 107 entries, 212 undirected edges, mean 3.96 neighbors, and 33/34 catalog names. Its one named removal is **Proxima Centauri**; the 9.4 ly candidate also removes **Wolf 359**.

This raises the unresolved multiple-star-system question: separately cataloged components currently count as separate nodes, including components of the Alpha Centauri system. Grouping stars into physical systems may preserve the recognizable destination while changing graph density. No such grouping has been implemented or assumed here. Do not adopt a final reach before resolving this question and reviewing any protected-name list.

## Implementation boundary and verification

Display preservation and named candidate priority are implemented in the Phase 0 generator. Reachability pruning remains an analysis tool until the reach value and source-ID/3D export migration are agreed. No pruning has been applied to the preserved baseline, and no dependent object/artifact data has been migrated.

Reproduce the analysis with:

```sh
python3 -m universe_builder.analysis.current_candidates > /tmp/cx16-current-candidates.json
```

The adjacent JSON records settings, input and implementation hashes, all candidate source identities, retained/removed indices, and trial statistics. Current tests: **26 passing**, covering selection, display preservation, named preference, graph bounds, pruning, and runner behavior. All five preserved source/baseline hashes still match. Full M1 validation remains pending.
