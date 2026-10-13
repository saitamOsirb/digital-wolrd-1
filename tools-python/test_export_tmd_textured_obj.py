import unittest
from export_tmd_textured_obj import export_textured

REPORT = {"format":"psx-tmd-textured-uv-survey","objects":[
 {"index":0,"vertices":[[0,0,0],[100,0,0],[0,100,0],[100,100,0]],
 "texturedFaces":[{"tpage":128,"clut":123,"indices":[0,1,2],"uvRaw":[[0,0],[255,0],[0,255]]},
                  {"tpage":0,"clut":123,"indices":[0,1,2,3],"uvRaw":[[0,0],[1,0],[1,1],[0,1]]}]}]}

class TexturedOBJTests(unittest.TestCase):
    def test_filters_page_and_generates_uv(self):
        obj, mtl, count = export_textured(REPORT, 128, 123, "page.png")
        self.assertEqual(count, 1)
        self.assertIn("vt 0.00195312 0.99804688", obj)
        self.assertIn("f 3/3 2/2 1/1", obj)
        self.assertIn("map_Kd page.png", mtl)

    def test_unmatched_page_has_no_faces(self):
        obj, _, count = export_textured(REPORT, 128, 999, "page.png")
        self.assertEqual(count, 0)
        self.assertNotIn("\nf ", obj)

    def test_rejects_bad_indices(self):
        bad = {"format": REPORT["format"], "objects":[
            {"index":0,"vertices":[[0,0,0]],"texturedFaces":[
                {"tpage":128,"clut":123,"indices":[0,1,2],"uvRaw":[[0,0],[1,1],[2,2]]}]}]}
        with self.assertRaises(ValueError):
            export_textured(bad, 128, 123, "page.png")

if __name__ == "__main__":
    unittest.main()
