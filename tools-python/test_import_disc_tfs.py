import unittest
from pathlib import Path
from unittest.mock import patch
from import_disc_tfs import convert_disc_tfs

class DiscTFSTests(unittest.TestCase):
    def test_blocks_non_tfs_path(self):
        with self.assertRaises(ValueError):
            convert_disc_tfs(Path("missing.bin"), "MAP/MAP14/TWNA01.MAP", Path("x.png"))
    def test_blocks_directory_traversal(self):
        with self.assertRaises(ValueError):
            convert_disc_tfs(Path("missing.bin"), "../TWNA01.TFS", Path("x.png"))
    def test_rejects_unavailable_disc(self):
        with self.assertRaises(FileNotFoundError):
            convert_disc_tfs(Path("missing.bin"), "MAP/MAP14/TWNA01.TFS", Path("x.png"))
