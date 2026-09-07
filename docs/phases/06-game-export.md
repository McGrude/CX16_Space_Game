# Phase 6 — Commander X16 export

Status: planned, M8. No implementation yet.

## Inputs and proposed outputs

Input: approved phase 5 snapshot and a versioned runtime export profile.
Output: a manifest plus compact game tables for systems, places, factions, names/history, economy, and mission seeds. File formats, sizes, bank usage, and loader interfaces must be finalized with runtime requirements; do not adopt old CSV formats without a compatibility decision.

## Responsibilities

Map simulator IDs to stable game IDs through an explicit mapping table. Preserve enough historical context for exploration without requiring the X16 to run the offline simulator. Separate static data from mutable save state. Resolve simulation dates versus the prototype's 12×28 calendar. Respect source-data license attribution in exported catalog-derived materials.

Do not merge `game/data/legacy/` directly: it uses different system IDs, faction definitions, and schemas.

## Exit criteria

Export validator checks references, string encodings/lengths, numeric ranges, ordering, visibility, size budgets, schema versions, and mapping stability. A minimal real loader reads a representative world in the X16 emulator. Record timings and memory consumption; export success alone is not proof the runtime can use it.
