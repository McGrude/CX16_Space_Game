"""Exact-quota major-artifact trial; technology effects are design placeholders."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import platform
from universe_builder.validation.phase1 import validate

from universe_builder.phases.phase_2_artifact_sites import ELIGIBLE, ARCH_TYPES, key, rank, hop_distances, select_spaced, place


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
