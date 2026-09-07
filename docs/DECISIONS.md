# Decisions and open questions

## Accepted

| Decision | Basis |
|---|---|
| Offline history precedes gameplay | User wants both a parameterized generator and an explorable generated world |
| Start at the dawn of interstellar travel | User direction |
| Earth powers seed the simulation; future factions emerge | User direction |
| Propulsion advances increase speed / reduce travel time; they do not increase reach | User direction: fixed reachability simplifies the network |
| Reachability constraints may prune systems | User accepts removing systems to obtain useful connectivity and neighbor counts |
| Display collisions do not prune systems | User direction: remove the earlier map-collision pruning |
| Recognizable named stars receive retention preference | User direction; use catalog proper names initially, not generated names |
| Binary/multiple stellar systems are one interstellar destination | User direction; retain member stars and names inside the destination |
| Phase 1 represents a curated set of significant local objects | User prefers sparse gameplay locations over a full planetary inventory |
| Normal natural-object counts are 0–3, mostly 1–2; 4–5 are rare | User direction; numerical probability weights remain proposed |
| Planets and represented moons share the Phase 1 natural-body budget | The sparse count applies to curated natural locations, not primaries plus unbounded moons |
| Artificial satellites/stations belong to civilization generation and are rare | User direction; planets and moons are typical civilization destinations |
| Messages initially move with ships; later research/artifacts unlock faster communication | User direction |
| Culture, language, and historical naming matter | User direction |
| No living aliens | Existing world-generation rule retained |
| Retain existing MIT license | Repository already has an MIT license |
| Preserve phase 0–2 output and validate before expanding | Repository reorganization scope |

## Accepted Phase 0 v1 settings

The grouped configuration applies catalog membership links plus a sourced Alpha Centauri override, groups before radius selection, uses designated primary coordinates for travel, and persists stable `hyg:<primary-id>` system identities. It evaluates configured reach candidates and selects by named systems retained, then total retained, then smaller reach/lower seed. The current result selects **9.0 ly**: **99 destinations, 127 cataloged members, all 30 named systems and 34 named members**, degrees 1–6. This is a valid heuristic result, not an optimality claim. The primary-coordinate convention is an engineering approximation, not a derived barycenter. See [grouped results](analysis/phase-0-grouped-results.md).

## Superseded exploratory settings

On the superseded 136-entry candidate pool, a 3D reach of **9.4 ly** with reachability-based pruning produced a connected 108-system subset of the preserved 136 entries, all degrees 1–6. This was the largest candidate in the documented heuristic sweep, not a proven optimum. Only Sol was protected in that experiment. It does not establish the best reach for the current 167-entry pool or the new named-star preference. Re-evaluate before fixing production policy. See [reachability analysis](analysis/phase-0-reachability.md).

The updated 167-entry pool with catalog-name preference produced a 9.0 ly candidate retaining 107 entries and 33 of 34 names. Proxima Centauri is the named removal. That single-star-node experiment is superseded by the grouped run above. See [current candidate analysis](analysis/phase-0-current-candidates.md).

## Engineering defaults for this reorganization

Python 3.9+ with no new runtime dependencies; JSON configuration; separate new run directories; existing algorithms unchanged; uppercase `AGENTS.md` for agent discovery. Phase numbers 0–2 retain their meaning. Former phase 3–5 plans are superseded by the current phase index and milestone roadmap.

## Decide when needed

| Before | Question | Why it matters |
|---|---|---|
| Phase 1 generation | How should noninteractive parent bodies needed for represented moons be stored/count toward the budget? | Planets and represented moons share the budget; rare artificial stations belong to later civilization generation |
| Phase 3 | Epoch date and initial Earth powers: fictional analogues or named historical states? | Scenario identities, cultures, starting assets |
| Phase 3 | Starting off-Earth settlements and infrastructure? | Avoid accidentally assuming an empty or fully industrialized Sol system |
| Phase 0 routes | Adopt 3D travel distances with a separate flat display, and choose distance-only versus selected routes? | Reachability analysis uses 3D distances; route policy remains open |
| Future Phase 0 revision | New catalog evidence or changes to membership/reach policy? | Accepted v1 uses 9.0 ly; reopen deliberately rather than changing the downstream input |
| Phase 4 travel | Initial travel speeds? | Arrival schedules and expansion pace; technology changes speed, not reach |
| Phase 4 travel | Annual decisions with finer arrival times, or another time model? | Event ordering and runtime |
| Phase 4 travel | Can vessels upgrade during a journey? Default proposal: no | Reproducible arrival scheduling |
| Phase 4 research | Research costs, diffusion, and whether advances can be lost? | Divergence and technological monopolies |
| Phase 4 politics | How to model Earth-based territories without a full Earth strategy game? | Shared origin, resources, and conflict |
| Phase 4 culture | Initial language/name datasets and permitted naming conventions? | Authenticity and data provenance |
| Phase 4 communications | Speed, range, infrastructure, ownership, and interception after unlock? | Political reach and information inequality |
| Phase 5 | Stop after a duration, at a target date, or under world-readiness conditions? | Reproducible playable starting point |
| Phase 6 | Game calendar versus simulation dates; export schemas and memory budgets? | X16 runtime compatibility |

Do not block the current organization/validation milestones on these questions. Discuss them before implementing dependent mechanics.

## Phase 0 acceptance

User requested closeout after reviewing the grouped result. Accepted v1 is the preserved 99-destination dataset at 9.0 ly. Its documented source limitations remain recorded; no claim of complete astronomical catalog accuracy is made. Source/override/implementation hashes and the six output hashes define the handoff. See [closeout](PHASE_0_CLOSEOUT.md). Phase 1 review and validation is next.

## Phase 0 cube revision — September 2026

At the user's request, replace the current spherical neighborhood with a 50 ly cube centered on Sol, aligned with HYG x/y/z axes. Select designated primary coordinates inclusively within ±25 ly on every axis. Group members first, preserving companions beyond these bounds. Radial distance remains descriptive; it is not the cube cutoff.

Keep 9 ly physical 3D reach, technology affecting travel time only, named-system preference, the 300-candidate budget, and connected 1–6-neighbor system pruning. The map is a 100×100 square projection at 0.5 ly/cell with no circular background mask and no map-collision pruning. Preserve spherical v1; generate cube v2 separately. See [results](analysis/phase-0-cube-results.md). Phase 1 data must be regenerated deliberately for the new catalog.

## Local Spob overlap resolution — September 2026

Approved by the user: preserve natural objects and their properties; resolve display collisions after preferred local placement. Process parents before moons, then stable object ID. Use nearest free cells within 50×50, with equal-distance ties resolved by row then column. This introduces no minimum sprite spacing beyond cell uniqueness. The corrected cube dataset is `phase1-cube-v3`; earlier outputs remain preserved.

## Runtime identities and world versions — September 2026

Keep source-based system IDs offline. Export contiguous byte indexes for X16: Sol 0, other systems sorted by source ID, 255 reserved for no reference. Assign local Spob byte indexes per system and translate every exported reference through explicit mappings. Enforce 255-system and 255-Spob-per-system capacity. World compatibility uses a format-version byte and full 32-byte content-derived world ID; future saves must match both before using indexes. Early physical identity export is implemented, while full Phase 6 and the save loader remain planned. See the Phase 6 contract.

## Phase 1 acceptance — September 2026

The user authorized promotion, validation and closeout before discussing Phase 2. Adopt total-body weights 10/35/35/15/4/1 percent for 0–5 Spobs, counting represented moons and parents together. Retain Sol's Earth/Luna/Mars/Ceres exception and primary-spectral attribute approximation; defer member-specific stellar orbits. Promote the curated algorithm to the standard pipeline, preserving an explicitly named legacy generator for comparisons. Accepted production artifact: `physical-phase1-v1`, with the same 274 Spobs as corrected trial v3.

## Major artifact direction and trial — September 2026

User direction: artifacts should strongly shape history; a Sol find enabled initial interstellar capability. Trial target: 7–8 technologies with 3–5 times as many archaeological finds. Trial v1 uses 8 technology sites including a provisional Mars origin, plus 32 archaeology-only sites. Exact technology list, origin location, redundancy and effect mechanics remain provisional. A separate scenario handoff records pre-epoch exploitation without inventing discoverers, dates or initial beneficiaries. See the Phase 2 trial report.

## Artifacts accelerate independently researchable technology — September 2026

Every artifact-associated technology can also be developed through independent research. Sites can accelerate progress toward that technology; they are not exclusive sources or mandatory prerequisites. Discovery alone does not automatically grant mastery, deployment or shared faction knowledge. The magnitude and mechanism of acceleration remain to be designed.

User clarification supersedes the unique-prize interpretation of trial v1. A unique site is not a unique path to a technology. Sol’s origin discovery accelerated the historical arrival of interstellar capability. No quantitative boost, prerequisite model or research simulation is accepted or implemented by this clarification.

## Approved technology-site spacing — September 2026

Following the successful test, the user approved committing the three-jump placement rule: eight technology-associated sites including the fixed Mars origin, separated by at least three shortest-path jumps on the travel graph. Retain 32 loosely scattered archaeological sites. This approves the placement direction; Phase 2 production integration, reusable artifact validation and closeout remain before Phase 3.
