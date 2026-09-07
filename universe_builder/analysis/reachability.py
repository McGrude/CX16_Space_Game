"""Analyze fixed-radius 3D travel graphs without modifying generation data."""
import csv
import hashlib
import json
import math
from pathlib import Path

from universe_builder.analysis.pruning import sweep

from universe_builder.phases.phase_0_star_catalog import (
    PC_TO_LY, generate_synthetic_name, load_hyg_csv,
)

ROOT = Path(__file__).resolve().parents[2]


def graph_stats(distances, radius):
    n = len(distances)
    adjacency = [[j for j in range(n) if j != i and distances[i][j] <= radius]
                 for i in range(n)]
    unseen = set(range(n))
    sizes = []
    while unseen:
        stack = [min(unseen)]
        unseen.remove(stack[0])
        size = 0
        while stack:
            i = stack.pop()
            size += 1
            for j in adjacency[i]:
                if j in unseen:
                    unseen.remove(j)
                    stack.append(j)
        sizes.append(size)
    degrees = [len(a) for a in adjacency]
    return {"radius_ly": radius, "min_neighbors": min(degrees),
            "max_neighbors": max(degrees), "mean_neighbors": sum(degrees)/n,
            "isolated_systems": degrees.count(0), "systems_over_six": sum(d > 6 for d in degrees),
            "components": len(sizes), "component_sizes": sorted(sizes, reverse=True),
            "edges": sum(degrees)//2}


def critical_distances(distances):
    n = len(distances)
    if n < 8:
        raise ValueError("At least eight systems required for seventh-neighbor analysis")
    ordered = [sorted((distances[i][j], j) for j in range(n) if j != i) for i in range(n)]
    isolated_limit, isolated_i = max((row[0][0], i) for i, row in enumerate(ordered))
    seventh_limit, seventh_i = min((row[6][0], i) for i, row in enumerate(ordered))
    mst = minimum_spanning_tree(distances)
    bridge = max(mst)
    return {"no_isolates_radius_ly": isolated_limit,
            "no_isolates_limiting_system_index": isolated_i,
            "six_neighbor_radius_exclusive_upper_bound_ly": seventh_limit,
            "first_seven_neighbor_system_index": seventh_i,
            "connected_radius_ly": bridge[0], "last_connecting_edge_indices": list(bridge[1:]),
            "degree_1_to_6_possible": isolated_limit < seventh_limit,
            "connected_degree_1_to_6_possible": bridge[0] < seventh_limit}


def minimum_spanning_tree(distances):
    """Deterministic Prim tree on a complete distance matrix."""
    n = len(distances)
    seen = {0}
    best = [(distances[0][j], 0) for j in range(n)]
    mst = []
    while len(seen) < n:
        distance, parent, j = min((best[j][0], best[j][1], j) for j in range(n) if j not in seen)
        mst.append((distance, parent, j))
        seen.add(j)
        for k in range(n):
            if k not in seen and (distances[j][k], j) < best[k]:
                best[k] = (distances[j][k], j)
    return mst


def sparse_route_example(distances, radius=10.3, cap=6, target=3):
    """Illustrative route-selection policy, not a change to travel rules.

    Start with an MST; add shortest edges helping an endpoint below target,
    provided neither endpoint exceeds cap. Reject an infeasible initial tree.
    This is not a general degree-constrained spanning-tree solver.
    """
    n = len(distances)
    tree = minimum_spanning_tree(distances)
    edges = {(min(i,j), max(i,j)) for _,i,j in tree}
    degree = [0]*n
    for i,j in edges:
        degree[i] += 1
        degree[j] += 1
    tree_max_degree = max(degree)
    if tree_max_degree > cap or max(d for d,_,_ in tree) > radius:
        raise ValueError("This MST does not satisfy the proposed route bounds")
    for distance,i,j in sorted((distances[i][j],i,j) for i in range(n) for j in range(i+1,n)):
        if distance > radius:
            break
        if ((i,j) not in edges and degree[i] < cap and degree[j] < cap
            and (degree[i] < target or degree[j] < target)):
            edges.add((i,j))
            degree[i] += 1
            degree[j] += 1
    return {"status": "illustrative alternative; not an adopted rule",
            "radius_ly": radius, "target_neighbors": target, "cap_neighbors": cap,
            "mst_max_neighbors": tree_max_degree, "edges": len(edges),
            "min_neighbors": min(degree), "max_neighbors": max(degree),
            "mean_neighbors": sum(degree)/n,
            "components": 1, "max_route_length_ly": max(distances[i][j] for i,j in edges),
            "degree_histogram": {str(d): degree.count(d) for d in sorted(set(degree))}}


def main():
    baseline = ROOT / 'universe_builder/data/baseline/phase_0/star_catalog.csv'
    source = ROOT / 'universe_builder/data/source/hygdata_v42.csv'
    config_path = ROOT / 'universe_builder/configs/baseline.json'
    scale = json.loads(config_path.read_text())['phase_0']['scale']
    with baseline.open(newline='') as f:
        rows = list(csv.DictReader(f))
    # Reidentify existing entries using all exported physical/name fields.
    # No phase output is regenerated, and no new stars are selected.
    candidates = {}
    for s in load_hyg_csv(str(source)):
        if not math.isfinite(s['dist_ly']):
            continue
        key = round(s['dist_ly'], 9)
        candidates.setdefault(key, []).append(s)
    matched = []
    for row in rows:
        matches = []
        for s in candidates.get(round(float(row['dist_ly']), 9), []):
            name = s['proper'].strip() or generate_synthetic_name(s)
            if (name == row['proper'] and s['spect'] == row['spect']
                and round(50+s['x_ly']/scale) == int(row['grid_x'])
                and round(50+s['y_ly']/scale) == int(row['grid_y'])):
                matches.append(s)
        if len(matches) != 1:
            raise ValueError(f"Expected unique HYG match for {row['id']} {row['proper']}; got {len(matches)}")
        matched.append(matches[0])
    coordinates = [[s[k] for k in ('x_ly', 'y_ly', 'z_ly')] for s in matched]
    distances = [[math.dist(a,b) for b in coordinates] for a in coordinates]
    critical = critical_distances(distances)
    isolated_i = critical.pop('no_isolates_limiting_system_index')
    crowded_i = critical.pop('first_seven_neighbor_system_index')
    edge = critical.pop('last_connecting_edge_indices')
    identity = lambda i: {'id': int(rows[i]['id']), 'name': rows[i]['proper'], 'hyg_id': matched[i]['id']}
    critical['no_isolates_limiting_system'] = identity(isolated_i)
    critical['first_seven_neighbor_system'] = identity(crowded_i)
    critical['last_connecting_edge'] = [identity(i) for i in edge]
    thresholds = sorted(set([4., 5., 6., 7., 8., 9., 10., 12.,
        10.3, critical['no_isolates_radius_ly'], critical['connected_radius_ly'],
        math.nextafter(critical['six_neighbor_radius_exclusive_upper_bound_ly'], -math.inf)]))
    result = {
        'method': 'Undirected edge iff true 3D separation <= radius; no map-coordinate distances. All 136 baseline entries uniquely matched to HYG source.',
        'system_count': len(rows), 'parsec_to_ly': PC_TO_LY,
        'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (baseline, source, config_path)},
        'critical_distances': critical,
        'sparse_route_example': sparse_route_example(distances),
        'pruning_sweep': sweep(distances, [6., 6.5, 7., 7.5, 8., 8.5, *[i/10 for i in range(90, 101)], 10.3]),
        'thresholds': [graph_stats(distances, r) for r in thresholds],
        'source_identity_mapping': [identity(i) for i in range(len(rows))],
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
