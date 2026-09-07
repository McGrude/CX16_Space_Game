import unittest
from universe_builder.analysis.phase2_major_artifacts import hop_distances, select_spaced


class ArtifactSpacingTests(unittest.TestCase):
    def test_hops_and_separation_on_chain(self):
        routes=[dict(from_system_id=i,to_system_id=i+1) for i in range(10)]
        hops=hop_distances(routes)
        self.assertEqual(hops[0][10],10)
        selected=select_spaced([(i,0) for i in range(1,11)],(0,2),4,hops,3)
        self.assertEqual(selected,[(0,2),(3,0),(6,0),(9,0)])
        with self.assertRaisesRegex(ValueError,'no relaxation'):
            select_spaced([(i,0) for i in range(1,11)],(0,2),5,hops,3)

    def test_disconnected_graph_rejected(self):
        with self.assertRaises(ValueError):
            hop_distances([dict(from_system_id=0,to_system_id=1),dict(from_system_id=2,to_system_id=3)])
