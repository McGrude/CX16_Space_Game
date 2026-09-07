"""Reachability review of current selection without historical map pruning."""
import hashlib
import json
import math
from pathlib import Path
from universe_builder.analysis.pruning import sweep
from universe_builder.phases.phase_0_star_catalog import load_hyg_csv, select_stars_within_radius

ROOT = Path(__file__).resolve().parents[2]


def main():
    config_path = ROOT/'universe_builder/configs/baseline.json'
    config = json.loads(config_path.read_text())
    source = (config_path.parent/config['source_catalog']).resolve()
    settings = config['phase_0']
    stars = select_stars_within_radius(load_hyg_csv(str(source)), settings['radius_ly'], settings['max_stars'])
    preferred = {i for i,s in enumerate(stars) if s['proper'].strip()}
    points = [[s[k] for k in ('x_ly','y_ly','z_ly')] for s in stars]
    distances = [[math.dist(a,b) for b in points] for a in points]
    results = sweep(distances,[8.,8.5,9.,9.4,9.5,10.,10.3],preferred=preferred)
    print(json.dumps({
        'status':'design experiment; not a production catalog',
        'candidate_count':len(stars),'catalog_named_count_including_sol':len(preferred),
        'settings':settings,'trials_per_radius':8,
        'preference':'Minimize named losses at each removal, then excess-degree reduction per lost node; prefer named reinsertion. Select trials by names retained, then total retained. Heuristic, not globally optimal.',
        'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,config_path)},
        'implementation_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [Path(__file__),ROOT/'universe_builder/analysis/pruning.py',ROOT/'universe_builder/phases/phase_0_star_catalog.py']},
        'candidates':[{'index':i,'hyg_id':s['id'],'catalog_name':s['proper'],'dist_ly':s['dist_ly']} for i,s in enumerate(stars)],
        'pruning_sweep':results,
    },indent=2))


if __name__ == '__main__':
    main()
