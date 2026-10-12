import struct
import unittest
from inspect_map_tiles import read_tile_layout

class TileLayoutTests(unittest.TestCase):
    def test_layout_and_sparse_tiles(self):
        data = bytes(12) + struct.pack("<ii6i", 3, 2, -1, 4, 4, -1, 12, 0)
        report = read_tile_layout(data, 12)
        self.assertEqual(report["nonemptyIndices"], [1, 2, 4, 5])
        self.assertEqual(report["nonemptyCount"], 4)
        self.assertEqual(report["width"], 3)
        self.assertEqual(report["height"], 2)

    def test_requires_aligned_offset(self):
        with self.assertRaises(ValueError):
            read_tile_layout(bytes(32), 1)

    def test_rejects_truncated_list(self):
        with self.assertRaises(ValueError):
            read_tile_layout(struct.pack("<ii", 3, 4), 0)

    def test_rejects_unreasonable_dimensions(self):
        with self.assertRaises(ValueError):
            read_tile_layout(struct.pack("<ii", 1000, 1000), 0)

if __name__ == "__main__":
    unittest.main()
