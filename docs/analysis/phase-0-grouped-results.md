# Phase 0 grouped-system result

**Accepted and closed as Phase 0 v1.** See [closeout](../PHASE_0_CLOSEOUT.md) for the current validation gate and Phase 1 handoff. The report below records generation-time findings.

Applied the agreed rules to the bundled HYG catalog. Output is a new dataset, not a replacement for the preserved historical baseline.

## Main result

| Measure | Result |
|---|---:|
| Neighborhood radius from Sol | 25 ly |
| Nearby cataloged stellar components | 167 |
| Candidate destinations after grouping | 133 |
| Named candidate destinations | 30 |
| Retained destinations | **99** |
| Retained cataloged components | **127** |
| Systems pruned | 34 |
| Named destinations retained | **30 of 30** |
| Member-star proper names retained | **34 of 34** |
| Selected fixed reach | **9.0 ly** |
| Connected components | **1** |
| Neighbors per destination | **1–6** |
| Average neighbors | **3.80** |
| Undirected travel connections | **188** |

The retained dataset has 75 destinations with one cataloged member, 20 with two, and four with three. These are counts of source records, not an assertion that the catalog lists every known companion.

## Grouping and travel assumptions

The HYG documentation identifies `comp_primary` as a component's primary-star ID and notes that grouping fields are used for Gliese stars. We follow those links before filtering and retain the original member records. [HYG field documentation](https://raw.githubusercontent.com/astronexus/HYG-Database/main/hyg/README.md).

HYG lists Proxima independently of the Alpha Centauri A/B pair. A versioned override groups all three into **Alpha Centauri**, based on the documented gravitational association. Rigil Kentaurus, Toliman, and Proxima Centauri remain member names. [ESO: Proxima's relationship to Alpha Centauri](https://www.eso.org/public/ireland/announcements/ann16089/).

The designated primary's x/y/z defines the system's travel position. This is an explicit approximation, not a calculated barycenter. Membership is never inferred from separation, similar names, or overlapping map symbols. Map placement does not prune destinations.

## Reach comparison

Selection prefers named destinations retained, then total destinations, then smaller reach and lower trial seed. Eight deterministic heuristic trials were evaluated at each of 16 reach values. Selected comparisons:

| Reach (ly) | Destinations retained | Named destinations retained |
|---|---:|---:|
| 7.5 | 84 | 23 / 30 |
| 8.0 | 81 | 23 / 30 |
| 8.5 | 83 | 24 / 30 |
| 9.0 | 99 | 30 / 30 |
| 9.2 | 98 | 29 / 30 |
| 9.3 | 101 | 29 / 30 |
| 9.4 | 101 | 29 / 30 |
| 9.5 | 98 | 29 / 30 |
| 10.0 | 85 | 28 / 30 |
| 10.3 | 89 | 28 / 30 |

**9.0 ly wins under named-system preference**: slightly larger retained subsets at 9.3–9.4 ly lose a named destination. This is the best candidate in this bounded heuristic search, not a proof of global optimality or a final freeze of game balance. Propulsion advances change speed and travel time without increasing reach.

## Sol's direct neighbors

| Destination | Distance (ly) |
|---|---:|
| Alpha Centauri | 4.320 |
| Barnard's Star | 5.945 |
| Wolf 359 | 7.799 |
| Lalande 21185 | 8.304 |
| Sirius | 8.601 |

## Named destinations preserved

Sol, Alpha Centauri, Barnard's Star, Wolf 359, Lalande 21185, Sirius, Ross 154, Ross 248, Ran, Lacaille 9352, Ross 128, EZ Aqr, Procyon, Struve 2398, Groombridge 34, Luyten's Star, Kapteyn's Star, Lacaille 8760, Kruger 60, Ross 614, Van Maanen's Star, Wolf 1061, Keid, Altair, Alsafi, Guniibuu, Achird, 82 G. Eri, 268 G. Cet, 96 G. Psc.

## Quality flags and limits

Three retained groups have catalog member coordinates more than 1 ly from the recorded primary: **Gl 338** (primary HYG 45211), **Gl 661** (83882), and **Gl 644** (82565). Their catalog associations are preserved; conflicting astrometry is flagged in the member/candidate files. Travel uses the primary position. These offsets are not being claimed as physically correct binary separations.

One excluded candidate, **GJ 3193 B** (118187), identifies itself as a secondary but points to itself as primary. The audit retains that ambiguity. No unseen companion was invented.

The catalog plus the sourced override may still omit or fail to associate other companions. New grouping evidence could change the graph. This pass does not implement per-star planetary orbits, stellar evolution, or a full source-quality audit.

## Deliverables

- [Star-system catalog](../../universe_builder/results/grouped-phase0-v1/phase_0/star_catalog.csv): stable source-based IDs, display positions, and primary 3D coordinates.
- [Member stars](../../universe_builder/results/grouped-phase0-v1/phase_0/stellar_members.json): all 127 records, original properties, aliases, and grouping provenance.
- [Travel connections](../../universe_builder/results/grouped-phase0-v1/phase_0/routes.csv): every qualifying undirected physical edge.
- [Map](../../universe_builder/results/grouped-phase0-v1/phase_0/star_map.txt): 100×100 display, one symbol per destination.
- [All candidates and pruning outcomes](../../universe_builder/results/grouped-phase0-v1/phase_0/candidate_systems.json).
- [Machine-readable summary](../../universe_builder/results/grouped-phase0-v1/phase_0/selection_summary.json).
- [Run manifest](../../universe_builder/results/grouped-phase0-v1/manifest.json): inputs, override, implementation and output hashes.

Paths in run provenance describe the machine where generation occurred; reproduction uses the repository-relative config command below.

## Reproduction and verification

```sh
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems.json --output /tmp/cx16-grouped-world --through 0
python3 -m unittest discover -s universe_builder/tests -v
python3 -m universe_builder verify-baseline
```

The output directory must be new. **37 tests passed**. All six phase-output files were byte-identical between independent runs. An independent export audit recomputed every 3D pair, checked that the route table contains exactly all pairs within 9 ly, checked degree bounds and connectivity from Sol, verified unique member identities and Alpha Centauri grouping, and checked unique display cells. All five preserved baseline/source hashes remain unchanged.

Grouped numeric IDs are primary HYG IDs, not contiguous runtime indexes. Do not join this catalog to historical object/artifact files. Phase 1's current primary-spectral model can read the leading catalog fields, but full downstream validation and multi-star object modeling remain separate work. This result completes the requested Phase 0 rule application and report; it does not mark all of M1 complete.
