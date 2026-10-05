# Project specification

Status: current direction agreed during repository planning, September 2026.

## Two complementary projects

1. A Commander X16 space trading and exploration RPG with turn-based combat, ship management, crew, upgrades, missions, and faction relationships.
2. A configurable offline world generator inspired by Dwarf Fortress history generation. It simulates the conditions that create a world before the player enters it.

The simulator runs on a development computer. The X16 consumes a compact exported starting state and relevant historical information. Continuing the full historical simulation during gameplay is not currently a requirement.

## Game interface direction

The game interface is text-only, resembling a vintage terminal console. No sprites are planned. The proposed palette is eight base colors with a bold/bright bit for sixteen color variants. Game text is expected to use 7-bit ASCII; borders and similar interface decoration may use platform-specific character glyphs.

On Commander X16, use available character glyphs for borders and other text-cell decoration. Possible Mac/PC terminal versions may use a custom font or a CP437-like glyph repertoire; exact encoding, font and terminal mappings remain undecided. Keep ASCII content distinct from platform-specific decorative glyph rendering. This is future interface direction, not a new implementation task or a change to the physical-world datasets.

### Planned port menu

After the history simulation, the playable game should present a simple text port menu with these service interfaces:

- Trade Goods Market: commodity trading.
- Ship Services: ships, ship upgrades and repairs.
- Mission Board: available jobs.
- Possible Trade Union interface: purpose and organization remain to be defined.
- Possible Faction interface: faction missions.
- Possible Black Market interface: access follows the accepted local-contact or criminal-reputation requirement where a black market exists.

The last three interfaces are tentative. This describes future game presentation, not a simulation interface or an implemented screen. Keep the menu simple; exact layout, service availability and how hidden services are revealed remain open. A proposed trade union interface does not establish a new faction or equate that organization with the Belt Workers' Commonwealth.

## Accepted simulation direction

- Begin on April 5, 2148, with the joint Mars artifact discovery and eight Earth political blocs. First operational interstellar ships are targeted around 2153. The current map is Atlantic Union, Eurasian Directorate, Sino Cooperative Sphere, Indo-Pacific Compact, Indian Confederation, West Asian League, African Union and Southern Commonwealth. See `docs/phases/03-initial-scenario.md` for current affiliations; Atlantic, Sino and Indo-Pacific jointly sponsor Luna/Mars and co-discover the artifact; dates and development timing are preserved. Detailed starting assets remain under design.
- Slow early travel constrains settlement, trade, military reach, and political control. Research and discoveries increase speed and reduce travel times; they do not increase reach. The physical reachability network remains fixed as propulsion technology advances.
- Initial communication includes ship-carried information and ordinary light-speed radio reports from survey probes. Probe findings reach remote sponsors only after propagation delay. Faster-than-light communication requires its own research/artifact development and infrastructure; propulsion improvements do not automatically speed radio.
- Initial actors also include loosely affiliated criminal groups sometimes used by blocs, the Belt Workers' Commonwealth controlling Ceres, the decentralized Mesh (also called the Null Collective), and two named commercial shipping firms, Meridian and KVI, alongside hundreds of other operators represented in aggregate. The named firms are intended as recognizable game actors and may also be modeled during history generation. Additional companies may emerge in simulation; no initial religious factions are planned. Organization membership and relationships are distinct from territorial government.
- Factions explore, establish outposts and colonies, develop technology, forge and break alliances, merge, split, and become extinct. The factions present at game start are outputs, not a fixed roster.
- Every artifact-associated technology is independently researchable. Artifact study may accelerate development; no technology requires exclusive access to a site. The Mars find at the scenario start catalyzes initial interstellar capability. This later scenario decision supersedes the preserved Phase 2 handoff's pre-epoch timing.
- No living aliens. Ancient artifacts exist physically before discovery, but actors must discover and learn about them before acting on them.
- Cultures and languages influence names and institutions. Culture is distinct from political ownership and can persist through conquest or independence. Avoid assigning fixed behavior from ancestry or language alone.
- Place names have historical authorship: who named a place, when, and why. Original, official, local, and foreign names can coexist.
- Settlements, populations, institutions, names, and ruins may survive their parent faction.
- Binary and multiple-star systems are one destination. Preserve member-star names and properties; use catalog membership and sourced overrides, never proximity alone.
- Display placement must not discard physical systems. Nearby free cells resolve overlaps; catalog proper names receive retention preference over unnamed entries. Sol is mandatory.
- Reachability is an allowed system-selection/pruning criterion. The aim is a single connected network including Sol, with 1–6 directly reachable systems per retained system; the current fixed reach is 9 ly with named-preferred deterministic system pruning. The current geographic selection is a 50 ly cube centered on Sol (±25 ly on each HYG axis).
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

Grouped schema 2 exports primary 3D positions separately from approximate display coordinates and computes travel distances from them. The historical baseline and legacy schema 1 lack full 3D positions. Never infer pairwise distances from radial distance alone. The current grouped result uses a 9.0 ly reach and preserves all named destinations; see the Phase 0 contract.

The old 92-system game dataset and older future-faction descriptions are archived design inputs, not authoritative simulation output.
