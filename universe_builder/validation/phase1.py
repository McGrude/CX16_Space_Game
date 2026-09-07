"""Independent checks for standard pipeline Phase 1 artifacts."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
from universe_builder.validation.phase0 import require, validate as validate_phase0


def validate(root):
    root = Path(root)
    validate_phase0(root)
    manifest = json.loads((root/'manifest.json').read_text())
    require(1 in manifest['completed_phases'], 'Phase 1 incomplete')
    path = root/'phase_1/system_objects.csv'
    require(hashlib.sha256(path.read_bytes()).hexdigest() == manifest['outputs']['phase_1/system_objects.csv'],
            'Phase 1 checksum mismatch')
    with (root/'phase_0/star_catalog.csv').open() as f:
        systems = {int(s['id']) for s in csv.DictReader(f)}
    with path.open() as f:
        rows = list(csv.DictReader(f))
    groups = defaultdict(dict)
    classes = {'RP','DP','IC','GG','RM','IM','AS'}
    for row in rows:
        sid, oid = int(row['system_id']), int(row['object_id'])
        require(sid in systems and oid >= 0 and oid not in groups[sid], 'Invalid object identity')
        require(row['class'] in classes, 'Invalid object class')
        require(row['is_moon'] in ('0','1'), 'Invalid moon flag')
        require((row['class'] in ('RM','IM')) == (row['is_moon']=='1'), 'Moon class mismatch')
        for key, maximum in [('local_x',49),('local_y',49),('ore_richness',3),
                             ('fuel_richness',3),('habitability',100),('risk',100)]:
            require(0 <= int(row[key]) <= maximum, 'Attribute out of range: '+key)
        require(bool(row['name']), 'Missing object name')
        groups[sid][oid] = row
    for sid in systems:
        objects = groups[sid]
        require(set(objects)==set(range(len(objects))), 'Noncontiguous local object IDs')
        require(len(objects) <= (4 if sid==0 else manifest['config']['phase_1']['max_objects_per_system']),
                'Object budget exceeded')
        require(len({(r['local_x'],r['local_y']) for r in objects.values()})==len(objects), 'Overlapping cells')
        require(sum(r['class']=='AS' for r in objects.values())<=1, 'Multiple asteroids')
        for row in objects.values():
            if row['is_moon']=='1':
                require(row['parent_object_id'] != '', 'Missing moon parent')
                parent = objects.get(int(row['parent_object_id']))
                require(parent is not None and parent['class'] in ('RP','DP','IC','GG')
                        and parent['is_moon']=='0', 'Invalid moon parent')
            else:
                require(row['parent_object_id']=='', 'Primary has parent')
        for oid, row in objects.items():
            moons = sum(r['parent_object_id']==str(oid) for r in objects.values())
            require(moons <= (3 if row['class']=='GG' else 1 if row['class'] in ('RP','DP','IC') else 0),
                    'Too many moons')
    sol = groups[0]
    require([(r['name'],r['class'],r['parent_object_id']) for _,r in sorted(sol.items())] ==
            [('Earth','RP',''),('Luna','RM','0'),('Mars','RP',''),('Ceres','AS','')], 'Invalid Sol')
    return dict(status='passed', systems=len(systems), objects=len(rows),
                distribution=dict(sorted(Counter(len(groups[sid]) for sid in systems).items())),
                classes=dict(sorted(Counter(r['class'] for r in rows).items())))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory',type=Path)
    print(json.dumps(validate(parser.parse_args().run_directory),indent=2))
