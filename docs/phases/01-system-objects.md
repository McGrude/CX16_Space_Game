# Phase 1 — Natural system objects

Status: existing implementation, validation pending (M1).
Implementation: `universe_builder/phases/phase_1_system_objects.py`.

## Inputs and configuration

Phase 0 star catalog; required fields `id,proper,spect`. Preserved launcher settings: global seed 42 and `max_objects_per_system` 5. Audit the exact cap semantics against the implementation: the intended primary count is not a cap on all moons plus primaries.

## Output

`phase_1/system_objects.csv`:

```text
system_id,object_id,name,class,parent_object_id,is_moon,local_x,local_y,ore_richness,fuel_richness,habitability,risk
```

Classes: RP rocky planet, DP desert planet, IC ice planet, GG gas giant, RM rocky moon, IM icy moon, AS large asteroid.

## Intended invariants

Natural identity is the pair `(system_id, object_id)`. Parent references resolve within the same system. Systems may contain no natural objects. Weighted generation creates 0–5 primaries, at most one large asteroid, and optional moons. Sol has the special Earth/Luna/Mars/Ceres arrangement; audit precisely which attributes are fixed versus generated.

Local coordinates are 0–49, ore/fuel richness 0–3, habitability/risk 0–100, and `is_moon` is 0 or 1. Spectral type influences habitability/risk. Per-system seed derivation must be reproducible.

## Validation gate

Check parent references, unique identities and coordinates as required by layout rules, field ranges, zero-object systems, Sol, moon eligibility, object caps, seed effects, repeated runs, and baseline differences. Physical object names are not civilization settlement names; preserve their identity through later cultural naming.
