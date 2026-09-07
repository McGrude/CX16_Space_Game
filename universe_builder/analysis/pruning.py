"""Heuristic connected degree-bounded subsets; never modifies catalog files."""
import random


def component(adjacency, active, root):
    seen = {root}
    stack = [root]
    while stack:
        i = stack.pop()
        for j in sorted(adjacency[i] & (active - seen)):
            seen.add(j)
            stack.append(j)
    return seen


def prune_to_reachability(distances, radius, cap=6, root=0, seed=0, preferred=()):
    """Keep root's component; greedily remove degree pressure, then reinsert.

    Candidate removals are scored by excess-degree reduction per lost node,
    accounting for components disconnected from the root. Seeded weights explore
    nearby greedy choices. This finds valid subsets, not a proven largest one.
    """
    preferred = set(preferred)
    rng = random.Random(seed)
    n = len(distances)
    adjacency = [{j for j in range(n) if j != i and distances[i][j] <= radius} for i in range(n)]
    active = component(adjacency, set(range(n)), root)
    weights = [rng.uniform(0.85, 1.15) if seed else 1.0 for _ in range(n)]
    while True:
        degree = {i: len(adjacency[i] & active) for i in active}
        over = {i for i in active if degree[i] > cap}
        if not over:
            break
        candidates = (over | set().union(*(adjacency[i] & active for i in over))) - {root}
        excess = sum(max(0, d-cap) for d in degree.values())
        best = None
        for i in sorted(candidates):
            remaining = component(adjacency, active - {i}, root)
            new_excess = sum(max(0, len(adjacency[j] & remaining)-cap) for j in remaining)
            loss = len(active)-len(remaining)
            named_loss = len((active - remaining) & preferred)
            score = (-named_loss, (excess-new_excess)/loss*weights[i], -loss, -i)
            if best is None or score > best[0]:
                best = (score, remaining)
        active = best[1]
    # Restore feasible nodes, considering different deterministic orders.
    changed = True
    while changed:
        changed = False
        missing = sorted(set(range(n))-active)
        if seed:
            rng.shuffle(missing)
        missing.sort(key=lambda i: i not in preferred)
        for i in missing:
            neighbors = adjacency[i] & active
            if 1 <= len(neighbors) <= cap and all(len(adjacency[j] & active) < cap for j in neighbors):
                active.add(i)
                changed = True
    degree = [len(adjacency[i] & active) for i in sorted(active)]
    if len(active) < 2:
        return None
    assert component(adjacency, active, root) == active
    assert min(degree) >= 1 and max(degree) <= cap
    return {'radius_ly': radius, 'seed': seed, 'retained_count': len(active),
            'removed_count': n-len(active), 'preferred_retained': len(active & preferred), 'min_neighbors': min(degree),
            'max_neighbors': max(degree), 'mean_neighbors': sum(degree)/len(active),
            'edges': sum(degree)//2, 'components': 1, 'retained_indices': sorted(active),
            'removed_indices': sorted(set(range(n))-active)}


def sweep(distances, radii, trials=8, preferred=()):
    results = []
    for radius in radii:
        candidates = [prune_to_reachability(distances, radius, seed=seed, preferred=preferred) for seed in range(trials)]
        candidates = [c for c in candidates if c is not None]
        if candidates:
            results.append(max(candidates, key=lambda c: (c['preferred_retained'], c['retained_count'], -c['seed'])))
    return results
