# Phase 6 — Commander X16 export

Status: full export planned, M8. Physical-world runtime ID export is implemented as an early subset; no X16 loader or save reader yet.

## Inputs and proposed outputs

Input: approved phase 5 snapshot and a versioned runtime export profile.
Output: a manifest plus compact game tables for systems, places, factions, names/history, economy, and mission seeds. File formats, sizes, bank usage, and loader interfaces must be finalized with runtime requirements; do not adopt old CSV formats without a compatibility decision.

## Responsibilities

Map simulator IDs to stable game IDs through an explicit mapping table. Preserve enough historical context for exploration without requiring the X16 to run the offline simulator. Separate static data from mutable save state. Resolve simulation dates versus the prototype's 12×28 calendar. Respect source-data license attribution in exported catalog-derived materials.

Do not merge `game/data/legacy/` directly: it uses different system IDs, faction definitions, and schemas.

## Exit criteria

Export validator checks references, string encodings/lengths, numeric ranges, ordering, visibility, size budgets, schema versions, and mapping stability. A minimal real loader reads a representative world in the X16 emulator. Record timings and memory consumption; export success alone is not proof the runtime can use it.

## Implemented runtime identity profile v1

Command: `python3 -m universe_builder export-runtime --phase0 <phase0-run> --phase1 <phase1-run> --output <new-directory>`.

Current artifact: `universe_builder/results/runtime-cube-v1/`, built from cube Phase 0 v2 and Phase 1 v3. Offline artifacts keep source-based IDs. Runtime system IDs are contiguous bytes: Sol = 0, then ascending numeric source ID. Spob indexes are contiguous per system in ascending source object-ID order. All exported system, route, Spob and parent references are translated consistently. Source IDs and system keys in the diagnostic systems CSV are provenance only. Mapping CSVs permit reverse lookup.

Indexes 0–254 are usable; 255 means no reference. Export rejects more than 255 systems or more than 255 Spobs in one system. Current indexes are 0–169, with 274 Spobs in total.

Packed files (raw bytes, no implicit BASIC load-address prefix):

- `neighbors.bin`: seven bytes per system, in runtime system order: neighbor count followed by six destination slots, ascending runtime ID, unused slots padded with 255. Current size: 1,190 bytes.
- `spob_refs.bin`: three bytes per Spob, sorted by runtime system/object ID: system index, local object index, parent local index (255 if absent). Current size: 822 bytes. Attributes and strings remain in diagnostic CSVs until the full export profile is designed.
- `world_header.bin`: 37 bytes: ASCII `CX16` (4), format version (1), raw SHA-256 world ID (32).

`manifest.json` records format version 1, the full hexadecimal world ID, counts, sentinel value, input hashes, exporter hash and output checksums. World identity hashes canonical JSON containing input hashes, format version, mapping and exporter hash; it is deterministic, content-based and intentionally changes when those inputs or implementation change. Directory names are human labels, not compatibility identifiers.

Future saves must carry the same header and compare both format version and all 32 world-ID bytes before interpreting any runtime indexes. A mismatch requires rejecting the save or explicit migration using the old/new mappings; never reinterpret indexes silently. The save reader and migration are not implemented yet. Regeneration may renumber indexes; stability is scoped to a specific world version.

Tests cover sparse-ID translation, local parent translation, sentinel padding, capacity rejection, deterministic export, binary sizes and world-header consistency. All 51 tests pass. Complete Phase 6 still requires civilization/history/artifact references, packed attributes, strings, visibility rules, licensing delivery and an emulator-tested loader.
