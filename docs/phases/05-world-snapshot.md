# Phase 5 — World inspection and playable snapshot

Status: planned, M7. No implementation yet.

## Inputs and proposed outputs

Input: phase 4 state, event ledger, metrics, and selected stopping point.
Outputs: a versioned `world_snapshot.json`, human-readable `history.md`, balance summaries, and `opportunities.json` containing mission/trade/exploration seeds grounded in actual entities and events.

## Responsibilities

Expose why settlements exist, who owns them, what they need, which relationships are disputed, and which sites are abandoned. Preserve old names and extinct factions in records. Differentiate author inspection (may show all truth) from player-visible knowledge. Do not reveal every hidden artifact through an exported public gazetteer.

A shortage may seed a delivery opportunity; a contested claim may seed a diplomatic or salvage mission. Do not invent causally unrelated wars, ruins, or arbitrary mission locations to decorate the world. Detailed prices and mission mechanics depend on the eventual runtime; this phase supplies grounded state and opportunities.

## Exit criteria

All historical and opportunity references resolve. Snapshot corresponds exactly to its stop time. Author reports expose health metrics and causal histories; player-facing output respects visibility. Seed sweeps identify runaway expansion, fragmentation, collapse, and stagnation, with documented parameter choices and reviewed outcomes.
