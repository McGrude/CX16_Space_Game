# Universe generation phases

These are the current phase boundaries. Phases 0–2 retain existing implementations; later stages are planned. See [roadmap](../ROADMAP.md) for incremental implementation gates.

| Phase | Purpose | Implementation | Contract |
|---|---|---|---|
| 0 | Grouped stellar systems, routes and map | Closed: accepted v1 | [Stars](00-star-catalog.md) |
| 1 | Natural bodies and resources | Existing; validation pending | [Objects](01-system-objects.md) |
| 2 | Hidden ancient artifacts | Existing; validation pending | [Artifacts](02-alien-artifacts.md) |
| 3 | Initial Earth scenario | Planned, M2 | [Scenario](03-initial-scenario.md) |
| 4 | Historical simulation | Planned, M3–M6 | [History](04-history-simulation.md) |
| 5 | Inspect and prepare the playable world | Planned, M7 | [Snapshot](05-world-snapshot.md) |
| 6 | Export for Commander X16 | Planned, M8 | [Export](06-game-export.md) |

The flow is physical inputs → initial scenario → evolving history → selected snapshot → game data. Phases are not isolated substitutes for interacting simulation systems: economy, research, politics, and culture all participate in phase 4.

## Shared contracts

- Record schema versions, input hashes, implementation hashes, configuration, seeds, and Python version.
- Never overwrite an existing run or the preserved baseline.
- System IDs remain stable. Natural object identity is `(system_id, object_id)`, not `object_id` alone.
- New entities require stable identities independent of mutable names or ownership.
- Hidden physical truth must not leak into actor decision-making.
- Any schemas below for planned stages are proposals to finalize at their milestone; no outputs currently exist.
- Archived specifications are background. Current phase contracts identify intended invariants; M1 will establish where code meets or violates them.
