"""Accepted artifact validation and corruption detection."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from universe_builder.validation.phase0 import validate

ACCEPTED = Path(__file__).resolve().parents[1]/'results/grouped-phase0-v1'


class ArtifactTests(unittest.TestCase):
    def copied_run(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        target=Path(temp.name)/'run'
        shutil.copytree(ACCEPTED,target)
        return target

    def update_hash(self, root, name):
        manifest=json.loads((root/'manifest.json').read_text())
        manifest['outputs'][name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
        (root/'manifest.json').write_text(json.dumps(manifest))

    def test_accepted_artifact(self):
        result=validate(ACCEPTED)
        self.assertEqual(result['retained_systems'],99)
        self.assertEqual(result['retained_named_systems'],30)
        self.assertEqual(result['reach_ly'],9.0)

    def test_checksum_detects_modified_file(self):
        root=self.copied_run()
        with (root/'phase_0/routes.csv').open('a') as f:f.write('0,1,1\n')
        with self.assertRaisesRegex(ValueError,'checksum'):
            validate(root)

    def test_missing_physical_edge_detected_even_with_updated_hash(self):
        root=self.copied_run()
        p=root/'phase_0/routes.csv'
        lines=p.read_text().splitlines()
        p.write_text('\n'.join([lines[0],*lines[2:]])+'\n')
        self.update_hash(root,'phase_0/routes.csv')
        with self.assertRaisesRegex(ValueError,'omits or adds'):
            validate(root)

    def test_member_assigned_twice_is_rejected_even_with_updated_hash(self):
        root=self.copied_run()
        p=root/'phase_0/stellar_members.json'
        data=json.loads(p.read_text())
        alpha=next(s for s in data['systems'] if s['name']=='Alpha Centauri')
        alpha['members'][1]=alpha['members'][0]
        p.write_text(json.dumps(data))
        self.update_hash(root,'phase_0/stellar_members.json')
        with self.assertRaises(ValueError):validate(root)


if __name__=='__main__':unittest.main()
