import tempfile
import unittest
from pathlib import Path
from render_map_demo import TILE, composite, create_scene, demo_tile

class RenderMapDemoTests(unittest.TestCase):
    def test_tile_bytes(self):
        self.assertEqual(len(demo_tile(0, 0)), TILE * TILE * 4)

    def test_tiles_are_placed_in_row_major_order(self):
        red = bytes([255, 0, 0, 255]) * (TILE * TILE)
        blue = bytes([0, 0, 255, 255]) * (TILE * TILE)
        data = composite(2, 1, {(0, 0): red, (1, 0): blue})
        self.assertEqual(data[:4], red[:4])
        self.assertEqual(data[TILE * 4:TILE * 4 + 4], blue[:4])

    def test_reject_bad_tile(self):
        with self.assertRaises(ValueError):
            composite(1, 1, {(0, 0): b"invalid"})

    def test_png_and_manifest(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "map.png"
            manifest = create_scene(path, 2, 2)
            self.assertEqual(manifest["widthPixels"], 256)
            self.assertTrue(path.read_bytes().startswith(bytes([137, 80, 78, 71])))
            self.assertTrue(path.with_suffix(".json").exists())

if __name__ == "__main__":
    unittest.main()
