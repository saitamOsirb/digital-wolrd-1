import json
import struct
import tempfile
import unittest
from pathlib import Path
from build_godot_character_preview import build_preview

def sample_model():
    header = struct.pack("<III", 0x41, 0, 1)
    record = struct.pack("<7I", 28, 3, 0, 0, 52, 1, 0)
    vertices = b"".join(struct.pack("<hhhh", *v, 0) for v in ((0,0,0),(100,0,0),(0,100,0)))
    payload = bytes((128,128,128,0))
    payload += struct.pack("<BBHBBHBBH",0,0,0, 1,0,0, 0,1,0)
    payload += struct.pack("<3H",0,1,2) + b"\0\0"
    packet = bytes((0,len(payload)//4,1,0x24)) + payload
    return header + record + vertices + packet

def sample_tim():
    return struct.pack("<II",0x10,2)+struct.pack("<IHHHHH",14,0,0,1,1,0x7fff)

class GodotCharacterPipelineTests(unittest.TestCase):
    def test_builds_manifest_and_texture(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/"export"
            manifest = build_preview(sample_model(), [sample_tim()], target)
            self.assertEqual(manifest["format"],"dw1-textured-preview")
            self.assertEqual(len(manifest["objects"][0]["faces"]),1)
            self.assertTrue((target/"0000_0000.png").read_bytes().startswith(b"\x89PNG"))
            self.assertEqual(json.loads((target/"model.json").read_text())["schemaVersion"],1)

    def test_no_faces_prevents_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/"export"
            data = bytearray(sample_model())
            data[67] = 0x20
            with self.assertRaises(ValueError):
                build_preview(bytes(data), [sample_tim()], target)
            self.assertFalse(target.exists())

if __name__ == "__main__":
    unittest.main()
