"""Checks for candidate reachability pruning, separate from phase generation."""
import unittest
from universe_builder.analysis.pruning import prune_to_reachability
from universe_builder.analysis.reachability import graph_stats


def matrix(points):
    return [[abs(a-b) for b in points] for a in points]


class PruningTests(unittest.TestCase):
    def test_keep_only_sol_component(self):
        result = prune_to_reachability(matrix([0, 1, 10, 11]), 1)
        self.assertEqual(result['retained_indices'], [0, 1])

    def test_complete_graph_prunes_nodes_not_edges(self):
        distances = matrix(range(8))
        result = prune_to_reachability(distances, 7)
        kept = result['retained_indices']
        self.assertIn(0, kept)
        self.assertEqual(len(kept), 7)
        actual = graph_stats([[distances[i][j] for j in kept] for i in kept], 7)
        self.assertEqual(actual['min_neighbors'], 6)
        self.assertEqual(actual['max_neighbors'], 6)
        self.assertEqual(actual['components'], 1)

    def test_named_preference_preserves_named_entries_when_feasible(self):
        result = prune_to_reachability(matrix(range(8)), 7, preferred={0,1,2,3})
        self.assertTrue({0,1,2,3}.issubset(result['retained_indices']))
        self.assertEqual(result['preferred_retained'],4)
        self.assertEqual(result['retained_count'],7)

    def test_valid_network_is_preserved(self):
        result = prune_to_reachability(matrix(range(9)), 3)
        self.assertEqual(result['retained_count'], 9)

    def test_isolated_sol_has_no_valid_subset(self):
        self.assertIsNone(prune_to_reachability(matrix([0, 10, 11]), 1))

    def test_seeded_search_reproducible_and_valid(self):
        distances = matrix(range(16))
        first = prune_to_reachability(distances, 5, seed=7)
        self.assertEqual(first, prune_to_reachability(distances, 5, seed=7))
        kept = first['retained_indices']
        actual = graph_stats([[distances[i][j] for j in kept] for i in kept], 5)
        self.assertEqual(actual['components'], 1)
        self.assertGreaterEqual(actual['min_neighbors'], 1)
        self.assertLessEqual(actual['max_neighbors'], 6)
        self.assertEqual(first['edges'],actual['edges'])


if __name__ == '__main__':
    unittest.main()
