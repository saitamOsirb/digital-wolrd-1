import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from import_all_maps import batch_import

class BatchImportTests(unittest.TestCase):
    def test_catalog_contains_successes_and_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            def fake_convert(disc, source, target, palette):
                if source.endswith("FAIL.TFS"):
                    raise ValueError("invalid fixture")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"PNG")
                return {"mapId": "TEST", "widthPixels": 128, "heightPixels": 256}
            with patch("import_all_maps.list_disc_files", return_value=[
                {"path": "MAP/MAP01/OK.TFS", "size": 1},
                {"path": "MAP/MAP02/FAIL.TFS", "size": 1}
            ]), patch("import_all_maps.convert_disc_tfs", side_effect=fake_convert):
                report = batch_import(folder / "disc.bin", folder / "out")
            self.assertEqual(len(report["maps"]), 1)
            self.assertEqual(len(report["failed"]), 1)
            self.assertEqual(report["maps"][0]["image"], "MAP/MAP01/OK.png")
            self.assertTrue((folder / "out/catalog.json").exists())

    def test_limits_are_validated(self):
        with self.assertRaises(ValueError):
            batch_import(Path("x"), Path("y"), -1)
