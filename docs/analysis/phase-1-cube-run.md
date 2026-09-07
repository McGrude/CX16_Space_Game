# Phase 1 — Cube runs

Generated at the user's request from the preserved 170-system cube catalog, using the revised total-body weights (0–5: 10%, 35%, 35%, 15%, 4%, 1%) and seed 42. Sol retains Earth, Luna, Mars and Ceres. No artificial satellites are generated.

Result: **274 natural Spobs**: 208 planets (including 25 gas giants), 52 moons and 14 asteroids. Distribution by system: 15 empty, 70 with one, 58 with two, 20 with three, seven with four, none with five. Thus 155 systems contain at least one natural Spob; this does not establish landing eligibility or habitation.

The revised density implementation checks object budgets, IDs, parent references, field ranges and per-system replay during generation. Three inherited local-coordinate overlaps remain (system IDs 91484, 118447, 105913). This is a generated dataset for review, not closure of Phase 1 validation or promotion of the experimental implementation to the main launcher.

- [Objects](../../universe_builder/results/phase1-cube-v2/system_objects.csv)
- [Summary](../../universe_builder/results/phase1-cube-v2/summary.json)
- [Manifest and hashes](../../universe_builder/results/phase1-cube-v2/manifest.json)
- [Configuration](../../universe_builder/configs/phase1_density_cube_v2.json)
- [Universe text map](../../universe_builder/results/grouped-phase0-cube-v2/phase_0/star_map.txt)

Phase 1 adds local objects; it does not change the universe map or travel graph. The map remains the cube Phase 0 output.

Reproduce into a new directory:

```sh
python3 -m universe_builder.analysis.phase1_density --config universe_builder/configs/phase1_density_cube_v2.json --output /tmp/my-new-phase1-cube-run
```

## Collision fix — Phase 1 v3

The prior v2 files above remain preserved. Current corrected output is [phase1-cube-v3/system_objects.csv](../../universe_builder/results/phase1-cube-v3/system_objects.csv), with [summary](../../universe_builder/results/phase1-cube-v3/summary.json) and [manifest](../../universe_builder/results/phase1-cube-v3/manifest.json). Reuse the same configuration with a new output path to reproduce it using the corrected implementation.

Three moon symbols moved one cell:

| System ID | Object ID | Previous cell | New cell |
|---|---|---|---|
| 91484 | 1 | (20,24) | (20,23) |
| 118447 | 1 | (26,20) | (26,19) |
| 105913 | 1 | (27,20) | (27,19) |

No overlaps remain. Comparison of all 274 CSV rows confirms that only these coordinates changed; every other field and the count distribution are identical. All 48 tests passed. A fresh independent run produced byte-identical CSV, summary and manifest files. The universe star map remains unchanged. Phase 1 design/acceptance work beyond this defect remains open.
