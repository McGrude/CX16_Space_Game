import json
from pathlib import Path
import tempfile
import unittest
from universe_builder.export.runtime_ids import export, translate

ROOT = Path(__file__).resolve().parents[1]


class RuntimeIDsTests(unittest.TestCase):
    def test_sparse_ids_and_local_parent_translation(self):
        systems = [{'id':'900'}, {'id':'0'}]
        objects = [dict(system_id='900',object_id='70',parent_object_id='20'),
                   dict(system_id='900',object_id='20',parent_object_id='')]
        routes = [dict(from_system_id='0',to_system_id='900')]
        mapping, local, converted, adjacency = translate(systems,objects,routes)
        self.assertEqual(mapping,{0:0,900:1})
        self.assertEqual(converted[0]['parent_object_id'],255)
        self.assertEqual(converted[1]['parent_object_id'],0)
        self.assertEqual(adjacency,[{1},{0}])
        self.assertEqual(translate(list(reversed(systems)),list(reversed(objects)),routes),
                         (mapping,local,converted,adjacency))
        objects[0]['parent_object_id']='99'
        with self.assertRaises(ValueError): translate(systems,objects,routes)

    def test_system_byte_capacity(self):
        with self.assertRaises(ValueError):
            translate([{'id':str(i)} for i in range(256)],[],[])

    def test_export_replay_header_and_binary_references(self):
        with tempfile.TemporaryDirectory() as temp:
            a,b=Path(temp)/'a',Path(temp)/'b'
            args=(ROOT/'results/grouped-phase0-cube-v2',ROOT/'results/phase1-cube-v3')
            m=export(*args,a)
            export(*args,b)
            for path in a.iterdir():self.assertEqual(path.read_bytes(),(b/path.name).read_bytes())
            header=(a/'world_header.bin').read_bytes()
            self.assertEqual(header[:5],b'CX16\x01')
            self.assertEqual(header[5:].hex(),m['world_id'])
            data=(a/'neighbors.bin').read_bytes()
            self.assertEqual(len(data),170*7)
            for index in range(170):
                record=data[index*7:(index+1)*7]
                self.assertTrue(1<=record[0]<=6)
                self.assertTrue(all(n<170 for n in record[1:1+record[0]]))
                self.assertEqual(record[1+record[0]:],bytes([255])*(6-record[0]))
            self.assertEqual(len((a/'spob_refs.bin').read_bytes()),274*3)
            with self.assertRaises(ValueError):export(*args,a)
