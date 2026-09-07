# Phase 0 — Stellar-system catalog

Status: **accepted — cube v2**, incorporated unchanged into accepted production run `physical-phase1-v1`. The spherical v1 artifact remains preserved. See [cube v2 results](../analysis/phase-0-cube-results.md); the [v1 closeout](../PHASE_0_CLOSEOUT.md) is historical. M1 remains open.

Supported configuration: `universe_builder/configs/grouped_systems_cube.json` (schema 2). The original `grouped_systems.json` retains the spherical settings.
Implementation: `phase_0_stellar_systems.py`, `system_grouping.py`, and shared layout/pruning helpers.

## Applied rules, in order

1. **Read HYG identities, grouping fields, names, and physical data.** Duplicate/invalid source IDs, missing primary links, and cycles are errors. Invalid astrometry is flagged; no invented coordinates are used. Unusable primary positions cannot enter the neighborhood, but known companion records remain attached to a valid system.
2. **Group before geographic selection.** Follow `comp_primary` references and apply versioned, sourced membership overrides. Never merge stars by proximity, similar names, or map position. Alpha Centauri combines A, B, and Proxima using the documented override. Keep every cataloged member and original properties, including members outside the chosen region when their primary is inside.
3. **Choose a representative position.** Use the designated primary's original x/y/z converted to light-years. This is a travel approximation, not a calculated center of mass. Catalog offsets greater than 1 ly are flagged for review, not used to sever recorded associations.
4. **Select the neighborhood.** Use a **50 ly cube centered on Sol**, aligned with the catalog x/y/z axes: **−25 <= x,y,z <= +25 ly**, inclusive. Selection uses the primary position; radial distance remains exported but is not the cutoff. Cube corners are about 43.30 ly from Sol. Require valid Sol at the origin. The configurable **300-system** candidate budget prefers Sol, systems with at least one actual catalog proper name, then nearer systems. Synthetic names do not confer preference. The current 225 candidates are below the cap.
5. **Evaluate fixed reach.** Each tested radius connects every pair of candidate systems within that true 3D distance. Technology changes speed/travel time, not reach. Cube v2 fixes reach at **9.0 ly** (a singleton candidate list); the original sphere config retains its historical reach sweep.
6. **Prune systems for connectivity and degree.** Keep Sol and one connected component. Require **1–6 neighbors per retained destination**. Heuristic removals first minimize named-system losses (including disconnected branches), then reduce excess degree per lost system. Reinsert feasible named systems first. Evaluate eight deterministic trials at each reach. Choose the result retaining the most named systems, then most total systems, then smaller reach, then lower seed. All within-reach edges remain; this is system pruning, not selective route suppression.
7. **Preserve identities.** `system_key=hyg:<designated-primary-id>`; numeric `id` is that primary's HYG ID, with Sol 0. These IDs are sparse, stable across pruning/reach changes with the same source and membership policy, and not compact X16 indices. Source upgrades or membership changes require migration. Member stars retain their own HYG IDs. Downstream object keys remain `(system_id, object_id)`.
8. **Lay out the map without removing systems.** Sol at (50,50); other projected x/y positions assigned to nearest free cells, deterministic ties by row/column. Scale currently 0.5 ly/cell. Cube maps have a square dot background without the spherical mask. The 100-cell even-sized grid is approximate: Sol remains at (50,50), and boundary positions use the nearest available cell. Physical coordinates stay unchanged. Full display capacity is an error, never silent pruning.
9. **Export and independently check the network.** Recompute every physical edge and all degrees/connectivity from selected system coordinates. Write provenance and a candidate audit including pruned systems. Preserve the old baseline.

## Output schema 2

`star_catalog.csv` (one row per destination):

```text
id,proper,dist_ly,grid_x,grid_y,spect,system_key,primary_hyg_id,member_count,is_named,x_ly,y_ly,z_ly
```

- `spect`: representative primary spectral type; full member types remain in the member file.
- `member_count`: cataloged rows in this destination, not a claim that HYG contains every known companion.
- `stellar_members.json`: all retained members' raw source properties, names, positions, grouping provenance, and quality flags.
- `candidate_systems.json`: all neighborhood candidates, membership IDs, stable identities, coordinates, names, and retained/pruned status.
- `routes.csv`: one row per undirected edge (`from_system_id,to_system_id,distance_ly`).
- `selection_summary.json`: candidate/retained counts, named losses, reach comparisons, degree distribution, and quality flags.
- `star_map.txt`: 100×100 ASCII map; X=Sol, *=destination.
- Parent `manifest.json`: config, input/override/implementation hashes, interpreter version, completion status, and output hashes.

## Current result and reproduction

[Grouped results](../analysis/phase-0-grouped-results.md): Historical spherical v1: 133 candidates, 99 retained. [Cube v2](../analysis/phase-0-cube-results.md): **225 candidates from 274 catalog entries; 170 retained destinations containing 210 entries at 9.0 ly. 38/39 named destinations and 43/44 named members retained.**

```sh
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems_cube.json --output /tmp/cx16-grouped-world --through 0
```

Output directory must be new. `baseline.json` (schema 1) remains a legacy single-star-entry mode for comparison; it does not implement grouping/reach pruning. Historical 136-entry baseline files remain untouched.

## Documented limits and future changes

Membership is only as complete as HYG plus reviewed overrides. An unlinked entry is not proven single. Catalog astrometry discrepancies remain recorded. No mass-weighted barycenters, orbit evolution, or companion invention. Phase 1 can consume the leading ID/name/spectral fields, but its current natural-object model uses the primary spectral type and does not yet model planets orbiting particular stellar members. Export to X16 still needs a compact index mapping.

Phases 0–1 are now accepted; continue M1 with Phase 2 discussion and validation. Additional astronomical source enrichment or changes to the accepted Phase 0 rules reopen Phase 0 deliberately; they are not prerequisites for this accepted game dataset. Historical single-entry reach analyses remain available in `docs/analysis/` but no longer set current reach recommendations.

## Acceptance verification

```sh
python3 -m universe_builder.validation.phase0 universe_builder/results/grouped-phase0-cube-v2
```

The reusable verifier checks output hashes, schema/identity/reference consistency, configured geographic bounds, every physical route, degree bounds, connectivity, member uniqueness, candidate selection, map cells and summary counts. Cube v2 passes; all 46 current tests pass. A separate replay matches all six output files. The original spherical artifact also still validates.
