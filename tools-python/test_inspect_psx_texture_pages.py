import unittest
from inspect_psx_texture_pages import annotate, clut_fields, tpage_fields

class TexturePageTests(unittest.TestCase):
    def test_tpage_coordinates_and_depth(self):
        self.assertEqual(tpage_fields(0x0093)["x"], 192)
        self.assertEqual(tpage_fields(0x0093)["y"], 256)
        self.assertEqual(tpage_fields(0x0093)["depthBpp"], 8)
    def test_clut_coordinates(self):
        value = 5 + (123 << 6)
        self.assertEqual(clut_fields(value), {"raw": value, "x": 80, "y": 123})
    def test_invalid_metadata(self):
        with self.assertRaises(ValueError):
            clut_fields(65536)
        with self.assertRaises(ValueError):
            tpage_fields(-1)
    def test_report_annotation(self):
        report = {"format": "psx-tmd-textured-uv-survey",
                  "objects":[{"texturedFaces":[{"clut":1, "tpage":0x80}]}]}
        out = annotate(report)
        self.assertEqual(out["gpuMetadataFaceCount"], 1)
        self.assertEqual(out["objects"][0]["texturedFaces"][0]["texturePage"]["depthBpp"], 8)

if __name__ == "__main__":
    unittest.main()
