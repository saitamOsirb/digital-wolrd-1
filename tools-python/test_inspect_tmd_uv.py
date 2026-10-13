import struct
import unittest
from inspect_tmd_uv import inspect_uv

def fixture(mode=0x24, flags=1, truncate=False):
    count = 3 if mode == 0x24 else 4
    header = struct.pack("<III", 0x41, 0, 1)
    obj = struct.pack("<7I", 28, 4, 0, 0, 60, 1, 0)
    vertices = b"".join(struct.pack("<hhhh", i * 10, 0, 0, 0) for i in range(4))
    payload = bytes([128, 128, 128, 0])
    for i in range(count):
        payload += struct.pack("<BBH", 10+i, 20+i, 0x1234 if i == 0 else 0x5678 if i == 1 else 0)
    payload += struct.pack("<"+"H"*count, *range(count))
    if count == 3:
        payload += b"\x00\x00"
    packet = struct.pack("<BBBB", 0, len(payload)//4, flags, mode) + payload
    data = header + obj + vertices + packet
    return data[:-2] if truncate else data

class TMDUVTests(unittest.TestCase):
    def test_triangle_raw_uv_metadata(self):
        result = inspect_uv(fixture())
        face = result["objects"][0]["texturedFaces"][0]
        self.assertEqual(face["indices"], [0,1,2])
        self.assertEqual(face["uvRaw"], [[10,20],[11,21],[12,22]])
        self.assertEqual(face["clut"], 0x1234)
        self.assertEqual(face["tpage"], 0x5678)
        self.assertEqual(result["texturedFaceCount"], 1)

    def test_quad(self):
        result = inspect_uv(fixture(0x2C))
        self.assertEqual(result["objects"][0]["texturedFaces"][0]["indices"], [0,1,2,3])

    def test_unsupported_flags_are_skipped(self):
        result = inspect_uv(fixture(flags=0))
        self.assertEqual(result["texturedFaceCount"], 0)
        self.assertEqual(sum(result["skippedPackets"].values()), 1)

    def test_truncation_rejected(self):
        with self.assertRaises(ValueError):
            inspect_uv(fixture(truncate=True))

if __name__ == "__main__":
    unittest.main()
