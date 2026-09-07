# Phase 1 closeout — accepted production v1

Status: closed for the agreed natural-Spob generation scope. The user authorized promotion and validation with the discussed modeling choices. Phase 2 discussion and validation is next; M1 remains open until Phase 2 is accepted.

## Accepted result

[Production manifest](../universe_builder/results/physical-phase1-v1/manifest.json) and [object catalog](../universe_builder/results/physical-phase1-v1/phase_1/system_objects.csv).

- 170 systems; 274 natural Spobs: 208 planets (25 gas giants), 52 moons, 14 asteroids.
- Distribution: 15 empty systems; 70 with one; 58 with two; 20 with three; seven with four; none with five.
- 155 systems have natural objects; no landing, habitation or artificial station claims.
- Sol retains Earth, Luna, Mars and Ceres. Represented parents and moons share the total-body budget. Primary spectral type supplies the stellar attribute approximation.
- No overlapping local cells; deterministic parent-first collision resolution is part of production generation.

## Promotion and verification

The standard `python3 -m universe_builder generate ... --through 1` pipeline now uses the curated generator. Total-body weights are explicit in `configs/grouped_systems_cube.json`. The cap includes moons; Sol retains its four-object exception. Historical primary-budget code is explicitly named `generate_legacy_objects_for_system` for comparisons, and experimental density calls delegate to production.

All 55 tests passed. The reusable `python3 -m universe_builder.validation.phase1 universe_builder/results/physical-phase1-v1` independently checks output integrity, source IDs, parent references, types, ranges, budgets, moon limits, Sol and unique coordinates, alongside Phase 0 validation. Corruption tests reject local overlaps even after updating the checksum. Tests also cover forced budgets, cap behavior, seeds, invalid weights and replay.

The production Phase 1 CSV is byte-identical to corrected cube trial v3. A second full generation matches all seven Phase 0/1 output files byte-for-byte. The six Phase 0 files also match cube v2 exactly. All five preserved source/baseline files passed the preservation check. Older datasets, runtime export and their manifests remain untouched.

## Handoff and limits

Use the accepted production object catalog for Phase 2; retain source-based identities until export. The existing runtime export refers to corrected trial v3, whose object CSV is identical; it remains a separately versioned physical export and has not been silently rebuilt.

Habitability/risk/resources are gameplay abstractions, not verified physical measurements. Per-member stellar orbits, settlements, landing eligibility and artificial satellites remain deferred. Unique map cells do not establish sprite spacing. Local identities are stable within this generated world; changed generation rules may require a new world version.

Discuss Phase 2 placement eligibility, abundance, Sol policy and discovery semantics before accepting an artifact dataset. No Phase 2 output was generated or accepted as part of this closeout.
