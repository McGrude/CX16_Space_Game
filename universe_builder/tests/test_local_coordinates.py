"""Display collision resolution preserves objects and deterministic placement."""
import copy
import unittest
from universe_builder.phases.phase_1_system_objects import resolve_local_coordinate_overlaps


class LocalCoordinatesTests(unittest.TestCase):
    def test_parent_priority_ties_and_input_order(self):
        objects = [
            dict(object_id=0, is_moon=1, parent_object_id=1, local_x=10, local_y=10),
            dict(object_id=1, is_moon=0, parent_object_id=None, local_x=10, local_y=10),
            dict(object_id=2, is_moon=0, parent_object_id=None, local_x=30, local_y=30),
        ]
        original = copy.deepcopy(objects)
        reverse = copy.deepcopy(list(reversed(objects)))
        resolve_local_coordinate_overlaps(objects)
        resolve_local_coordinate_overlaps(reverse)
        self.assertEqual(objects, list(reversed(reverse)))
        self.assertEqual((objects[0]['local_x'], objects[0]['local_y']), (10, 9))
        self.assertEqual(objects[1:], original[1:])
        for before, after in zip(original, objects):
            self.assertEqual({k:v for k,v in before.items() if not k.startswith('local_')},
                             {k:v for k,v in after.items() if not k.startswith('local_')})
        placed = copy.deepcopy(objects)
        resolve_local_coordinate_overlaps(objects)
        self.assertEqual(objects, placed)

    def test_corner_collisions_stay_in_bounds(self):
        for corner in (0,49):
            objects = [dict(object_id=i, is_moon=0, local_x=corner, local_y=corner)
                       for i in range(5)]
            resolve_local_coordinate_overlaps(objects)
            self.assertEqual(len({(o['local_x'],o['local_y']) for o in objects}),5)
            self.assertTrue(all(0 <= o[k] < 50 for o in objects for k in ('local_x','local_y')))
