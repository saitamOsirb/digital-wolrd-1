import struct
import unittest
from inspect_tmd_primitives import decode_faces

class PrimitiveSurveyTests(unittest.TestCase):
    def test_known_packet_is_reported_not_invented(self):
        header = struct.pack("<III", 0x41, 0, 1)
        obj = struct.pack("<7I", 28, 1, 0, 0, 36, 1, 0)
        vertex = struct.pack("<hhhh", 1, 2, 3, 0)
        packet = struct.pack("<BBBB", 4, 4, 0, 0x20) + bytes(16)
        report = decode_faces(header + obj + vertex + packet)
        self.assertEqual(report["objects"][0]["faces"], [])
        self.assertEqual(report["objects"][0]["primitiveCount"], 1)
        self.assertEqual(len(report["warnings"]), 1)

    def test_malformed_packet_rejected(self):
        header = struct.pack("<III", 0x41, 0, 1)
        obj = struct.pack("<7I", 28, 1, 0, 0, 36, 1, 0)
        vertex = struct.pack("<hhhh", 1, 2, 3, 0)
        packet = struct.pack("<BBBB", 4, 20, 0, 0x20)
        with self.assertRaises(ValueError):
            decode_faces(header + obj + vertex + packet)
if __name__ == "__main__":
    unittest.main()
