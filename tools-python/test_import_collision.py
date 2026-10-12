import unittest
from import_collision import collision_rectangles

class CollisionTests(unittest.TestCase):
    def test_empty_grid(self):
        self.assertEqual(collision_rectangles(bytes(10000)), [])

    def test_high_bit_only(self):
        grid = bytearray(10000)
        grid[0] = 0x7f
        grid[1] = 0x80
        grid[2] = 0xff
        self.assertEqual(collision_rectangles(grid), [
            {"x": 1, "y": 0, "width": 2, "height": 1}
        ])

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            collision_rectangles(bytes(10))

if __name__ == "__main__":
    unittest.main()
