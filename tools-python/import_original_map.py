"""Build a real map PNG directly from a local Digimon World US BIN image.

Example:
python tools-python/import_original_map.py "Digimon World (USA).bin" --map TWNA01
"""
import argparse
import json
from pathlib import Path
from psx_iso import extract_iso_file
from render_tfs_map import decode_tfs_map
from convert_tim import encode_png

KNOWN_MAPS = {
    "TWNA01": "MAP/MAP14/TWNA01.TFS",
    "TWNA02": "MAP/MAP12/TWNA02.TFS",
    "TWNB01": "MAP/MAP13/TWNB01.TFS",
}

def build_from_disc(disc: Path, scene_id: str, destination: Path, palette: int = 0):
    name = scene_id.upper()
    if name not in KNOWN_MAPS:
        raise ValueError("Map not configured: " + name)
    data = extract_iso_file(disc, KNOWN_MAPS[name])
    width, height, pixels = decode_tfs_map(data, palette)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(encode_png(width, height, pixels))
    metadata = {"schemaVersion": 1, "source": "local-extraction", "mapId": name,
                "texture": destination.name, "widthPixels": width,
                "heightPixels": height, "paletteIndex": palette,
                "note": "Map background only; no accurate camera, player, overlays or warps"}
    destination.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc", type=Path, help="Extracted local USA BIN, not 7z")
    parser.add_argument("--map", choices=sorted(KNOWN_MAPS), default="TWNA01")
    parser.add_argument("--palette", type=int, default=0)
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/demo/map.png"))
    args = parser.parse_args()
    result = build_from_disc(args.disc, args.map, args.output, args.palette)
    print(f"Original {result['mapId']} rendered at {result['widthPixels']}x{result['heightPixels']}: {args.output}")

if __name__ == "__main__":
    main()
