import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from universe_builder import __main__ as runner
from universe_builder.phases.phase_2_artifact_sites import validate_settings
from universe_builder.validation.phase2 import validate

ROOT=Path(__file__).resolve().parents[1]
ACCEPTED=ROOT/'results/physical-phase2-v1'


class ProductionArtifactTests(unittest.TestCase):
    def test_production_artifact_and_trial_parity(self):
        summary=validate(ACCEPTED)
        self.assertEqual(summary['categories'],{'technology':8,'archaeology':32})
        self.assertEqual(summary['minimum_technology_hops'],3)
        self.assertEqual((ACCEPTED/'phase_2/system_objects.csv').read_bytes(),
                         (ROOT/'results/phase2-blue-noise-trial-v1/system_objects.csv').read_bytes())
        config,source=runner.load_config(ROOT/'configs/grouped_systems_cube.json')
        self.assertTrue(runner.commands(config,source,Path('/tmp/world'),2)[2][1].endswith('phase_2_artifact_sites.py'))

    def test_review_map_corruption_detected_after_rehash(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'run';shutil.copytree(ACCEPTED,root)
            p=root/'phase_2/star_map.txt';p.write_text(p.read_text().replace('T','*',1))
            m=json.loads((root/'manifest.json').read_text())
            m['outputs']['phase_2/star_map.txt']=hashlib.sha256(p.read_bytes()).hexdigest()
            (root/'manifest.json').write_text(json.dumps(m))
            with self.assertRaisesRegex(ValueError,'map mismatch'):validate(root)

    def test_spacing_and_origin_config_rejected(self):
        c=json.loads((ACCEPTED/'manifest.json').read_text())['config']['phase_2']
        for k,v in [('technology_min_hops',0),('origin_site',{'system_id':0,'object_id':0}),('seed',-1)]:
            with self.assertRaises(ValueError):validate_settings({**c,k:v})
