import unittest
from pathlib import Path
from unittest.mock import patch
from audit_dw1_character_pipeline import audit

FILES = [
    {"path": "CHDAT/TMD0/EXAMPLE.BIN", "size": 1024},
    {"path": "CHDAT/MTN0/MOTION.BIN", "size": 128},
]

class CharacterAuditTests(unittest.TestCase):
    @patch("audit_dw1_character_pipeline.inspect_uv")
    @patch("audit_dw1_character_pipeline.read_vertices")
    @patch("audit_dw1_character_pipeline.scan_tmd")
    @patch("audit_dw1_character_pipeline.extract_iso_file", return_value=b"fake")
    @patch("audit_dw1_character_pipeline.list_disc_files", return_value=FILES)
    def test_reports_partial_decode_and_does_not_extract_motion(self, _files, extract, scanner, vertex, uv):
        scanner.return_value = [{"byteOffset": 32, "objects": 1}]
        vertex.return_value = {"vertexCount": 4}
        uv.return_value = {"texturedFaceCount": 2, "skippedPackets": {"a": 3}}
        report = audit(Path("test.bin"))
        self.assertEqual(report["summary"]["archives"], 2)
        self.assertEqual(report["summary"]["ft3ft4Faces"], 2)
        self.assertEqual(report["archives"][0]["models"][0]["status"], "partial-ft3-ft4-decode")
        self.assertEqual(report["archives"][1]["status"], "animation-or-oversize-not-scanned")
        self.assertEqual(extract.call_count, 1)

    @patch("audit_dw1_character_pipeline.list_disc_files", return_value=FILES)
    def test_refuses_excessive_file_counts(self, _files):
        with self.assertRaises(ValueError):
            audit(Path("test.bin"), max_files=1)

    @patch("audit_dw1_character_pipeline.extract_iso_file", side_effect=ValueError("bad"))
    @patch("audit_dw1_character_pipeline.list_disc_files", return_value=FILES)
    def test_records_read_errors_without_aborting(self, _files, _extract):
        report = audit(Path("test.bin"))
        self.assertEqual(report["archives"][0]["status"], "file-read-error")
        self.assertEqual(report["summary"]["tmdCandidates"], 0)

if __name__ == "__main__":
    unittest.main()
