# Phase 0 fixed-reach analysis

## Accepted design decision

Technology advancement increases speed and decreases travel time. It does not increase reach. Physical route availability is fixed across propulsion technology levels; knowledge of destinations and political access are separate concerns. The user also accepts reachability as a system-pruning criterion. The fixed distance and exact pruning policy remain undecided.

## Dataset and method

Read the preserved 136-entry phase 0 catalog. Match each entry uniquely to the bundled HYG source using exported name (including the existing synthetic naming function), distance from Sol, spectral type, and projected cell at the configured scale. All 136 matches are unique. Retain existing entries and IDs; do not regenerate or select a new catalog.

Calculate Euclidean distances from original HYG x/y/z coordinates, converting parsecs using the generator's factor 3.26156. Treat every retained catalog entry as one game node, including separately retained members of multiple-star systems. This analysis does not resolve that modeling question or restore stars removed by map collisions. Future catalog changes require recalculation.

For a radius R, connect every pair whose distance is <= R. Edges are undirected. Count degrees and connected components: having no isolated vertices is not by itself sufficient to prevent disconnected groups.

Exact bounds for this dataset:

- No isolated systems requires R >= **10.282294458649544 ly**, the largest nearest-neighbor distance.
- A maximum of six neighbors requires R < **6.504054848147945 ly**, the smallest seventh-neighbor distance. The upper bound is exclusive.
- A single connected component requires R >= **10.282294458649544 ly**, the largest edge in a minimum spanning tree.

The ranges do not overlap. **No single distance-only reach value satisfies both requirements.** Reported precision describes arithmetic on catalog inputs, not astronomical measurement accuracy.

## Results

| Reach (ly) | Min neighbors | Max neighbors | Average | Isolated systems | Disconnected groups/components |
|---|---:|---:|---:|---:|---:|
| 6.0 | 0 | 5 | 2.00 | 27 | 46 |
| Just below 6.504055 | 0 | 6 | 2.46 | 20 | 34 |
| 8.0 | 0 | 11 | 4.18 | 7 | 15 |
| 10.0 | 0 | 15 | 7.90 | 1 | 3 |
| 10.3 | 1 | 17 | 8.68 | 0 | 1 |

The limiting remote node is **Koros Arc-62**, game ID 134 / HYG ID 119616. Its nearest connection is **268 G. Cet**, game ID 117, at about 10.2823 ly. **Meridian Expanse-58**, game ID 51, first reaches seven neighbors at about 6.50405 ly.

## Pruning systems: permitted approach and candidate recommendation

With pruning permitted, keep the simple distance rule: every pair of **retained** systems within reach is connected. Do not suppress individual edges to enforce a neighbor cap.

Tested 18 radii (6, 6.5, 7, 7.5, 8, 8.5; 9.0–10.0 in 0.1 increments; 10.3 ly), each using eight deterministic greedy searches (seeds 0–7). For each radius:

1. Start with the component containing Sol. Other components cannot be connected by deleting nodes.
2. While a degree exceeds six, consider removing overloaded nodes or their neighbors, excluding Sol. Score each deletion by reduction in total excess degree divided by lost nodes, including nodes disconnected from Sol. Seed 0 uses unweighted scores; other seeds apply fixed 0.85–1.15 weights to explore choices.
3. Reinsert removed nodes when they reconnect to the retained component and keep all degrees <= 6. Repeat until no insertion succeeds.
4. Verify the full induced distance graph, including every within-range edge, is connected and has degrees 1–6. Keep the largest candidate found for each radius.

This is a reproducible heuristic, **not a proof of the maximum possible retained count**. It does not optimize name preservation, alternative-route resilience, or regional balance.

| Reach (ly) | Retained | Pruned from 136 | Neighbor range | Mean neighbors |
|---|---:|---:|---|---:|
| 7.5 | 85 | 51 | 1–6 | 3.41 |
| 8.0 | 82 | 54 | 1–6 | 3.63 |
| 8.5 | 88 | 48 | 1–6 | 3.66 |
| 9.0 | 105 | 31 | 1–6 | 4.04 |
| 9.2 | 107 | 29 | 1–6 | 4.02 |
| **9.4** | **108** | **28** | **1–6** | **4.31** |
| 9.5 | 106 | 30 | 1–6 | 4.28 |
| 10.0 | 102 | 34 | 1–6 | 4.35 |
| 10.3 | 98 | 38 | 1–6 | 4.31 |

Every row is one connected graph containing Sol. The 9.4 ly candidate has 233 undirected edges and retains about 79% of the current catalog. It is a reasonable **provisional reach setting**, pending review of retention priorities. It removes named entries including Wolf 359, Ross 154, Lacaille 9352, EZ Aqr, Procyon, Kruger 60, Ross 614, Van Maanen's Star, Wolf 1061, and Guniibuu. Only Sol is protected in this analysis.

All retained/removed indices and their original IDs/names are recorded in the JSON. No actual system deletion or ID renumbering has been applied to the baseline. Production generation will need an explicit derived dataset and migration strategy for dependent objects/artifacts. Once map-collision pruning is removed or the candidate pool changes, recompute these results before choosing a final reach.

## Demonstrated alternative: selected fixed routes

If retaining every existing system matters more than distance-only reachability, an alternative is a **10.3 ly maximum route length plus explicit route selection**. This changes the rule: being within the distance limit permits a route but does not automatically create one. The user has not yet adopted this policy; the physical/game rationale needs discussion.

An illustrative deterministic construction on this exact catalog:

1. Build a minimum spanning tree to ensure all systems can be reached from Sol through multiple hops.
2. Check its edges fit the radius and its degrees fit the cap. This tree has maximum degree four. An arbitrary future dataset is not guaranteed to pass these checks.
3. Consider remaining edges shortest-first. Add an edge if at least one endpoint has fewer than three neighbors, both have fewer than six, and the distance is <= 10.3 ly.

Result: **one connected network, 240 undirected routes, 1–6 neighbors per system, average 3.53**. Longest route: about 10.2823 ly. Neighbor-count distribution: 3 systems have one neighbor, 10 have two, 63 have three, 37 have four, 18 have five, and 5 have six.

This demonstrates feasibility for selected routes, not a solution using distance alone. A naive six-nearest-neighbors rule can break symmetry or disconnect the network. The illustrative construction checks the spanning tree first and preserves it. It guarantees baseline connectivity, not resilience against blockade or route closure.

If arbitrary within-range travel is preferred, retain the full distance graph: 10.3 ly connects all current systems, but some have 17 neighbors. Restricting only the displayed suggestions would not change actual reachability.

## Reproduction and verification

```sh
python3 -m universe_builder.analysis.reachability > /tmp/cx16-reachability.json
python3 -m unittest discover -s universe_builder/tests -v
python3 -m universe_builder verify-baseline
```

The adjacent JSON contains thresholds, graph statistics, input hashes, source-ID matches, pruning candidates, and the illustrative route summary. The script reads source/baseline data and writes its report to stdout. Graph tests cover disconnected groups without isolated vertices, inclusive/exclusive degree bounds, incompatible constraints, spanning-tree connectivity thresholds, and sparse-network limits. This analysis is narrower than full M1 generator validation.

Verification for this analysis: 20 unit tests pass (runner, reachability, pruning); all five baseline/source hashes remain unchanged. Full M1 validation remains pending.
