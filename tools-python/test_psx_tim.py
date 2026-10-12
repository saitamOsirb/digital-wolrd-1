"""Self-contained synthetic TIM and PNG regression tests."""
import struct
import unittest
import zlib
from psx_tim import decode
from convert_tim import encode_png

def block(width, height, payload):
    return struct.pack("<IHHHH", 12 + len(payload), 0, 0, width, height) + payload

def tim(mode, payload, words, palette=b"", palette_width=0):
    flags = mode | (8 if palette else 0)
    header = struct.pack("<II", 16, flags)
    if palette:
        header += block(palette_width, 1, palette)
    return header + block(words, 1, payload)

class TIMTests(unittest.TestCase):
    def test_four_bit_palette(self):
        clut = struct.pack("<16H", 0, 0x001F, *([0] * 14))
        image = decode(tim(0, bytes([0x10, 0x11]), 1, clut, 16))
        self.assertEqual((image.width, image.height), (4, 1))
        self.assertEqual(image.rgba[:4], bytes([0, 0, 0, 0]))
        self.assertEqual(image.rgba[4:8], bytes([255, 0, 0, 255]))
    def test_eight_bit_palette(self):
        clut = struct.pack("<256H", 0, 0x03E0, *([0] * 254))
        image = decode(tim(1, bytes([1, 0]), 1, clut, 256))
        self.assertEqual(image.width, 2)
        self.assertEqual(image.rgba[:4], bytes([0, 255, 0, 255]))
    def test_sixteen_bit(self):
        image = decode(tim(2, struct.pack("<H", 0x7C00), 1))
        self.assertEqual(image.rgba, bytes([0, 0, 255, 255]))
    def test_twenty_four_bit(self):
        image = decode(tim(3, bytes([10, 20, 30, 40, 50, 60]), 3))
        self.assertEqual(image.width, 2)
        self.assertEqual(image.rgba, bytes([10,20,30,255,40,50,60,255]))
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            decode(b"not a tim")
        with self.assertRaises(ValueError):
            decode(tim(2, b"\x00", 1))
    def test_png_signature_and_pixels(self):
        png = encode_png(1, 1, bytes([1, 2, 3, 255]))
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        marker = png.index(b"IDAT")
        compressed_length = struct.unpack_from(">I", png, marker - 4)[0]
        raster = zlib.decompress(png[marker + 4:marker + 4 + compressed_length])
        self.assertEqual(raster, bytes([0, 1, 2, 3, 255]))

if __name__ == "__main__":
    unittest.main()
