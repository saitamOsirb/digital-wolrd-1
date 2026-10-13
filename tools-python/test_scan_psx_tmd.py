import struct
import unittest
from scan_psx_tmd import scan_tmd

def fixture(objects=1, flags=0):
    head = struct.pack("<III", 0x41, flags, objects)
    obj = struct.pack("<7I", 128, 6, 256, 4, 384, 2, 0)
    return head + obj * objects + bytes(512)

class TMDScanTests(unittest.TestCase):
    def test_candidate_with_nonzero_offset(self):
        data = bytes(16) + fixture()
        result = scan_tmd(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["byteOffset"], 16)
        self.assertEqual(result[0]["headers"][0]["vertices"], 6)

    def test_invalid_flags_and_truncation(self):
        self.assertEqual(scan_tmd(fixture(flags=8)), [])
        self.assertEqual(scan_tmd(fixture()[:18]), [])

    def test_disallow_zero_geometry(self):
        data = struct.pack("<III7I", 0x41, 0, 1, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(scan_tmd(data), [])

if __name__ == "__main__":
    unittest.main()
