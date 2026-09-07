"""Grouped, named-preferred, connected stellar-system catalog generation."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys

if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))

from universe_builder.analysis.pruning import component, sweep
from universe_builder.phases.phase_0_star_catalog import project_to_grid, write_ascii_map
from universe_builder.phases.system_grouping import read_members, group_members, select_systems


def write_json(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def validate_network(systems, radius, cap=6):
    """Rebuild every physical edge independently of pruning's reported metrics."""
    if len(systems)<2 or len({s['id'] for s in systems})!=len(systems):
        raise ValueError('Network needs multiple systems with unique identities')
    roots=[i for i,s in enumerate(systems) if s['id']==0]
    if len(roots)!=1:
        raise ValueError('Network must contain Sol exactly once')
    adjacency=[set() for _ in systems]
    edges=[]
    for i,a in enumerate(systems):
        for j in range(i+1,len(systems)):
            b=systems[j]
            distance=math.dist(a['point'],b['point'])
            if distance<=radius:
                adjacency[i].add(j);adjacency[j].add(i)
                edges.append({'from_system_id':a['id'],'to_system_id':b['id'],'distance_ly':distance})
    degrees=[len(a) for a in adjacency]
    if not all(1<=d<=cap for d in degrees):
        raise ValueError('Network violates neighbor limits')
    if len(component(adjacency,set(range(len(systems))),roots[0]))!=len(systems):
        raise ValueError('Network is disconnected')
    return edges, degrees


def build(source, override_path, output, radius, max_systems, scale, reaches, trials, shape="sphere"):
    members, invalid=read_members(source)
    grouped=group_members(members,json.loads(Path(override_path).read_text()))
    candidates, nearby_count=select_systems(grouped,radius,max_systems,shape)
    if len(candidates)<2:
        raise ValueError('Not enough systems in the neighborhood')
    preferred={i for i,s in enumerate(candidates) if s['is_named']}
    matrix=[[math.dist(a['point'],b['point']) for b in candidates] for a in candidates]
    trials_by_reach=sweep(matrix,reaches,trials=trials,preferred=preferred)
    if not trials_by_reach:
        raise ValueError('No connected degree-bounded network found for configured reaches')
    chosen=max(trials_by_reach,key=lambda s:(s['preferred_retained'],s['retained_count'],-s['radius_ly'],-s['seed']))
    kept=[candidates[i] for i in chosen['retained_indices']]
    removed=[candidates[i] for i in chosen['removed_indices']]
    edges,degrees=validate_network(kept,chosen['radius_ly'])
    for s in kept:
        s['x_ly'],s['y_ly'],s['z_ly']=s['point']
    project_to_grid(kept,scale)
    cells={(s['grid_x'],s['grid_y']) for s in kept}
    if len(cells)!=len(kept):
        raise ValueError('Duplicate display cells')
    output=Path(output)
    # Runner owns directory creation; fail instead of replacing any phase output.
    if any(output.iterdir()):
        raise ValueError('Phase output directory must be empty')
    fields=['id','proper','dist_ly','grid_x','grid_y','spect','system_key',
            'primary_hyg_id','member_count','is_named','x_ly','y_ly','z_ly']
    with (output/'star_catalog.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader()
        for s in kept:
            writer.writerow({k:int(s[k]) if k=='is_named' else s[k] for k in fields})
    with (output/'routes.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['from_system_id','to_system_id','distance_ly'])
        writer.writeheader();writer.writerows(edges)
    write_ascii_map(kept,str(output/'star_map.txt'),scale,radius,shape=shape)
    write_json(output/'stellar_members.json',{'schema_version':2,'systems':[
        {'system_id':s['id'],'system_key':s['system_key'],'name':s['proper'],
         'primary_hyg_id':s['primary_hyg_id'],'grouping_basis':s['grouping_basis'],
         'override':s['override'],'members':s['members'],'quality_flags':s['quality_flags']} for s in kept]})
    candidate_audit=[]
    retained_ids={s['id'] for s in kept}
    for s in candidates:
        candidate_audit.append({k:s[k] for k in ['id','system_key','proper','primary_hyg_id',
          'is_named','member_count','member_names','point','dist_ly','grouping_basis',
          'quality_flags','max_member_offset_ly']})
        candidate_audit[-1].update(member_hyg_ids=[m['hyg_id'] for m in s['members']],
                                 retained=s['id'] in retained_ids)
    write_json(output/'candidate_systems.json',{'schema_version':2,'systems':candidate_audit})
    named_losses=[{'id':s['id'],'name':s['proper'],'member_names':s['member_names']} for s in removed if s['is_named']]
    summary={
        'schema_version':2,'source_rows':len(members),'invalid_astrometry_ids':invalid,
        'grouping_rule':'HYG primary links plus sourced overrides; no proximity merges',
        'coordinate_rule':'Designated primary position; not a computed mass barycenter',
        'neighborhood_shape':shape,
        ('neighborhood_half_extent_ly' if shape=='cube' else 'neighborhood_radius_ly'):radius,'systems_before_budget':nearby_count,
        'candidate_systems':len(candidates),'candidate_catalog_members':sum(s['member_count'] for s in candidates),
        'candidate_named_systems':len(preferred),'candidate_named_members':sum(len(s['member_names']) for s in candidates),
        'reach_ly':chosen['radius_ly'],'pruning_seed':chosen['seed'],'pruning_trials_per_reach':trials,
        'selection_objective':'named systems retained, then total systems, then smaller reach, then lower seed; heuristic, not globally optimal',
        'retained_systems':len(kept),'retained_catalog_members':sum(s['member_count'] for s in kept),
        'retained_named_systems':sum(s['is_named'] for s in kept),
        'retained_named_members':sum(len(s['member_names']) for s in kept),
        'pruned_systems':len(removed),'named_system_losses':named_losses,
        'single_member_destinations':sum(s['member_count']==1 for s in kept),
        'multiple_member_destinations':sum(s['member_count']>1 for s in kept),
        'components':1,'routes':len(edges),'min_neighbors':min(degrees),'max_neighbors':max(degrees),
        'mean_neighbors':sum(degrees)/len(degrees),
        'degree_histogram':{str(d):degrees.count(d) for d in sorted(set(degrees))},
        'sol_neighbors':[{'id':s['id'],'name':s['proper'],'distance_ly':math.dist(s['point'],[0,0,0])}
                         for s in kept if s['id']!=0 and math.dist(s['point'],[0,0,0])<=chosen['radius_ly']],
        'quality_flags':[{'id':s['id'],'name':s['proper'],'flags':s['quality_flags'],'retained':s['id'] in retained_ids}
                         for s in candidates if s['quality_flags']],
        'reach_comparison':[{k:v for k,v in result.items() if not k.endswith('_indices')} for result in trials_by_reach],
    }
    write_json(output/'selection_summary.json',summary)
    print(f"Grouped {summary['candidate_catalog_members']} catalog entries into {len(candidates)} candidate systems; "
          f"retained {len(kept)} systems at {chosen['radius_ly']} ly, {min(degrees)}–{max(degrees)} neighbors.")
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-csv',required=True)
    parser.add_argument('--membership-overrides',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--radius-ly',type=float,required=True,help='Sphere radius or cube half extent in ly')
    parser.add_argument('--shape',choices=['sphere','cube'],default='sphere')
    parser.add_argument('--max-stars',type=int,required=True,help='System candidate budget after grouping')
    parser.add_argument('--scale',type=float,required=True)
    parser.add_argument('--reach-candidates',type=float,nargs='+',required=True)
    parser.add_argument('--trials',type=int,required=True)
    args=parser.parse_args()
    build(args.input_csv,args.membership_overrides,args.output_dir,args.radius_ly,
          args.max_stars,args.scale,args.reach_candidates,args.trials,args.shape)


if __name__=='__main__':
    main()
