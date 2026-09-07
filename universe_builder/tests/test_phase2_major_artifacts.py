import copy
import json
from pathlib import Path
import unittest
from universe_builder.analysis.phase2_major_artifacts import place

CONFIG=json.loads((Path(__file__).resolve().parents[1]/'configs/phase2_major_artifacts_trial.json').read_text())


class MajorArtifactTests(unittest.TestCase):
    def rows(self):
        return [dict(system_id=str(i),object_id='2',name='Fixture',
                     **{'class':'GG' if i>60 else 'RP'}) for i in range(80)]

    def test_quota_origin_exclusion_pass_through_and_order(self):
        rows=self.rows();original=copy.deepcopy(rows)
        result=place(rows,CONFIG)
        self.assertEqual(rows,original)
        self.assertEqual(result,list(reversed(place(list(reversed(rows)),CONFIG))))
        self.assertEqual(sum(r['artifact_category']=='technology' for r in result),8)
        self.assertEqual(sum(r['artifact_category']=='archaeology' for r in result),32)
        self.assertEqual(result[0]['technology_id'],'interstellar_propulsion')
        self.assertTrue(all(r['artifact_flag']=='0' for r in result if r['class']=='GG'))
        self.assertEqual(len({r['technology_id'] for r in result if r['technology_id']}),8)
        for before,after in zip(rows,result):
            self.assertTrue(all(after[k]==v for k,v in before.items()))

    def test_seed_variation_keeps_origin(self):
        config=copy.deepcopy(CONFIG);config['seed']+=1
        a,b=place(self.rows(),CONFIG),place(self.rows(),config)
        self.assertNotEqual(a,b)
        self.assertEqual(a[0],b[0])

    def test_invalid_quota_or_origin_rejected(self):
        for field,value in [('archaeological_sites',1000),('archaeological_sites',-1),
                            ('origin_site',dict(system_id=1,object_id=2))]:
            config=copy.deepcopy(CONFIG);config[field]=value
            with self.assertRaises(ValueError):place(self.rows(),config)
