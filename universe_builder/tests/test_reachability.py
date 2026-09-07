"""Graph-analysis checks independent of the catalog generation algorithms."""
import math
import unittest

from universe_builder.analysis.reachability import (
    critical_distances, graph_stats, minimum_spanning_tree, sparse_route_example,
)


def distances(points):
    return [[abs(a-b) for b in points] for a in points]


class ReachabilityTests(unittest.TestCase):
    def test_no_isolates_does_not_mean_connected(self):
        result = graph_stats(distances([0, 1, 10, 11]), 1)
        self.assertEqual(result['isolated_systems'], 0)
        self.assertEqual(result['components'], 2)

    def test_seventh_neighbor_boundary_is_exclusive(self):
        matrix = distances(range(8))
        result = critical_distances(matrix)
        limit = result['six_neighbor_radius_exclusive_upper_bound_ly']
        self.assertEqual(graph_stats(matrix, limit)['max_neighbors'], 7)
        self.assertLessEqual(graph_stats(matrix, math.nextafter(limit, -math.inf))['max_neighbors'], 6)
        self.assertTrue(result['connected_degree_1_to_6_possible'])

    def test_dense_group_and_remote_system_are_incompatible(self):
        result = critical_distances(distances([*range(8), 100]))
        self.assertEqual(result['connected_radius_ly'], 93)
        self.assertFalse(result['degree_1_to_6_possible'])

    def test_mst_threshold_connects_but_smaller_radius_does_not(self):
        matrix = distances([0, 1, 2, 3, 10, 11, 12, 13])
        tree = minimum_spanning_tree(matrix)
        self.assertEqual(len(tree), 7)
        limit = max(edge[0] for edge in tree)
        self.assertEqual(limit, 7)
        self.assertEqual(graph_stats(matrix, limit)['components'], 1)
        self.assertEqual(graph_stats(matrix, math.nextafter(limit, -math.inf))['components'], 2)

    def test_sparse_routes_respect_bounds_or_reject(self):
        matrix = distances(range(8))
        result = sparse_route_example(matrix, radius=2, cap=3, target=2)
        self.assertEqual(result['components'], 1)
        self.assertLessEqual(result['max_neighbors'], 3)
        self.assertLessEqual(result['max_route_length_ly'], 2)
        self.assertGreaterEqual(result['min_neighbors'], 1)
        with self.assertRaises(ValueError):
            sparse_route_example(matrix, radius=0.5)


if __name__ == '__main__':
    unittest.main()
