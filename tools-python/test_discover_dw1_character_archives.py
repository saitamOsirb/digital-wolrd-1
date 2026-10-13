import unittest
from pathlib import Path
from unittest.mock import patch
from discover_dw1_character_archives import find_character_archives, inventory

FIXTURE = [
    {"path": "CHDAT/TMD0/ABC.TMD", "size": 120},
    {"path": "CHDAT/MMD0/XYZ.MMD", "size": 200},
    {"path": "CHDAT/MTN0/AAA.MTN", "size": 30},
    {"path": "MAP/MAP14/TWNA01.TFS", "size": 500},
    {"path": "CHDAT/EXTRA/OTHER", "size": 10},
]

class ArchiveDiscoveryTests(unittest.TestCase):
    def test_filters_only_actual_archive_directories(self):
        result = find_character_archives(FIXTURE)
        self.assertEqual(len(result), 3)
        self.assertEqual({x["kind"] for x in result}, {"TMD0", "MMD0", "MTN0"})

    @patch("discover_dw1_character_archives.list_disc_files", return_value=FIXTURE)
    def test_metadata_only_does_not_extract(self, _):
        with patch("discover_dw1_character_archives.extract_iso_file") as extract:
            output = inventory(Path("fake.bin"))
        extract.assert_not_called()
        self.assertEqual(output["counts"], {"TMD0": 1, "MMD0": 1, "MTN0": 1})

    @patch("discover_dw1_character_archives.scan_tmd", return_value=[
        {"byteOffset": 48, "objects": 3}])
    @patch("discover_dw1_character_archives.extract_iso_file", return_value=b"test")
    @patch("discover_dw1_character_archives.list_disc_files", return_value=FIXTURE)
    def test_optional_scan_never_scans_animation_data(self, _files, extract, scan):
        output = inventory(Path("fake.bin"), scan=True)
        self.assertEqual(scan.call_count, 2)
        self.assertEqual(extract.call_count, 2)
        self.assertEqual(sum(len(row["tmdCandidates"]) for row in output["archives"]), 2)

if __name__ == "__main__":
    unittest.main()
