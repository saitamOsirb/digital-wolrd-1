import struct
import tempfile
import unittest
from pathlib import Path
from build_tmd_materials import build

def test_model():
    header = struct.pack("<III", 0x41, 0, 1)
    object_header = struct.pack("<7I", 28, 3, 0, 0, 52, 1, 0)
    vertices = b"".join(struct.pack("<hhhh", x, y, z, 0) for x, y, z in
                        [(0,0,0), (100,0,0), (0,100,0)])
    payload = bytes([128,128,128,0])
    for i in range(3):
        payload += struct.pack("<BBH", i, i, 0)
    payload += struct.pack("<3H", 0, 1, 2) + bytes(2)
    packet = struct.pack("<BBBB", 0, len(payload)//4, 1, 0x24) + payload
    return header + object_header + vertices + packet

def tim():
    pixels = struct.pack("<IHHHHH", 14, 0, 0, 1, 1, 0x7fff)
    return struct.pack("<II", 0x10, 2) + pixels

class MaterialBuildTests(unittest.TestCase):
    def test_exports_matching_groups_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "materials"
            report = build(test_model(), [tim()], out)
            self.assertEqual(report["exportedFaces"], 1)
            self.assertEqual(len(report["textureGroups"]), 1)
            group = report["textureGroups"][0]
            for key in ("obj", "mtl", "png"):
                self.assertTrue((out / group[key]).exists())
            self.assertIn("map_Kd page_0000_0000.png", (out / group["mtl"]).read_text())
            self.assertTrue((out / "manifest.json").exists())

    def test_no_supported_faces_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "materials"
            data = test_model()
            # Override primitive mode FT3 to unsupported value.
            data = data[:67] + bytes([0x20]) + data[68:]
            with self.assertRaises(ValueError):
                build(data, [tim()], out)
            self.assertFalse(out.exists())

if __name__ == "__main__":
    unittest.main()
