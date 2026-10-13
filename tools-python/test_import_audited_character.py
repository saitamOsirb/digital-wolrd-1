import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from import_audited_character import select_candidate, build_from_disc

AUDIT = {"format": "dw1-character-archive-audit", "archives": [{
    "path": "CHDAT/MMD0/EXAMPLE.BIN", "kind": "MMD0",
    "models": [{"offset": 32, "status": "partial-ft3-ft4-decode", "texturedFaces": 2},
               {"offset": 128, "status": "vertex-only", "texturedFaces": 0}]
}]}

class AuditedImportTests(unittest.TestCase):
    def test_requires_supported_explicit_candidate(self):
        self.assertEqual(select_candidate(AUDIT, "CHDAT/MMD0/EXAMPLE.BIN", 32)["offset"], 32)
        for archive, offset in (("CHDAT/MMD0/EXAMPLE.BIN", 128),
                                ("CHDAT/MMD0/MISSING.BIN", 32)):
            with self.assertRaises(ValueError):
                select_candidate(AUDIT, archive, offset)

    def test_rejects_missing_texture_paths_before_extraction(self):
        with self.assertRaises(ValueError):
            build_from_disc(Path("fake.bin"), AUDIT, "CHDAT/MMD0/EXAMPLE.BIN",
                            32, [], Path("unused"))

    @patch("import_audited_character.build_preview", return_value={
        "objects": [{"faces": [{}, {}]}]})
    @patch("import_audited_character.extract_iso_file", return_value=b"sample")
    def test_generates_local_provenance_without_asserting_identity(self, extract, _preview):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            build_from_disc(Path("fake.bin"), AUDIT, "CHDAT/MMD0/EXAMPLE.BIN",
                            32, ["TEXTURE/A.TIM"], output)
            provenance = (output / "provenance.json").read_text(encoding="utf-8")
            self.assertIn('"verifiedTamer": false', provenance)
            self.assertIn('"verifiedAnimation": false', provenance)
            self.assertEqual(extract.call_count, 2)

if __name__ == "__main__":
    unittest.main()
