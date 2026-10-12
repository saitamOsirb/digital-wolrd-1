import unittest
from generate_demo_texture import make_tim
from psx_tim import decode
from convert_tim import encode_png

class FixtureTests(unittest.TestCase):
    def test_tim_decoding(self):
        img = decode(make_tim())
        self.assertEqual((img.width, img.height), (32,32))
        self.assertEqual(len(img.rgba), 4096)
        self.assertTrue(any(channel != 0 for channel in img.rgba))
    def test_export_png(self):
        image = decode(make_tim(8,8))
        png = encode_png(image.width, image.height, image.rgba)
        self.assertTrue(png.startswith(bytes([137,80,78,71,13,10,26,10])))
    def test_reject_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            make_tim(0, 32)

if __name__ == "__main__":
    unittest.main()
