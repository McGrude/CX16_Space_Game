"""Exact-quota major-artifact trial; technology effects are design placeholders."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import platform
from universe_builder.validation.phase1 import validate

ELIGIBLE = {'RP','DP','IC','RM','IM','AS'}
ARCH_TYPES = ('ARC','RUI','FAC','BEA')


def key(row):
    return int(row['system_id']), int(row['object_id'])


def rank(seed, purpose, identity):
    return hashlib.sha256(f'{seed}:{purpose}:{identity[0]}:{identity[1]}'.encode()).digest(), identity


def hop_distances(routes):
    adjacency = {}
    for route in routes:
        a,b = int(route['from_system_id']),int(route['to_system_id'])
        adjacency.setdefault(a,set()).add(b)
        adjacency.setdefault(b,set()).add(a)
    distances = {}
    for source in sorted(adjacency):
        found = {source:0}
        queue = [source]
        for node in queue:
            for neighbor in sorted(adjacency[node]):
                if neighbor not in found:
                    found[neighbor] = found[node]+1
                    queue.append(neighbor)
        if len(found)!=len(adjacency):
            raise ValueError('Travel graph must be connected')
        distances[source] = found
    return distances


def select_spaced(candidates, origin, count, distances, minimum):
    if type(minimum) is not int or minimum < 1:
        raise ValueError('Minimum separation must be a positive integer')
    if any(i[0] not in distances for i in [origin,*candidates]):
        raise ValueError('Candidate missing from travel graph')
    selected = [origin]
    for candidate in candidates:
        if len(selected)==count:
            break
        if all(distances[candidate[0]][other[0]] >= minimum for other in selected):
            selected.append(candidate)
    if len(selected)!=count:
        raise ValueError('Seeded greedy placement could not meet the quota at the requested spacing; no relaxation applied')
    return selected


def place(rows, config, distances=None):
    indexed = {key(r):r for r in rows}
    if len(indexed)!=len(rows):
        raise ValueError('Duplicate input object identity')
    tech = config['technologies']
    if not tech or len({t['id'] for t in tech})!=len(tech) or tech[0]['id']!='interstellar_propulsion':
        raise ValueError('Require unique technologies with interstellar propulsion first')
    count=config['archaeological_sites']
    if type(count) is not int or count<0:
        raise ValueError('Invalid archaeology quota')
    origin = config['origin_site']['system_id'],config['origin_site']['object_id']
    if origin[0]!=0 or origin not in indexed or indexed[origin]['class'] not in ELIGIBLE:
        raise ValueError('Origin must be an eligible Sol object')
    eligible={identity for identity,r in indexed.items() if r['class'] in ELIGIBLE}
    distant=sorted((i for i in eligible if i[0]!=0),key=lambda i:rank(config['seed'],'technology',i))
    if len(distant)<len(tech)-1 or len(eligible)<len(tech)+count:
        raise ValueError('Insufficient eligible objects for exact quotas')
    selected = [origin,*distant[:len(tech)-1]]
    if 'technology_min_hops' in config:
        if distances is None:raise ValueError('Travel graph required for spaced placement')
        selected = select_spaced(distant,origin,len(tech),distances,config['technology_min_hops'])
    technology_sites=dict(zip(selected, [t['id'] for t in tech]))
    archaeology=sorted(eligible-technology_sites.keys(),key=lambda i:rank(config['seed'],'archaeology',i))[:count]
    archaeology=set(archaeology)
    result=[]
    for row in rows:
        identity=key(row)
        category='technology' if identity in technology_sites else 'archaeology' if identity in archaeology else ''
        typ='TEC' if category=='technology' else ARCH_TYPES[rank(config['seed'],'form',identity)[0][0]%len(ARCH_TYPES)] if category else ''
        result.append({**row,'artifact_flag':str(int(bool(category))), 'artifact_type':typ,
                       'artifact_category':category,'technology_id':technology_sites.get(identity,''),
                       'artifact_site_id':f'site:{identity[0]}:{identity[1]}' if category else ''})
    return result


def run(config_path, output):
    config_path,output=Path(config_path).resolve(),Path(output).resolve()
    if output.exists():raise ValueError('Choose a new output directory')
    config=json.loads(config_path.read_text())
    if config['schema_version']!=1:raise ValueError('Unsupported config schema')
    source=(config_path.parent/config['input_run']).resolve()
    validate(source)
    input_path=source/'phase_1/system_objects.csv'
    with input_path.open() as f:rows=list(csv.DictReader(f))
    with (source/"phase_0/routes.csv").open() as f:distances=hop_distances(list(csv.DictReader(f)))
    result=place(rows,config,distances)
    for before,after in zip(rows,result):
        if any(after[k]!=v for k,v in before.items()):raise ValueError('Phase 1 fields changed')
    with (source/'phase_0/star_catalog.csv').open() as f:names={int(s['id']):s['proper'] for s in csv.DictReader(f)}
    sites=[r for r in result if r['artifact_flag']=='1']
    summary={'status':'trial; Phase 2 not accepted','systems':len(names),'spobs':len(rows),
             'eligible_spobs':sum(r['class'] in ELIGIBLE for r in rows),
             'sites':len(sites),'systems_with_sites':len({r['system_id'] for r in sites}),
             'categories':dict(Counter(r['artifact_category'] for r in sites)),
             'site_classes':dict(Counter(r['class'] for r in sites)),
             'technology_sites':[dict(system_id=int(r['system_id']),system_name=names[int(r['system_id'])],
                                      object_id=int(r['object_id']),object_name=r['name'],technology_id=r['technology_id'])
                                 for r in sites if r['artifact_category']=='technology']}
    tech_systems = [int(r['system_id']) for r in sites if r['artifact_category']=='technology']
    separations = [distances[a][b] for i,a in enumerate(tech_systems) for b in tech_systems[i+1:]]
    nearest = [min(distances[a][b] for b in tech_systems if b!=a) for a in tech_systems]
    summary['technology_spacing'] = dict(minimum_pair_hops=min(separations),
        mean_nearest_technology_hops=sum(nearest)/len(nearest),
        sol_to_other_technology_hops=sorted(distances[0][b] for b in tech_systems if b!=0),
        max_system_hops_to_technology=max(min(distances[a][b] for b in tech_systems) for a in distances))
    if 'technology_min_hops' in config and min(separations)<config['technology_min_hops']:
        raise ValueError('Placement violates requested separation')
    output.mkdir(parents=True)
    with (output/'system_objects.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    scenario={'status':'proposed initial-scenario handoff; not an executed historical event',
              'origin_site_id':f"site:{config['origin_site']['system_id']}:{config['origin_site']['object_id']}",
              'initial_technology':'interstellar_propulsion',
              'timing':'discovered and exploited before simulation epoch',
              'discoverer':None,'discovery_date':None,'initial_beneficiaries':None,
              'other_sites':'hidden until explicit discovery and knowledge propagation',
              'technology_effects':'not implemented; no placement field grants knowledge or bonuses'}
    for name,value in [('summary.json',summary),('initial_scenario_handoff.json',scenario),('technologies.json',config['technologies'])]:
        (output/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest={'schema_version':1,'config':config,'python_version':platform.python_version(),
              'routes_sha256':digest(source/'phase_0/routes.csv'),
              'input_sha256':digest(input_path),'input_manifest_sha256':digest(source/'manifest.json'),
              'config_sha256':digest(config_path),'implementation_sha256':digest(__file__),
              'outputs':{p.name:digest(p) for p in sorted(output.iterdir())}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    run(args.config,args.output)
