"""Experimental total-body budget; does not change the accepted phase generator."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import platform
import random

from universe_builder.phases import phase_1_system_objects as existing


def generate(star, seed, weights):
    return existing.generate_objects_for_system(int(star['id']),star['proper'],star['spect'],seed,5,weights)


def validate(star, objects):
    sid=int(star['id'])
    assert len(objects)<=5
    assert len({(o["local_x"],o["local_y"]) for o in objects})==len(objects), "Overlapping local coordinates"
    assert [o['object_id'] for o in objects]==list(range(len(objects)))
    for o in objects:
        assert o['system_id']==sid
        if o['is_moon']:
            parent=objects[o['parent_object_id']]
            assert not parent['is_moon'] and parent['class'] in existing.MAX_MOONS_PER_CLASS
        else:
            assert o['parent_object_id'] is None
        assert all(0<=o[k]<50 for k in ('local_x','local_y'))
        assert all(0<=o[k]<=100 for k in ('habitability','risk'))
        assert all(0<=o[k]<=3 for k in ('ore_richness','fuel_richness'))


def run(config_path, output):
    config_path=Path(config_path).resolve()
    config=json.loads(config_path.read_text())
    if config['schema_version']!=1 or config['sol_policy']!='existing_earth_luna_mars_ceres':
        raise ValueError('Unsupported trial configuration')
    weights=config['total_body_weights']
    if ([r[0] for r in weights]!=list(range(6))
        or any(type(w) is not int or w<0 for _,w in weights) or sum(w for _,w in weights)!=100):
        raise ValueError('Weights must specify 0–5 with integer percentages totaling 100')
    source=(config_path.parent/config['input_catalog']).resolve()
    with source.open(newline='') as f:stars=list(csv.DictReader(f))
    assert len({int(s['id']) for s in stars})==len(stars) and sum(s['id']=='0' for s in stars)==1
    output=Path(output).resolve()
    if output.exists():raise ValueError('Choose a new trial output directory')
    results=[];counts=Counter();ordinary=Counter();oldcounts=Counter();per_system=[]
    duplicate_cells=[]
    for star in stars:
        objs=generate(star,config['seed'],weights)
        validate(star,objs)
        assert objs==generate(star,config['seed'],weights),'Reproducibility failure'
        results.extend(objs);counts[len(objs)]+=1
        if star['id']!='0':ordinary[len(objs)]+=1
        old=existing.generate_legacy_objects_for_system(int(star['id']),star['proper'],star['spect'],config['seed'],5)
        oldcounts[len(old)]+=1
        if len({(o['local_x'],o['local_y']) for o in objs})!=len(objs):duplicate_cells.append(int(star['id']))
        per_system.append({'system_id':int(star['id']),'name':star['proper'],
                           'objects':len(objs),'moons':sum(o['is_moon'] for o in objs),
                           'existing_generator_objects':len(old)})
    classes=Counter(o['class'] for o in results)
    summary={'status':'experimental; Phase 1 not accepted','seed':config['seed'],
             'systems':len(stars),'objects':len(results),'mean_objects':len(results)/len(stars),
             'distribution_all_systems':{str(i):counts[i] for i in range(6)},
             'distribution_excluding_sol':{str(i):ordinary[i] for i in range(6)},
             'ordinary_systems':len(stars)-1,'class_counts':dict(sorted(classes.items())),
             'planets':sum(classes[c] for c in ('RP','DP','IC','GG')),
             'moons':sum(classes[c] for c in ('RM','IM')),'asteroids':classes['AS'],
             'existing_generator_objects':sum(n*c for n,c in oldcounts.items()),
             'existing_generator_distribution':dict(sorted(oldcounts.items())),
             'empty_systems':[s['name'] for s in per_system if not s['objects']],
             'coordinate_collision_system_ids':duplicate_cells,'per_system':per_system,
             'assumptions':['Total budget includes represented moons and their parent bodies.',
                            'Sol retains Earth, Luna, Mars, Ceres outside the random draw.',
                            'Planet types, attributes and moon probabilities reuse existing logic; moon count clipped to remaining slots.',
                            'Asteroid replacement only targets a moonless primary when at least two primaries exist.',
                            'Primary spectral type used; no per-member stellar orbits, artificial satellites or civilization.']}
    output.mkdir(parents=True)
    fields=['system_id','object_id','name','class','parent_object_id','is_moon',
            'local_x','local_y','ore_richness','fuel_richness','habitability','risk']
    with (output/'system_objects.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(results)
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest={'schema_version':1,'config':config,'python':platform.python_version(),
              'input_catalog_sha256':digest(source),'config_sha256':digest(config_path),
              'implementations':{'analysis/phase1_density.py':digest(__file__),
                                 'phases/phase_1_system_objects.py':digest(existing.__file__)},
              'outputs':{n:digest(output/n) for n in ('system_objects.csv','summary.json')}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('per_system','empty_systems','assumptions')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    run(args.config,args.output)
