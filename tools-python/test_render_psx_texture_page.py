import struct
import unittest
import zlib
from psx_vram import Vram
from render_psx_texture_page import render_page

class RenderPageTests(unittest.TestCase):
    def test_exports_png_with_sampled_16bit_texel(self):
        gpu = Vram()
        gpu.upload(0, 0, 1, 1, struct.pack("<H", 0x001f))
        png = render_page(gpu, 0x100, 0)
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(struct.unpack_from(">II", png, 16), (256, 256))
        payload_start = png.find(b"IDAT")
        data_length = struct.unpack_from(">I", png, payload_start - 4)[0]
        raw = zlib.decompress(png[payload_start+4:payload_start+4+data_length])
        self.assertEqual(raw[1:5], bytes([255, 0, 0, 255]))

    def test_bad_texture_depth(self):
        with self.assertRaises(ValueError):
            render_page(Vram(), 0x180, 0)

if __name__ == "__main__":
    unittest.main()
