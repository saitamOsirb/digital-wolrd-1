import unittest
from pathlib import Path
from unittest.mock import patch
from inspect_character_assets import model_inventory

class CharacterInventoryTests(unittest.TestCase):
    def test_classifies_candidates_without_export(self):
        records = [{"path": "MAP/SCENE.TFS", "size": 4},
                   {"path": "BATTLE/MODEL1.BIN", "size": 100},
                   {"path": "ANIM/PLAYER.DAT", "size": 20},
                   {"path": "DATA/FOO", "size": 12}]
        with patch("inspect_character_assets.list_disc_files", return_value=records):
            result = model_inventory(Path("dummy.bin"))
        self.assertEqual(result["totalFiles"], 4)
        self.assertEqual(len(result["candidateFiles"]), 2)
        self.assertEqual(result["extensionCounts"][".BIN"], 1)
        self.assertEqual(result["status"], "filename-candidates-not-verified-models")

if __name__ == "__main__":
    unittest.main()
