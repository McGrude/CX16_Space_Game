"""Catalog-backed membership; physical proximity never establishes a group."""
import csv
import json
import math
from collections import defaultdict

from universe_builder.phases.phase_0_star_catalog import PC_TO_LY, generate_synthetic_name


def read_members(path):
    members = {}
    rejected = []
    with open(path, newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        required = {'id','proper','dist','x','y','z','comp_primary','comp','base','spect'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('HYG input missing required grouping/physical fields')
        for row in reader:
            source_id = row['id'].strip()
            if not source_id.isdigit() or source_id in members:
                raise ValueError(f'Invalid or duplicate HYG identity: {source_id}')
            try:
                coordinates = [float(row[k])*PC_TO_LY for k in ('x','y','z')]
                distance = float(row['dist'])*PC_TO_LY
                valid = all(math.isfinite(x) for x in [distance,*coordinates]) and distance >= 0
            except ValueError:
                coordinates, distance, valid = None, None, False
            # Keep raw rows even if astrometry is invalid, so companions are not
            # silently lost; invalid representative positions cannot be selected.
            if not valid:
                rejected.append(source_id)
            members[source_id] = {
                'hyg_id':source_id, 'proper':row['proper'].strip(),
                'primary_hyg_id':row['comp_primary'].strip() or source_id,
                'component':row['comp'].strip(), 'base':row['base'].strip(),
                'spect':row['spect'], 'coordinates_ly':coordinates if valid else None,
                'catalog_distance_ly':distance if valid else None,
                'source_properties':row,
            }
    return members, rejected


def group_members(members, overrides):
    """Follow catalog primary links, then apply explicit sourced root merges."""
    roots = {}
    for source_id in sorted(members, key=int):
        chain = []
        current = source_id
        while current not in roots:
            if current not in members:
                raise ValueError(f'Missing primary {current} referenced by {source_id}')
            if current in chain:
                raise ValueError(f'Cyclic primary membership involving {source_id}')
            chain.append(current)
            parent = members[current]['primary_hyg_id']
            if parent == current:
                roots[current] = current
                break
            current = parent
        root = roots[current]
        for node in chain:
            roots[node] = root
    if overrides.get('schema_version') != 1:
        raise ValueError('Unsupported membership override schema')
    labels, evidence, used_roots = {}, {}, set()
    for override in overrides['groups']:
        primary = override['primary_hyg_id']
        ids = override['member_hyg_ids']
        if primary not in ids or any(i not in members for i in ids):
            raise ValueError('Override requires existing members and an included primary')
        if not override.get('source_url') or not override.get('reason') or not override.get('name'):
            raise ValueError('Override needs name, reason, and source attribution')
        merge_roots = {roots[i] for i in ids}
        if merge_roots & used_roots or primary in used_roots:
            raise ValueError('Overlapping membership overrides require an explicit combined group')
        if '0' in merge_roots and len(merge_roots) > 1:
            raise ValueError('Sol cannot be merged with another stellar system')
        used_roots.update(merge_roots | {primary})
        for node in roots:
            if roots[node] in merge_roots:
                roots[node] = primary
        labels[primary] = override['name']
        evidence[primary] = override
    grouped = defaultdict(list)
    for node, root in roots.items():
        grouped[root].append(members[node])
    systems = []
    for primary, group in sorted(grouped.items(), key=lambda pair:int(pair[0])):
        group.sort(key=lambda m:(m['hyg_id'] != primary,int(m['hyg_id'])))
        representative = members[primary]
        names = [m['proper'] for m in group if m['proper']]
        name = labels.get(primary) or representative['proper'] or (names[0] if names else '')
        if not name:
            name = generate_synthetic_name({'id':primary})
        if len(group)>1 and name.endswith(' A'):
            name = name[:-2]
        point = representative['coordinates_ly']
        issues=[]
        if any(m['coordinates_ly'] is None for m in group):
            issues.append('invalid_member_astrometry')
        span = max((math.dist(point,m['coordinates_ly']) for m in group
                    if point is not None and m['coordinates_ly'] is not None), default=0)
        if span>1:
            issues.append('catalog_member_offset_exceeds_1_ly')
        if len(group)==1 and representative['component'] not in ('','1'):
            issues.append('secondary_component_without_cataloged_primary_companion')
        systems.append({'id':int(primary),'system_key':f'hyg:{primary}', 'proper':name,
            'primary_hyg_id':primary,'is_named':bool(names),'member_names':names,
            'members':group,'member_count':len(group),'point':point,
            'dist_ly':math.dist(point,[0,0,0]) if point is not None else None,
            'spect':representative['spect'],'is_sol':primary=='0',
            'grouping_basis':'sourced_override' if primary in evidence else 'hyg_comp_primary',
            'override':evidence.get(primary),'quality_flags':issues,'max_member_offset_ly':span})
    return systems


def select_systems(systems, radius, limit, shape="sphere"):
    if shape not in ("sphere", "cube") or not math.isfinite(radius) or radius <= 0:
        raise ValueError("Invalid neighborhood shape or extent")
    sol=[s for s in systems if s['id']==0 and s['proper']=='Sol'
         and s['dist_ly'] is not None and s['dist_ly']<0.01]
    if len(sol)!=1:
        raise ValueError('Exactly one valid Sol system is required')
    nearby=[s for s in systems if s['dist_ly'] is not None and (max(abs(c) for c in s['point'])<=radius if shape=='cube' else s['dist_ly']<=radius)]
    # Names on any member confer preference; count one named destination per system.
    chosen=sorted(nearby,key=lambda s:(not s['is_sol'],not s['is_named'],s['dist_ly'],s['id']))[:limit]
    return sorted(chosen,key=lambda s:(not s['is_sol'],s['dist_ly'],s['id'])), len(nearby)
