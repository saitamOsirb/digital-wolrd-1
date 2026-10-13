import struct
import unittest
from psx_vram import Vram

def block(x, y, w, h, words):
    return struct.pack("<IHHHH", 12 + len(words), x, y, w, h) + words

class VramTests(unittest.TestCase):
    def test_16bit_pixel(self):
        gpu = Vram()
        gpu.load_tim(struct.pack("<II", 0x10, 2) + block(0, 0, 1, 1, struct.pack("<H", 0x001F)))
        self.assertEqual(gpu.texel(0x100, 0, 0, 0), (255, 0, 0, 255))

    def test_4bit_palette(self):
        gpu = Vram()
        palette = [0] * 16
        palette[3] = 0x03E0
        clut = block(0, 10, 16, 1, struct.pack("<16H", *palette))
        pixels = block(0, 0, 1, 1, struct.pack("<H", 0x0003))
        gpu.load_tim(struct.pack("<II", 0x10, 8) + clut + pixels)
        self.assertEqual(gpu.texel(0, 10 << 6, 0, 0), (0, 255, 0, 255))

    def test_8bit_indices(self):
        gpu = Vram()
        colors = [0] * 256
        colors[5] = 0x7C00
        gpu.upload(0, 10, 256, 1, struct.pack("<256H", *colors))
        gpu.upload(0, 0, 1, 1, struct.pack("<H", 0x0500))
        self.assertEqual(gpu.texel(0x80, 10 << 6, 1, 0), (0, 0, 255, 255))

    def test_out_of_bounds(self):
        with self.assertRaises(ValueError):
            Vram().upload(1023, 0, 2, 1, bytes(4))
        with self.assertRaises(ValueError):
            Vram().load_tim(bytes(8))

if __name__ == "__main__":
    unittest.main()
