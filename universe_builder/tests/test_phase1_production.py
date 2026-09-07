import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from universe_builder.phases.phase_1_system_objects import generate_objects_for_system, validate_weights
from universe_builder.validation.phase1 import validate

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT/'results/physical-phase1-v1'


class ProductionPhase1Tests(unittest.TestCase):
    def test_cap_includes_moons_and_seed_changes_output(self):
        for cap in range(6):
            for sid in range(1,40):
                objects=generate_objects_for_system(sid,'Fixture','G2V',42,cap,[(i,100 if i==5 else 0) for i in range(6)])
                self.assertEqual(len(objects),cap)
        self.assertNotEqual([generate_objects_for_system(i,'Fixture','G2V',42) for i in range(1,20)],
                            [generate_objects_for_system(i,'Fixture','G2V',43) for i in range(1,20)])

    def test_bad_weights_rejected(self):
        for weights in ([],[[0,100]],[(i,True) for i in range(6)],[(i,-1) for i in range(6)]):
            with self.assertRaises(ValueError):validate_weights(weights)

    def test_accepted_artifact_and_exact_promotion(self):
        self.assertEqual(validate(ACCEPTED)['objects'],274)
        self.assertEqual((ACCEPTED/'phase_1/system_objects.csv').read_bytes(),
                         (ROOT/'results/phase1-cube-v3/system_objects.csv').read_bytes())

    def test_overlap_detected_even_after_rehash(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'run';shutil.copytree(ACCEPTED,target)
            p=target/'phase_1/system_objects.csv'
            with p.open() as f:rows=list(csv.DictReader(f))
            sol=[r for r in rows if r['system_id']=='0']
            sol[1]['local_x'],sol[1]['local_y']=sol[0]['local_x'],sol[0]['local_y']
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            m=json.loads((target/'manifest.json').read_text())
            m['outputs']['phase_1/system_objects.csv']=hashlib.sha256(p.read_bytes()).hexdigest()
            (target/'manifest.json').write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError,'Overlapping'):validate(target)
