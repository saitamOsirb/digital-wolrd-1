import struct
import unittest
from export_tmd_mesh import decode_unlit_mesh

def synthetic(mode=0x20, flags=1, indices=(0, 1, 2)):
    header = struct.pack("<III", 0x41, 0, 1)
    obj = struct.pack("<7I", 28, 4, 0, 0, 60, 1, 0)
    verts = b"".join(struct.pack("<hhhh", x, y, z, 0) for x,y,z in (
        (0,0,0),(100,0,0),(0,100,0),(100,100,0)))
    packed = struct.pack("<" + "H" * len(indices), *indices)
    packed += bytes(8 - len(packed))
    packet = struct.pack("<BBBBBBBB", 3, 3, flags, mode, 255, 128, 32, 0) + packed
    return header + obj + verts + packet

class TMDMeshTests(unittest.TestCase):
    def test_unlit_triangle(self):
        result = decode_unlit_mesh(synthetic())
        self.assertEqual(result["triangleCount"], 1)
        self.assertEqual(result["objects"][0]["faces"][0]["indices"], [0, 1, 2])
        self.assertEqual(result["objects"][0]["faces"][0]["rgb"], [255,128,32])
    def test_unlit_quad(self):
        result = decode_unlit_mesh(synthetic(0x28,1,(0,1,2,3)))
        self.assertEqual(result["triangleCount"], 2)
    def test_unsupported_is_explicit(self):
        result = decode_unlit_mesh(synthetic(0x24,1))
        self.assertEqual(result["triangleCount"], 0)
        self.assertEqual(sum(result["skippedModes"].values()), 1)
    def test_invalid_vertex_reference(self):
        with self.assertRaises(ValueError):
            decode_unlit_mesh(synthetic(0x20,1,(0,1,99)))
if __name__ == "__main__":
    unittest.main()
