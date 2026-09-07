# Phase 4 — Historical simulation

Status: planned, implemented incrementally in M3–M6. No implementation yet.

## Inputs and outputs

Inputs: phase 3 initial state, physical data, versioned simulation settings, seed, and an explicit stopping condition.

Proposed outputs: `final_state.json`, `events.jsonl`, `metrics.csv`, and optional versioned checkpoints. Events carry identity, occurrence time, participants, location, causal factors, effects, and links to relevant earlier events. Information delivery time is separate from occurrence time. Record actual state transitions, not a chronology invented after simulation.

## Simulation structure

Begin with a small discrete-time model. Time units and same-time ordering must be specified before implementation. A candidate tick orders arrivals/information delivery, settlement production/consumption, research completion, decisions, and departures. Resource availability and political decisions must not depend accidentally on dictionary iteration order; document how simultaneous competition is resolved.

Use stable, purpose-specific random streams or keys. Record deterministic tie-breaking and serialization. Checkpoint replay should match an uninterrupted run when that feature is added.

## M3: travel and survival

- Population, industrial capacity, supplies, and explicit units.
- Decisions: explore, settle, resupply, invest; feasible actions compete for limited capacity.
- Expeditions have origin, destination, sponsor, payload, departure/arrival time, and vessel capability.
- Physical travel distances need an explicit 2D/3D decision; current CSVs cannot recover 3D pairwise distances.
- Supply delays, settlement viability, infrastructure development, failure, and persistent abandoned sites.
- Explain action selection and important rejected alternatives without logging every arithmetic operation.

## M4: technology and knowledge

Propulsion improvements require research or discoveries and deployment through construction/refits. Old vessels do not automatically acquire new performance. Initially messages move aboard ships: source, destination, content, observation date, and arrival date matter. Actors act only on available knowledge. Discovery, decoding, exploitation, and diffusion are different events.

## M5: political evolution

Sustained satisfaction/legitimacy pressures, autonomy demands, negotiation, alliances, conflict, independence, merger, and extinction. Political actions consume resources, have delays, and use inertia/recovery rules to avoid oscillation. Administrative and supply burdens counter unbounded expansion. Ownership changes do not delete settlements or rewrite cultural ancestry. Retain extinct factions for historical references.

## M6: culture and communications

Culture can persist, mix, migrate, and diverge; ownership and language remain separate. Names track original/current/alternate forms, language, naming actor, reason, and date. Start with authored, reviewable name pools; do not map ethnicity directly to aggression or intelligence.

Research or artifacts may unlock faster-than-light communication. Unlock is distinct from deployment: network reach, access, equipment, ownership, and message latency determine who benefits. Ship-carried news remains a fallback. Decide the mechanism and cost before implementation.

## Verification gates

Test causal scenarios: resource-limited settlement; home-government collapse during transit; treaty news arriving late; hidden artifact discovery; unequal technology; colony independence; culture persisting after conquest; communication outside network reach. Assert resource accounting, valid references, monotonic time, no knowledge from the future, deterministic replay, and bounded state values.

Run larger seed sweeps only after small scenarios are understandable. Political stability targets remain tunable and reviewed; avoid forcing a predetermined winner, faction count, or historical timeline.
