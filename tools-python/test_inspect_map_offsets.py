import struct
import unittest
from inspect_map_offsets import inspect_offsets

class OffsetTests(unittest.TestCase):
    def test_valid_table(self):
        data = struct.pack("<III", 12, 16, 24) + bytes(20)
        result = inspect_offsets(data, 3)
        self.assertEqual(result["offsets"], [12, 16, 24])
        self.assertEqual(result["segments"][1]["length"], 8)

    def test_reject_outside_file(self):
        with self.assertRaises(ValueError):
            inspect_offsets(struct.pack("<I", 100), 1)

    def test_reject_descending(self):
        with self.assertRaises(ValueError):
            inspect_offsets(struct.pack("<II", 12, 8) + bytes(8), 2)

    def test_reject_table_pointer(self):
        with self.assertRaises(ValueError):
            inspect_offsets(struct.pack("<II", 4, 12) + bytes(8), 2)

if __name__ == "__main__":
    unittest.main()
