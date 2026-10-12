import struct
import unittest
from inspect_tfs import inspect_tfs

class InspectTfsTests(unittest.TestCase):
    def test_header_without_palettes(self):
        result = inspect_tfs(struct.pack("<II", 123, 0) + bytes(15))
        self.assertEqual(result["headerWord"], 123)
        self.assertEqual(result["remainderStart"], 8)

    def test_palette_stride_is_512_bytes(self):
        payload = struct.pack("<II", 0, 2) + bytes(1024)
        result = inspect_tfs(payload)
        self.assertEqual(result["clutOffsets"], [8, 520])

    def test_known_tile_record_layout(self):
        tile = struct.pack("<I", 7) + bytes(16384)
        result = inspect_tfs(struct.pack("<II", 0, 0) + tile, 1)
        self.assertEqual(result["tileRecords"][0]["payloadOffset"], 12)
        self.assertEqual(result["tileRecords"][0]["payloadBytes"], 16384)

    def test_truncated_palette(self):
        with self.assertRaisesRegex(ValueError, "Truncated"):
            inspect_tfs(struct.pack("<II", 0, 1) + bytes(10))

    def test_truncated_tile(self):
        with self.assertRaisesRegex(ValueError, "Truncated"):
            inspect_tfs(struct.pack("<II", 0, 0) + bytes(10), 1)

if __name__ == "__main__":
    unittest.main()
