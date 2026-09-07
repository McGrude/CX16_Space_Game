"""Physical selection and display-layout regression tests."""
import unittest
from universe_builder.phases.phase_0_star_catalog import select_stars_within_radius, project_to_grid


def star(i, name, distance, x=0., y=0., z=0.):
    return dict(id=str(i), proper=name, dist_ly=distance, x_ly=x, y_ly=y, z_ly=z)


class Phase0SelectionTests(unittest.TestCase):
    def test_missing_sol_is_not_replaced_with_nearest_star(self):
        with self.assertRaises(ValueError):
            select_stars_within_radius([star(1, 'Other', 1, x=1)], 25, 300)

    def test_catalog_names_preferred_to_nearer_unnamed_entries(self):
        stars = [star(0, 'Sol', 0), star(1, '', 1, x=1), star(2, 'Named', 2, x=2)]
        selected = select_stars_within_radius(stars, 25, 2)
        self.assertEqual([s['id'] for s in selected], ['0', '2'])
        self.assertNotIn('is_sol', stars[0])

    def test_collisions_and_offscreen_entries_are_all_retained(self):
        stars = [star(0, 'Sol', 0), star(1, 'Named', 1, z=1),
                 star(2, '', 2, z=2), star(3, 'Edge', 25, x=25)]
        selected = select_stars_within_radius(stars, 25, 300)
        original = [(s['x_ly'],s['y_ly'],s['z_ly']) for s in selected]
        projected = project_to_grid(selected, .5)
        self.assertEqual(len(projected),4)
        cells = [(s['grid_x'],s['grid_y']) for s in projected]
        self.assertEqual(len(set(cells)),4)
        self.assertEqual(cells[0],(50,50))
        self.assertTrue(all(0 <= x < 100 and 0 <= y < 100 for x,y in cells))
        self.assertEqual(original,[(s['x_ly'],s['y_ly'],s['z_ly']) for s in projected])

    def test_selection_and_layout_independent_of_input_order(self):
        stars = [star(0, 'Sol', 0), star(1, '', 1, z=1), star(2, 'Named', 1, z=-1)]
        first = project_to_grid(select_stars_within_radius(stars,25,300),.5)
        second = project_to_grid(select_stars_within_radius(list(reversed(stars)),25,300),.5)
        self.assertEqual(first,second)

    def test_radius_and_invalid_numbers_exclude_entries(self):
        stars=[star(0,'Sol',0),star(1,'Too far',26,x=26),star(2,'Bad',1,x=float('nan'))]
        self.assertEqual(len(select_stars_within_radius(stars,25,300)),1)


if __name__ == '__main__':
    unittest.main()
