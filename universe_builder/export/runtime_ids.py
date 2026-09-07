"""Versioned byte-sized runtime identities for a physical world snapshot."""
import csv
import hashlib
import json
from pathlib import Path

from universe_builder.validation.phase0 import validate

FORMAT_VERSION = 1
NONE = 255


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(path):
    with Path(path).open(newline='') as stream:
        return list(csv.DictReader(stream))


def translate(systems, objects, routes):
    ids = [int(s['id']) for s in systems]
    if len(set(ids)) != len(ids) or ids.count(0) != 1 or not 1 <= len(ids) <= 255:
        raise ValueError('Require unique systems including Sol, with at most 255 destinations')
    mapping = {sid: index for index, sid in enumerate(sorted(ids, key=lambda sid: (sid != 0, sid)))}
    local = {}
    for obj in objects:
        sid, oid = int(obj['system_id']), int(obj['object_id'])
        if sid not in mapping or (sid, oid) in local:
            raise ValueError('Unknown system or duplicate object identity')
        local[sid, oid] = None
    for sid in mapping:
        oids = sorted(oid for system, oid in local if system == sid)
        if len(oids) > 255:
            raise ValueError('At most 255 Spobs per system; index 255 is reserved')
        for index, oid in enumerate(oids):
            local[sid, oid] = index
    converted = []
    for obj in objects:
        sid, oid = int(obj['system_id']), int(obj['object_id'])
        parent = obj['parent_object_id']
        if parent and (sid, int(parent)) not in local:
            raise ValueError('Unknown parent object')
        converted.append({**obj, 'system_id': mapping[sid], 'object_id': local[sid, oid],
                          'parent_object_id': local[sid, int(parent)] if parent else NONE})
    converted.sort(key=lambda o: (o['system_id'], o['object_id']))
    adjacency = [set() for _ in ids]
    for route in routes:
        a, b = int(route['from_system_id']), int(route['to_system_id'])
        if a not in mapping or b not in mapping or a == b:
            raise ValueError('Invalid route reference')
        a, b = mapping[a], mapping[b]
        if b in adjacency[a]:
            raise ValueError('Duplicate route')
        adjacency[a].add(b); adjacency[b].add(a)
    if any(not 1 <= len(neighbors) <= 6 for neighbors in adjacency):
        raise ValueError('Runtime routes require 1–6 neighbors')
    return mapping, local, converted, adjacency


def export(phase0, phase1, output):
    phase0, phase1, output = map(Path, (phase0, phase1, output))
    if output.exists():
        raise ValueError('Choose a new export output directory')
    validate(phase0)
    p0 = phase0 / 'phase_0'
    manifest1 = json.loads((phase1 / 'manifest.json').read_text())
    if manifest1['input_catalog_sha256'] != digest(p0 / 'star_catalog.csv'):
        raise ValueError('Phase 1 was generated from a different catalog')
    for name, expected in manifest1['outputs'].items():
        if digest(phase1 / name) != expected:
            raise ValueError('Phase 1 checksum mismatch')
    systems = read_csv(p0 / 'star_catalog.csv')
    objects = read_csv(phase1 / 'system_objects.csv')
    routes = read_csv(p0 / 'routes.csv')
    mapping, local, converted, adjacency = translate(systems, objects, routes)
    inputs = {f'phase0/{p.name}': digest(p) for p in sorted(p0.iterdir()) if p.is_file()}
    inputs.update({f'phase1/{name}': digest(phase1/name)
                   for name in ('system_objects.csv', 'manifest.json', 'summary.json')})
    identity = {'format_version': FORMAT_VERSION, 'inputs': inputs,
                'system_mapping': sorted(mapping.items()), 'exporter_sha256': digest(__file__)}
    world_id = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    output.mkdir(parents=True)
    def write_csv(name, fields, rows):
        with (output/name).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)
    write_csv('system_id_map.csv', ['source_system_id', 'runtime_system_id'],
              [{'source_system_id': sid, 'runtime_system_id': index} for sid,index in mapping.items()])
    write_csv('spob_id_map.csv', ['source_system_id', 'source_object_id', 'runtime_system_id', 'runtime_object_id'],
              [dict(source_system_id=sid, source_object_id=oid, runtime_system_id=mapping[sid], runtime_object_id=index)
               for (sid,oid),index in sorted(local.items())])
    write_csv('systems.csv', list(systems[0]),
              [{**s, 'id': mapping[int(s['id'])]} for s in sorted(systems, key=lambda s:mapping[int(s['id'])])])
    write_csv('spobs.csv', list(converted[0]) if converted else list(objects[0]) if objects else
              ['system_id','object_id','parent_object_id'], converted)
    write_csv('routes.csv', list(routes[0]),
              [{**r, 'from_system_id':mapping[int(r['from_system_id'])],
                'to_system_id':mapping[int(r['to_system_id'])]} for r in routes])
    (output/'neighbors.bin').write_bytes(bytes(value for neighbors in adjacency
        for value in [len(neighbors), *sorted(neighbors), *([NONE]*(6-len(neighbors)))]))
    (output/'spob_refs.bin').write_bytes(bytes(value for obj in converted
        for value in (obj['system_id'], obj['object_id'], obj['parent_object_id'])))
    # Shared world/save compatibility token: magic, format version, 32-byte world hash.
    (output/'world_header.bin').write_bytes(b'CX16'+bytes([FORMAT_VERSION])+bytes.fromhex(world_id))
    manifest = {'format_version':FORMAT_VERSION, 'world_id':world_id,
                'scope':'physical identity export; not a complete Phase 6 playable snapshot',
                'system_count':len(systems), 'spob_count':len(objects), 'no_reference':NONE,
                'inputs':inputs, 'exporter_sha256':identity['exporter_sha256'],
                'outputs':{p.name:digest(p) for p in sorted(output.iterdir())}}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    return manifest
