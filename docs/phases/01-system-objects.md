# Phase 1 — Natural system objects

Status: **closed — accepted production v1**, at the user's direction to promote and validate the revised model. See [closeout](../PHASE_1_CLOSEOUT.md). Phase 2 is next; M1 remains open until it passes validation.

Implementation: `universe_builder/phases/phase_1_system_objects.py`. Supported configuration: `universe_builder/configs/grouped_systems_cube.json`. Accepted run: `universe_builder/results/physical-phase1-v1/`.

## Accepted model

Generate a curated set of significant natural Spobs rather than a complete planetary inventory. Planets and represented moons share one per-system budget, including any represented parent body. Multiple stars do not multiply that budget. Use the designated primary star's spectral type for attributes; explicit per-member stellar orbits are deferred.

| Total natural Spobs | Probability |
|---|---:|
| 0 | 10% |
| 1 | 35% |
| 2 | 35% |
| 3 | 15% |
| 4 | 4% |
| 5 | 1% |

The configurable cap includes moons. Sol is an explicit exception to random selection and smaller caps: Earth, Luna, Mars and Ceres, with Luna parented to Earth. Sol's names/classes/relationship are fixed; attributes and display coordinates use deterministic model functions.

Generate a planet, then eligible moons clipped to the remaining budget, repeating until full. Preserve existing planet-class and moon-class probabilities. Optional asteroid replacement applies only to a moonless primary when at least two primaries exist. At most one asteroid per system. The legacy primary-budget implementation remains explicitly named for historical comparison; the main CLI uses the curated model.

Artificial satellites and stations belong to later civilization generation and are excluded. A natural Spob is not automatically landable or inhabited. Terminology is **Spobs**.

## Inputs and outputs

Input Phase 0 CSV requires `id,proper,spect`. Source-based system IDs remain stable offline; compact runtime indexes are assigned at export. Duplicate/invalid IDs or absent Sol are errors.

Output `phase_1/system_objects.csv`:

```text
system_id,object_id,name,class,parent_object_id,is_moon,local_x,local_y,ore_richness,fuel_richness,habitability,risk
```

Identity is `(system_id,object_id)`; local IDs are contiguous from zero. Empty parent means no parent. Classes: RP rocky planet, DP desert planet, IC ice planet, GG gas giant, RM rocky moon, IM icy moon, AS large asteroid. Moons refer to eligible planets in the same system. Ore/fuel range 0–3; habitability/risk 0–100; coordinates 0–49.

## Local display placement

Generate preferred positions, then process parents before moons, ordered by stable object ID in each group. Keep free cells; move collisions to the nearest free cell by squared Euclidean distance, with ties by row then column. Stay inside 50×50; never delete Spobs or modify physical attributes. Reject capacity overflow. No minimum sprite spacing beyond unique cells is implied.

## Reproduction and verification

```sh
python3 -m universe_builder generate --config universe_builder/configs/grouped_systems_cube.json --output /tmp/new-physical-world --through 1
python3 -m universe_builder.validation.phase1 universe_builder/results/physical-phase1-v1
python3 -m unittest discover -s universe_builder/tests -v
```

Output directories must be new. The standard manifest records config, interpreter, input and implementation hashes, completion and output checksums. Validation independently checks Phase 0, the Phase 1 checksum, identities, references, classes, field ranges, moon limits, budgets, Sol and unique local cells.

Accepted result: 274 Spobs across 170 systems, byte-identical to corrected cube trial v3. All 55 tests pass. Historical trial reports and outputs remain preserved and are not the current specification.
