# Phase 0 — Star catalog

Status: existing implementation, validation pending (M1).
Implementation: `universe_builder/phases/phase_0_star_catalog.py`.

## Inputs and configuration

HYG CSV with distance and Cartesian coordinates in parsecs, plus optional catalog identifiers, proper name, spectral type, and luminosity/magnitude. Consult the implementation and archived detailed specification during the input-schema audit.

The preserved launcher configuration is radius 25 light-years, maximum 300 candidates before projection/collision removal, and 0.5 light-years per grid cell. Script defaults differ. Do not silently treat defaults as baseline provenance.

## Outputs

`phase_0/star_catalog.csv`:

```text
id,proper,dist_ly,grid_x,grid_y,spect
```

`phase_0/star_map.txt`: 100×100 text map, Sol marked `X`, other stars `*`, unused cells `.` and exterior cells spaces.

## Intended invariants

Sol is ID 0 at (50,50); system IDs and occupied cells are unique. Projected cells lie within 0–99. Distances are in light-years. Selection, synthetic names, collision priority, and ordering are deterministic. IDs are stable within a frozen catalog, not guaranteed across changed generation parameters.

Current exports retain 2D positions and distance from Sol, not full 3D positions. M1 must flag this limitation; a later schema decision is required for inter-system physical travel distances.

## Validation gate

Verify catalog parsing, conversion, radius limits, selection ordering, collision priority, Sol handling, edge coordinates, synthetic naming stability, and repeated-run equivalence. Compare against baseline and explain differences without replacing it. Audit input attribution.
