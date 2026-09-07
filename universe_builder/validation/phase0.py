"""Validate a grouped Phase 0 run from its exported files."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(run_path):
    root = Path(run_path).resolve()
    manifest = json.loads((root/'manifest.json').read_text())
    require(manifest['status']=='complete' and 0 in manifest['completed_phases'], 'Phase 0 run is incomplete')
    require(manifest['config']['schema_version']==2, 'Grouped schema 2 required')
    phase = root/'phase_0'
    names = ('star_catalog.csv','star_map.txt','routes.csv','stellar_members.json',
             'candidate_systems.json','selection_summary.json')
    for name in names:
        require(hashlib.sha256((phase/name).read_bytes()).hexdigest()==manifest['outputs']['phase_0/'+name],
                f'Output checksum mismatch: {name}')
    with (phase/'star_catalog.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    systems = {int(r['id']):r for r in rows}
    require(len(systems)==len(rows)>1 and 0 in systems, 'Invalid or duplicate system IDs')
    summary = json.loads((phase/'selection_summary.json').read_text())
    members = json.loads((phase/'stellar_members.json').read_text())
    candidates = json.loads((phase/'candidate_systems.json').read_text())
    require(summary['schema_version']==members['schema_version']==candidates['schema_version']==2,'Invalid output schema')
    reach = summary['reach_ly']
    require(math.isfinite(reach) and reach>0,'Invalid reach')
    require(reach in manifest['config']['phase_0']['reach_candidates_ly'],'Reach absent from configured candidates')
    points = {i:[float(r[k]) for k in ('x_ly','y_ly','z_ly')] for i,r in systems.items()}
    cells = set()
    settings = manifest['config']['phase_0']
    shape = settings.get('shape', 'sphere')
    require(shape in ('sphere','cube'), 'Invalid neighborhood shape')
    radius = settings['half_extent_ly' if shape=='cube' else 'radius_ly']
    def inside(point):
        return (max(abs(c) for c in point) if shape=='cube' else math.dist(point,[0,0,0])) <= radius
    for i,r in systems.items():
        require(all(math.isfinite(c) for c in points[i]),'Nonfinite physical position')
        require(math.isclose(math.dist(points[i],[0,0,0]),float(r['dist_ly']),abs_tol=1e-10),'Invalid radial distance')
        require(inside(points[i]),'System outside neighborhood')
        require(r['system_key']==f'hyg:{i}' and int(r['primary_hyg_id'])==i,'Unstable source-based identity')
        cell = (int(r['grid_x']),int(r['grid_y']))
        require(all(0<=c<100 for c in cell) and cell not in cells,'Invalid or duplicate display cell')
        cells.add(cell)
    require(systems[0]['proper']=='Sol' and math.dist(points[0],[0,0,0])<.01,'Invalid Sol')
    require((int(systems[0]['grid_x']),int(systems[0]['grid_y']))==(50,50),'Sol not centered')
    adjacency = {i:set() for i in systems}
    edges = {}
    with (phase/'routes.csv').open(newline='') as f:
        for route in csv.DictReader(f):
            a,b = int(route['from_system_id']),int(route['to_system_id'])
            edge = frozenset((a,b))
            require(a in systems and b in systems and a!=b and edge not in edges,'Invalid/duplicate route')
            edges[edge] = float(route['distance_ly'])
            adjacency[a].add(b);adjacency[b].add(a)
    for i in systems:
        for j in systems:
            if j<=i:
                continue
            distance = math.dist(points[i],points[j])
            edge = frozenset((i,j))
            require((edge in edges)==(distance<=reach),'Route graph omits or adds a within-reach connection')
            if edge in edges:
                require(math.isclose(edges[edge],distance,rel_tol=0,abs_tol=1e-10),'Incorrect route distance')
    degrees = [len(a) for a in adjacency.values()]
    require(all(1<=d<=6 for d in degrees),'Neighbor count outside 1–6')
    seen,todo = {0},[0]
    while todo:
        for j in adjacency[todo.pop()]:
            if j not in seen:
                seen.add(j);todo.append(j)
    require(len(seen)==len(systems),'Disconnected travel network')
    member_systems = {s['system_id']:s for s in members['systems']}
    require(set(member_systems)==set(systems) and len(member_systems)==len(members['systems']), 'Member-system mismatch')
    member_ids,named_members = set(),0
    for i,s in member_systems.items():
        require(s['system_key']==f'hyg:{i}' and s['primary_hyg_id']==str(i),'Member primary mismatch')
        require(len(s['members'])==int(systems[i]['member_count']),'Incorrect member count')
        primary = [m for m in s['members'] if m['hyg_id']==str(i)]
        require(len(primary)==1 and primary[0]['coordinates_ly']==points[i],'Primary position mismatch')
        for member in s['members']:
            require(member['hyg_id'] not in member_ids,'Member appears in multiple destinations')
            member_ids.add(member['hyg_id'])
            named_members += bool(member['proper'])
        require(bool(int(systems[i]['is_named']))==any(m['proper'] for m in s['members']),'Named preference flag mismatch')
    audit = {s['id']:s for s in candidates['systems']}
    require(len(audit)==len(candidates['systems']),'Duplicate candidate identity')
    require(all(inside(s['point']) for s in audit.values()), 'Candidate outside neighborhood')
    require({i for i,s in audit.items() if s['retained']}==set(systems),'Candidate retention mismatch')
    for i,s in member_systems.items():
        require(set(audit[i]['member_hyg_ids'])=={m['hyg_id'] for m in s['members']},'Candidate membership mismatch')
    named_count = sum(int(r['is_named']) for r in rows)
    expected = {'retained_systems':len(systems),'retained_catalog_members':len(member_ids),
                'retained_named_systems':named_count,'retained_named_members':named_members,
                'candidate_systems':len(audit),'pruned_systems':len(audit)-len(systems),
                'routes':len(edges),'components':1,'min_neighbors':min(degrees),'max_neighbors':max(degrees)}
    for key,value in expected.items():
        require(summary[key]==value,f'Summary mismatch: {key}')
    require(summary['degree_histogram']=={str(d):degrees.count(d) for d in sorted(set(degrees))},'Degree histogram mismatch')
    require(math.isclose(summary['mean_neighbors'],sum(degrees)/len(degrees)),'Mean degree mismatch')
    loss_ids={s['id'] for s in summary['named_system_losses']}
    require(loss_ids=={i for i,s in audit.items() if s['is_named'] and not s['retained']},'Named-loss report mismatch')
    lines=(phase/'star_map.txt').read_text().splitlines()
    require(len(lines)==100 and all(len(line)==100 for line in lines),'Invalid map size')
    require(sum(line.count('X') for line in lines)==1 and sum(line.count('*') for line in lines)==len(systems)-1,'Map symbol count mismatch')
    for i,r in systems.items():
        require(lines[int(r['grid_y'])][int(r['grid_x'])]==('X' if i==0 else '*'),'Map position mismatch')
    return {'status':'passed','reach_ly':reach,**expected}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory',type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps(validate(args.run_directory),indent=2))
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(1,f'Validation failed: {exc}\n')


if __name__=='__main__':
    main()
