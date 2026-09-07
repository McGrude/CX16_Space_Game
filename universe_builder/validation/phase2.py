"""Independent checks of production artifacts, graph spacing and review map."""
from collections import Counter
import argparse
import csv
import hashlib
import json
from pathlib import Path
from universe_builder.validation.phase0 import require
from universe_builder.validation.phase1 import validate as validate_phase1


def read(path):
    with path.open() as stream:return list(csv.DictReader(stream))


def validate(root):
    root=Path(root)
    validate_phase1(root)
    manifest=json.loads((root/'manifest.json').read_text())
    require(2 in manifest['completed_phases'], 'Phase 2 incomplete')
    config=manifest['config']['phase_2']
    require(config['model']=='spaced_sites_v1','Wrong artifact model')
    phase=root/'phase_2'
    for name in ('system_objects.csv','star_map.txt','summary.json','technologies.json','initial_scenario_handoff.json'):
        require(hashlib.sha256((phase/name).read_bytes()).hexdigest()==manifest['outputs']['phase_2/'+name],
                'Phase 2 checksum mismatch: '+name)
    original=read(root/'phase_1/system_objects.csv')
    rows=read(phase/'system_objects.csv')
    require(len(original)==len(rows),'Spob count changed')
    additions={'artifact_flag','artifact_type','artifact_category','technology_id','artifact_site_id'}
    tech=[];categories={};sites=set()
    for before,after in zip(original,rows):
        require(set(after)==set(before)|additions,'Unexpected physical knowledge/schema fields')
        require(all(after[k]==v for k,v in before.items()),'Phase 1 fields changed')
        category=after['artifact_category'];sid=int(after['system_id'])
        require(category in ('','technology','archaeology'),'Invalid site category')
        if not category:
            require(after['artifact_flag']=='0' and all(after[k]=='' for k in additions-{'artifact_flag','artifact_category'}),
                    'Invalid empty site')
            continue
        require(after['artifact_flag']=='1' and after['class'] in {'RP','DP','IC','RM','IM','AS'},'Ineligible site')
        require(after['artifact_site_id']==f"site:{sid}:{after['object_id']}" and after['artifact_site_id'] not in sites,
                'Invalid site identity')
        sites.add(after['artifact_site_id']);categories.setdefault(sid,set()).add(category)
        if category=='technology':
            require(after['artifact_type']=='TEC','Invalid technology form');tech.append(after)
        else:
            require(after['artifact_type'] in {'ARC','RUI','FAC','BEA'} and after['technology_id']=='','Invalid archaeology')
    require(Counter(r['technology_id'] for r in tech)==Counter(t['id'] for t in config['technologies']), 'Technology quota/identity mismatch')
    require(sum(r['artifact_category']=='archaeology' for r in rows)==config['archaeological_sites'],'Archaeology quota mismatch')
    require(any(r['artifact_site_id']=='site:0:2' and r['name']=='Mars' and r['technology_id']=='interstellar_propulsion' for r in tech),'Mars origin missing')
    require(sum(r['system_id']=='0' for r in tech)==1,'Unexpected extra Sol technology')
    systems=read(root/'phase_0/star_catalog.csv');adj={int(s['id']):set() for s in systems}
    for edge in read(root/'phase_0/routes.csv'):
        a,b=int(edge['from_system_id']),int(edge['to_system_id']);adj[a].add(b);adj[b].add(a)
    technology_systems=[int(r['system_id']) for r in tech]
    require(len(set(technology_systems))==len(tech),'Technology sites share a system')
    pair_distances=[]
    for i,source in enumerate(technology_systems):
        found={source:0};frontier={source};depth=0
        while frontier:
            depth+=1
            frontier={n for node in frontier for n in adj[node] if n not in found}
            found.update({n:depth for n in frontier})
        pair_distances.extend(found[b] for b in technology_systems[i+1:])
    require(min(pair_distances)>=config['technology_min_hops'],'Technology spacing violation')
    lines=[list(line) for line in (root/'phase_0/star_map.txt').read_text().splitlines()]
    for system in systems:
        sid=int(system['id']);cat=categories.get(sid,set())
        symbol='X' if sid==0 else 'T' if 'technology' in cat else 'A' if 'archaeology' in cat else '*'
        lines[int(system['grid_y'])][int(system['grid_x'])]=symbol
    require((phase/'star_map.txt').read_text()=='\n'.join(''.join(line) for line in lines)+'\n','Review map mismatch')
    require(json.loads((phase/'technologies.json').read_text())==config['technologies'],'Technology definitions changed')
    handoff=json.loads((phase/'initial_scenario_handoff.json').read_text())
    require(handoff['origin_site_id']=='site:0:2' and handoff['initial_technology']=='interstellar_propulsion','Invalid scenario origin')
    require(all(handoff[k] is None for k in ('discoverer','discovery_date','initial_beneficiaries')),'Invented scenario history')
    require(handoff['other_sites']=='hidden until explicit discovery and knowledge propagation','Hidden knowledge policy missing')
    summary=json.loads((phase/'summary.json').read_text())
    expected=dict(systems=len(systems),spobs=len(rows),categories=dict(Counter(r['artifact_category'] for r in rows if r['artifact_category'])),
                  systems_with_sites=len(categories),minimum_technology_hops=min(pair_distances),
                  map_symbols=dict(Counter(c for line in lines for c in line if c in 'XTA*')))
    for k,v in expected.items():require(summary[k]==v,'Summary mismatch: '+k)
    return dict(status='passed',**expected)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory',type=Path)
    print(json.dumps(validate(parser.parse_args().run_directory),indent=2))
