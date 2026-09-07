# Decisions and open questions

## Accepted

| Decision | Basis |
|---|---|
| Offline history precedes gameplay | User wants both a parameterized generator and an explorable generated world |
| Start at the dawn of interstellar travel | User direction |
| Earth powers seed the simulation; future factions emerge | User direction |
| Propulsion advances reduce travel time | User direction |
| Messages initially move with ships; later research/artifacts unlock faster communication | User direction |
| Culture, language, and historical naming matter | User direction |
| No living aliens | Existing world-generation rule retained |
| Retain existing MIT license | Repository already has an MIT license |
| Preserve phase 0–2 output and validate before expanding | Repository reorganization scope |

## Engineering defaults for this reorganization

Python 3.9+ with no new runtime dependencies; JSON configuration; separate new run directories; existing algorithms unchanged; uppercase `AGENTS.md` for agent discovery. Phase numbers 0–2 retain their meaning. Former phase 3–5 plans are superseded by the current phase index and milestone roadmap.

## Decide when needed

| Before | Question | Why it matters |
|---|---|---|
| Phase 3 | Epoch date and initial Earth powers: fictional analogues or named historical states? | Scenario identities, cultures, starting assets |
| Phase 3 | Starting off-Earth settlements and infrastructure? | Avoid accidentally assuming an empty or fully industrialized Sol system |
| Phase 4 travel | Initial travel speeds and 2D gameplay versus 3D physical distances? | Arrival schedules and expansion pace |
| Phase 4 travel | Annual decisions with finer arrival times, or another time model? | Event ordering and runtime |
| Phase 4 travel | Can vessels upgrade during a journey? Default proposal: no | Reproducible arrival scheduling |
| Phase 4 research | Research costs, diffusion, and whether advances can be lost? | Divergence and technological monopolies |
| Phase 4 politics | How to model Earth-based territories without a full Earth strategy game? | Shared origin, resources, and conflict |
| Phase 4 culture | Initial language/name datasets and permitted naming conventions? | Authenticity and data provenance |
| Phase 4 communications | Speed, range, infrastructure, ownership, and interception after unlock? | Political reach and information inequality |
| Phase 5 | Stop after a duration, at a target date, or under world-readiness conditions? | Reproducible playable starting point |
| Phase 6 | Game calendar versus simulation dates; export schemas and memory budgets? | X16 runtime compatibility |

Do not block the current organization/validation milestones on these questions. Discuss them before implementing dependent mechanics.
