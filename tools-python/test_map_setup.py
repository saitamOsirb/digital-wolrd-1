import struct
import unittest
from map_setup import parse_setup
from import_map_setup import read_setup_file

def fixture():
    values = [0] * 38
    values[0:6] = [1,2,3,4,5,6]
    values[27] = 256
    values[36:38] = [2,2]
    return struct.pack("<42i", *(values + [-1, 7, 8, -1]))

class SetupTests(unittest.TestCase):
    def test_reads_camera_and_tiles(self):
        data = parse_setup(fixture())
        self.assertEqual(data["camera"]["position"], [2,4,6])
        self.assertEqual(data["camera"]["target"], [8,10,12])
        self.assertEqual(data["camera"]["projectionDistance"], 256)
        self.assertEqual(data["nonemptyTiles"], 2)

    def test_map_offset(self):
        doc = read_setup_file(struct.pack("<I", 8) + bytes(4) + fixture())
        self.assertEqual(doc["widthTiles"], 2)

    def test_rejects_truncation(self):
        with self.assertRaises(ValueError):
            parse_setup(fixture()[:-2])
        with self.assertRaises(ValueError):
            read_setup_file(struct.pack("<I", 999) + bytes(4))

if __name__ == "__main__":
    unittest.main()
