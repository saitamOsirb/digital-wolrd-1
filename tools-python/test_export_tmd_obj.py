import unittest
from export_tmd_obj import convert

DOC = {"format": "psx-tmd-experimental-unlit-mesh", "objects": [
    {"index": 0, "vertices": [[0,0,0],[100,0,0],[0,100,0],[100,100,0]],
     "faces": [{"indices": [0,1,2], "rgb": [255,128,0]},
               {"indices": [0,1,3,2], "rgb": [255,128,0]}]}
]}

class OBJExportTests(unittest.TestCase):
    def test_exports_vertices_faces_and_material(self):
        obj, mtl = convert(DOC, mtl_name="hero.mtl")
        self.assertIn("mtllib hero.mtl", obj)
        self.assertIn("v 0.20000000 -0.00000000 0.00000000", obj)
        self.assertIn("f 3 2 1", obj)
        self.assertIn("f 3 4 2 1", obj)
        self.assertEqual(mtl.count("newmtl"), 1)
        self.assertIn("Kd 1.000000 0.501961 0.000000", mtl)
    def test_rejects_invalid_face_indices(self):
        bad = {**DOC, "objects": [{**DOC["objects"][0], "faces": [{"indices":[0,1,99],"rgb":[1,2,3]}]}]}
        with self.assertRaises(ValueError):
            convert(bad)
    def test_rejects_unsupported_format(self):
        with self.assertRaises(ValueError):
            convert({"format":"psx-tmd-vertex-cloud"})
if __name__ == "__main__":
    unittest.main()
