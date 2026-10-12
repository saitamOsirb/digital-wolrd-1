import struct
import unittest
from inspect_map_tfs import build_report

class MapTfsTests(unittest.TestCase):
    def test_sparse_indices_match_payload_sequence(self):
        setup = struct.pack("<ii4i", 2, 2, -1, 10, -1, 20)
        tfs = struct.pack("<II", 0, 0) + (struct.pack("<I", 123) + bytes(16384)) * 2
        report = build_report(setup, 0, tfs)
        self.assertEqual(report["nonemptyCount"], 2)
        self.assertEqual(report["tiles"][0]["tileIndex"], 1)
        self.assertEqual(report["tiles"][1]["tileIndex"], 3)
        self.assertEqual(report["tiles"][1]["candidatePayloadOffset"], 12 + 16388)

    def test_truncation_is_error(self):
        setup = struct.pack("<ii1i", 1, 1, 1)
        with self.assertRaises(ValueError):
            build_report(setup, 0, struct.pack("<II", 0, 0))

if __name__ == "__main__":
    unittest.main()
