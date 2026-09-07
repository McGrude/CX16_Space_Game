"""Membership and network invariants for the grouped Phase 0 pipeline."""
import copy
import csv
import json
import tempfile
from pathlib import Path
import unittest

from universe_builder.phases.system_grouping import group_members,select_systems,read_members
from universe_builder.phases.phase_0_stellar_systems import validate_network
from universe_builder import __main__ as runner


def member(i, parent=None, name='', x=0, component='1'):
    return {'hyg_id':str(i),'primary_hyg_id':str(i if parent is None else parent),
            'proper':name,'component':component,'base':'','spect':'G2V',
            'coordinates_ly':[x,0,0],'catalog_distance_ly':abs(x),'source_properties':{}}


EMPTY={'schema_version':1,'groups':[]}


class GroupingTests(unittest.TestCase):
    def test_catalog_pair_one_destination_preserves_both_stars(self):
        raw={'0':member(0,name='Sol'),'1':member(1,name='Sirius',x=8),
             '2':member(2,parent=1,x=8.001,component='2')}
        systems=group_members(raw,EMPTY)
        self.assertEqual(len(systems),2)
        self.assertEqual(systems[1]['member_count'],2)
        self.assertEqual(systems[1]['point'],[8,0,0])
        self.assertEqual(systems[1]['members'][1]['coordinates_ly'],[8.001,0,0])

    def test_nearby_unrelated_stars_are_not_merged(self):
        systems=group_members({'1':member(1,x=1),'2':member(2,x=1.000001)},EMPTY)
        self.assertEqual(len(systems),2)

    def test_sourced_override_merges_roots_preserving_primary_and_aliases(self):
        raw={'1':member(1,name='A',x=4),'2':member(2,parent=1,name='B',x=4),
             '3':member(3,name='Proxima',x=3.9)}
        override={'schema_version':1,'groups':[{'primary_hyg_id':'1','member_hyg_ids':['1','2','3'],
                 'name':'Alpha Centauri','reason':'Fixture association','source_url':'https://example.test/source'}]}
        result=group_members(raw,override)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['id'],1)
        self.assertEqual(result[0]['member_names'],['A','B','Proxima'])
        self.assertEqual(result[0]['grouping_basis'],'sourced_override')
        del override['groups'][0]['source_url']
        with self.assertRaises(ValueError):
            group_members(raw,override)

    def test_group_before_radius_keeps_companion_outside_boundary(self):
        raw={'0':member(0,name='Sol'),'1':member(1,x=24.9),'2':member(2,parent=1,x=25.1)}
        systems,_=select_systems(group_members(raw,EMPTY),25,300)
        self.assertEqual(len(systems),2)
        self.assertEqual(systems[1]['member_count'],2)

    def test_cube_includes_corners_and_faces_but_excludes_each_outer_axis(self):
        raw={'0':member(0,name='Sol')}
        points=[[25,25,25],[-25,-25,-25],[25.001,0,0],[0,-25.001,0],[0,0,25.001]]
        for i,point in enumerate(points,1):
            raw[str(i)]=member(i)
            raw[str(i)]['coordinates_ly']=point
        grouped=group_members(raw,EMPTY)
        cube,count=select_systems(grouped,25,300,'cube')
        sphere,_=select_systems(grouped,25,300)
        self.assertEqual({s['id'] for s in cube},{0,1,2})
        self.assertEqual(count,3)
        self.assertEqual([s['id'] for s in sphere],[0])

    def test_cube_config_has_explicit_extent_and_fixed_reach(self):
        config,source=runner.load_config(runner.PACKAGE/'configs/grouped_systems_cube.json')
        command=runner.commands(config,source,Path('/tmp/cube-test'),0)[0]
        self.assertEqual(config['phase_0']['half_extent_ly'],25)
        self.assertEqual(config['phase_0']['reach_candidates_ly'],[9.0])
        self.assertEqual(command[command.index('--shape')+1],'cube')

    def test_missing_primary_and_cycles_rejected(self):
        for raw in [{'1':member(1,parent=2)}, {'1':member(1,parent=2),'2':member(2,parent=1)}]:
            with self.assertRaises(ValueError):
                group_members(raw,EMPTY)

    def test_duplicate_display_names_never_merge_ids(self):
        systems=group_members({'1':member(1,name='Shared'),'2':member(2,name='Shared')},EMPTY)
        self.assertEqual(len(systems),2)
        self.assertNotEqual(systems[0]['system_key'],systems[1]['system_key'])

    def test_companion_name_confers_system_preference(self):
        raw={'0':member(0,name='Sol'),'1':member(1,x=1),'2':member(2,x=2),
             '3':member(3,parent=2,name='Named companion',x=2)}
        systems,_=select_systems(group_members(raw,EMPTY),25,2)
        self.assertEqual([s['id'] for s in systems],[0,2])

    def test_order_independent_grouping_and_source_immutable(self):
        raw={'0':member(0,name='Sol'),'2':member(2,parent=1,x=3),'1':member(1,x=3)}
        original=copy.deepcopy(raw)
        first=group_members(raw,EMPTY)
        second=group_members(dict(reversed(list(raw.items()))),EMPTY)
        self.assertEqual(first,second)
        self.assertEqual(raw,original)

    def test_invalid_member_coordinates_preserved_as_flag(self):
        raw={'1':member(1,x=2),'2':member(2,parent=1)}
        raw['2']['coordinates_ly']=None
        result=group_members(raw,EMPTY)[0]
        self.assertEqual(result['member_count'],2)
        self.assertIn('invalid_member_astrometry',result['quality_flags'])

    def test_network_validator_checks_edges_and_connectivity(self):
        systems=[{'id':0,'point':[0,0,0]},{'id':1,'point':[1,0,0]},
                 {'id':2,'point':[10,0,0]},{'id':3,'point':[11,0,0]}]
        with self.assertRaises(ValueError):
            validate_network(systems,1)
        edges,degrees=validate_network(systems,9)
        self.assertEqual(len(edges),3)
        self.assertEqual(degrees,[1,2,2,1])

    def test_schema2_config_and_command_route_to_grouped_implementation(self):
        config,source=runner.load_config(runner.PACKAGE/'configs/grouped_systems.json')
        with tempfile.TemporaryDirectory() as tmp:
            command=runner.commands(config,source,Path(tmp),0)[0]
        self.assertTrue(command[1].endswith('phase_0_stellar_systems.py'))
        self.assertIn('--membership-overrides',command)
        self.assertIn('--reach-candidates',command)


if __name__=='__main__':
    unittest.main()
