import struct
import unittest
from export_tmd_vertices import read_vertices

class TMDVertexTests(unittest.TestCase):
    def test_one_model_object(self):
        header = struct.pack("<III", 0x41, 0, 1)
        obj = struct.pack("<7I", 28, 2, 0, 0, 44, 1, 0)
        vertices = struct.pack("<hhhhhhhh", 100, -20, 300, 0, -12, 44, 55, 0)
        doc = read_vertices(header + obj + vertices)
        self.assertEqual(doc["vertexCount"], 2)
        self.assertEqual(doc["objects"][0]["vertices"], [[100, -20, 300], [-12, 44, 55]])

    def test_rejects_absolute_pointers(self):
        with self.assertRaises(ValueError):
            read_vertices(struct.pack("<III", 0x41, 1, 1) + bytes(256))

    def test_rejects_truncated_geometry(self):
        with self.assertRaises(ValueError):
            read_vertices(struct.pack("<III7I", 0x41, 0, 1, 28, 2, 0, 0, 0, 0, 0))

if __name__ == "__main__":
    unittest.main()
