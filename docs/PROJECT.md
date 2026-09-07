# Project specification

Status: current direction agreed during repository planning, September 2026.

## Two complementary projects

1. A Commander X16 space trading and exploration RPG with turn-based combat, ship management, crew, upgrades, missions, and faction relationships.
2. A configurable offline world generator inspired by Dwarf Fortress history generation. It simulates the conditions that create a world before the player enters it.

The simulator runs on a development computer. The X16 consumes a compact exported starting state and relevant historical information. Continuing the full historical simulation during gameplay is not currently a requirement.

## Accepted simulation direction

- Begin on Earth at an epoch when interstellar travel is just becoming practical. Initial political powers are analogous to major Earth powers; exact identities and date remain open.
- Slow early travel constrains settlement, trade, military reach, and political control. Research and discoveries can reduce travel times.
- Initially messages travel aboard ships. Faster-than-light communication can be unlocked by research or an alien artifact; it is distinct from propulsion capability.
- Factions explore, establish outposts and colonies, develop technology, forge and break alliances, merge, split, and become extinct. The factions present at game start are outputs, not a fixed roster.
- No living aliens. Ancient artifacts exist physically before discovery, but actors must discover and learn about them before acting on them.
- Cultures and languages influence names and institutions. Culture is distinct from political ownership and can persist through conquest or independence. Avoid assigning fixed behavior from ancestry or language alone.
- Place names have historical authorship: who named a place, when, and why. Original, official, local, and foreign names can coexist.
- Settlements, populations, institutions, names, and ruins may survive their parent faction.
- Runs must be reproducible from recorded inputs, settings, and implementation versions.

## Architecture

Phases 0–2 establish physical geography and hidden artifacts. Phase 3 initializes an Earth scenario. Phase 4 advances that scenario through time. Phase 5 inspects histories and produces a playable snapshot and opportunities. Phase 6 exports data for the X16.

Research, culture, politics, and economics interact inside the historical simulation; they are not independent one-pass generators. Phase 4 is developed through several milestones to keep each addition explainable.

Keep three concepts separate:

- Physical truth: actual locations, resources, artifacts, and events.
- Actor knowledge: dated information available to each decision-maker.
- Game presentation: what a player can learn through charts, dialogue, records, and exploration.

## Stability and explanation

Actions require capacity, resources, and time. Political changes follow sustained pressures and have transition costs. Randomness introduces variation within explicit rules. Supply commitments, administration, and travel constrain growth; setbacks should have identifiable causes. Major events record causal factors and affected entities.

Tunable parameters need units and bounds. Scenario tests and seed sweeps should reveal monopolies, fragmentation, universal collapse, runaway growth, and histories in which nothing happens. Balance targets are design choices to establish experimentally, not claims of real-world prediction.

## Existing foundation and limits

The preserved catalog has 136 systems within approximately 25 light-years, 405 natural objects, and seven artifact sites. These are inventory counts, not proof of scientific or algorithmic correctness. Former launch scripts use different settings from some generator defaults and old design documents.

Current star CSV coordinates are a 2D map projection, plus distance from Sol. They do not retain full 3D positions. Before historical travel is implemented, choose projected gameplay distances or extend the physical schema to retain true pairwise distance information. Do not infer 3D pairwise distances from radial distance alone.

The old 92-system game dataset and older future-faction descriptions are archived design inputs, not authoritative simulation output.
