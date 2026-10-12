import struct
import unittest
from render_tfs_map import decode_tfs_map

def make_tfs():
    palette = [0] * 256
    palette[1] = 31
    palette[2] = 31 << 5
    palette[3] = 31 << 10
    output = bytearray(struct.pack("<HHI", 2, 1, 1))
    output.extend(struct.pack("<256H", *palette))
    for value in (1, 2):
        output.extend(struct.pack("<I", 0x2000140))
        output.extend(bytes([value]) * (128 * 128))
    return bytes(output)

class OriginalTfsTests(unittest.TestCase):
    def test_renders_two_real_format_tiles_in_order(self):
        width, height, rgba = decode_tfs_map(make_tfs())
        self.assertEqual((width, height), (256, 128))
        self.assertEqual(rgba[:4], bytes([255, 0, 0, 255]))
        self.assertEqual(rgba[128 * 4:128 * 4 + 4], bytes([0, 255, 0, 255]))
    def test_reject_truncated_stream(self):
        with self.assertRaises(ValueError):
            decode_tfs_map(make_tfs()[:-1])
    def test_reject_bad_palette(self):
        with self.assertRaises(ValueError):
            decode_tfs_map(make_tfs(), 3)

if __name__ == "__main__":
    unittest.main()
