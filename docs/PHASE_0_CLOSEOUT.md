# Phase 0 closeout — accepted v1

**Historical v1 closeout. Phase 0 has since been reopened for [cube v2](analysis/phase-0-cube-results.md); this document records the preserved spherical acceptance.** The user requested closeout after reviewing the grouped-system result. Phase 1 design review and validation is next; M1 remains open for phases 1–2.

## Accepted result

- **99 interstellar destinations**, containing **127 cataloged stellar components**.
- **9.0 ly fixed reach**, **188 undirected routes**, one connected graph, **1–6 neighbors** per destination.
- All **30 named destinations** and **34 member-star names** preserved.
- Grouping before selection; Alpha Centauri A/B/Proxima form one destination.
- Primary-star 3D position for travel; independent 100×100 display layout with no map-driven deletion.
- Stable source-based system identities; Sol is ID 0.

The exact version is identified by the [accepted manifest](../universe_builder/results/grouped-phase0-v1/manifest.json), including input, membership override, implementation and output hashes. The generating configuration is [grouped_systems.json](../universe_builder/configs/grouped_systems.json). It records the evaluated reach candidates; **9.0 ly is the accepted result**, not a research result that downstream phases should reselect.

## Verification evidence

- **41 tests passed**.
- Reusable artifact verifier passed: source-based IDs, schemas, output hashes, member/reference consistency, full physical edge set, degree bounds, Sol connectivity, map positions, and summary counts.
- Corruption tests reject changed bytes, omitted physical routes even after updating the checksum, and duplicated member assignments.
- Two independent generation runs produced identical bytes for all six Phase 0 output files.
- Current source, membership override and generator hashes still match the accepted run.
- All five historical baseline/source hashes remain unchanged.

```sh
python3 -m unittest discover -s universe_builder/tests -v
python3 -m universe_builder.validation.phase0 universe_builder/results/grouped-phase0-v1
python3 -m universe_builder verify-baseline
```

The artifact verifier validates the exported dataset and output checksums. Input and implementation hashes in the manifest describe generation provenance; they are checked separately and do not prevent future implementation changes.

## Documented limitations carried forward

| Item | Disposition |
|---|---|
| Gl 338, Gl 661, Gl 644 have inconsistent recorded member positions | Keep source associations and raw values with flags; travel uses the designated primary |
| GJ 3193 B has incomplete primary linkage | Preserve the audit flag; it was not retained in the final dataset |
| Some companions may be absent or unlinked in HYG | Member counts describe cataloged records; no unseen companions are invented |
| Representative system coordinates | Primary coordinates are an explicit approximation, not a mass-weighted barycenter |
| Pruning | Deterministic bounded heuristic; no claim of global optimality |
| Numeric identities | Sparse primary HYG IDs are offline keys; compact X16 indexes belong to later export |

These limitations are documented for the accepted game dataset. Correcting astrometry, adding associations, changing reach or membership, or enriching the source is a deliberate future Phase 0 revision. Full stellar/orbital realism is outside this closed scope.

## Phase 1 handoff

Use [the accepted catalog](../universe_builder/results/grouped-phase0-v1/phase_0/star_catalog.csv) and [member data](../universe_builder/results/grouped-phase0-v1/phase_0/stellar_members.json) as inputs. Do not regenerate Phase 0 merely to start Phase 1. Never combine this catalog with historical phase 1/2 rows: their ID spaces and physical selections differ.

Before extending the natural-object model, discuss whether objects explicitly orbit member stars or use the existing primary-spectral approximation. Keep natural object IDs scoped by system. Validate Sol's special case, sparse system IDs, deterministic seeds, zero-object systems, moons/parents, coordinate/range bounds, and independent outputs. Keep the accepted 9 ly route network fixed as technology advances.

## Reopening policy

Preserve accepted v1 unchanged. If a future change is needed, create a separately versioned dataset, explain differences, rerun the validators, and deliberately migrate dependent data. Do not silently update accepted files or erase quality flags to obtain a passing result.

See [the result summary](analysis/phase-0-grouped-results.md) for the full counts, reach comparison, sources, and export links.
