"""Production quota-based artifact placement and omniscient review map."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

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



def build(root):
    root=Path(root)
    config=json.loads((root/'manifest.json').read_text())['config']['phase_2']
    validate_settings(config)
    with (root/'phase_1/system_objects.csv').open() as f:rows=list(csv.DictReader(f))
    with (root/'phase_0/routes.csv').open() as f:distances=hop_distances(list(csv.DictReader(f)))
    with (root/'phase_0/star_catalog.csv').open() as f:systems=list(csv.DictReader(f))
    result=place(rows,config,distances)
    output=root/'phase_2'
    if any(output.iterdir()):raise ValueError('Phase output must be empty')
    with (output/'system_objects.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(result[0]));writer.writeheader();writer.writerows(result)
    categories={int(s['id']):set() for s in systems}
    for row in result:
        if row['artifact_category']:categories[int(row['system_id'])].add(row['artifact_category'])
    lines=[list(line) for line in (root/'phase_0/star_map.txt').read_text().splitlines()]
    for system in systems:
        sid=int(system['id'])
        symbol='X' if sid==0 else 'T' if 'technology' in categories[sid] else 'A' if 'archaeology' in categories[sid] else '*'
        lines[int(system['grid_y'])][int(system['grid_x'])]=symbol
    (output/'star_map.txt').write_text('\n'.join(''.join(line) for line in lines)+'\n')
    tech=[r for r in result if r['artifact_category']=='technology']
    names={int(s['id']):s['proper'] for s in systems}
    summary=dict(systems=len(systems),spobs=len(result),
        categories=dict(Counter(r['artifact_category'] for r in result if r['artifact_category'])),
        systems_with_sites=sum(bool(c) for c in categories.values()),
        technology_sites=[dict(system_id=int(r['system_id']),system_name=names[int(r['system_id'])],
            object_id=int(r['object_id']),object_name=r['name'],technology_id=r['technology_id']) for r in tech],
        minimum_technology_hops=min(distances[int(a['system_id'])][int(b['system_id'])]
            for i,a in enumerate(tech) for b in tech[i+1:]),
        map_symbols=dict(Counter(c for line in lines for c in line if c in 'XTA*')),
        map_visibility='omniscient developer review; not actor knowledge')
    handoff=dict(schema_version=1,origin_site_id='site:0:2',initial_technology='interstellar_propulsion',
        timing='discovered and exploited before simulation epoch',discoverer=None,discovery_date=None,
        initial_beneficiaries=None,other_sites='hidden until explicit discovery and knowledge propagation',
        technology_policy='All technologies independently researchable; sites can accelerate research.',
        technology_effects='not implemented; placement grants no knowledge or bonuses')
    for name,value in [('summary.json',summary),('initial_scenario_handoff.json',handoff),('technologies.json',config['technologies'])]:
        (output/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))


def validate_settings(config):
    expected={'model','seed','archaeological_sites','origin_site','technologies','technology_min_hops'}
    if set(config)!=expected or config['model']!='spaced_sites_v1':
        raise ValueError('Invalid spaced artifact configuration')
    if type(config['seed']) is not int or not 0<=config['seed']<2**32:
        raise ValueError('Invalid artifact seed')
    if type(config['archaeological_sites']) is not int or config['archaeological_sites']<0:
        raise ValueError('Invalid archaeology quota')
    if type(config['technology_min_hops']) is not int or config['technology_min_hops']<1:
        raise ValueError('Invalid technology spacing')
    if config['origin_site']!={'system_id':0,'object_id':2}:
        raise ValueError('Current scenario requires the Mars origin (0,2)')
    tech=config['technologies']
    if (not isinstance(tech,list) or len(tech)<2 or
        any(not isinstance(t,dict) or set(t)!={'id','name','role'} or
            any(not isinstance(v,str) or not v.strip() for v in t.values()) for t in tech)):
        raise ValueError('Invalid technology definitions')
    if len({t['id'] for t in tech})!=len(tech) or tech[0]['id']!='interstellar_propulsion':
        raise ValueError('Technology identities must be unique with propulsion first')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-directory',type=Path,required=True)
    build(parser.parse_args().run_directory)
