"""Extract the MAP setup segment using the first little-endian offset in a DW1 MAP file."""
import argparse
import json
import struct
from pathlib import Path
from psx_iso import extract_iso_file
from map_setup import parse_setup

def read_setup_file(data: bytes) -> dict:
    if len(data) < 8:
        raise ValueError("MAP file too short")
    start = struct.unpack_from("<I", data)[0]
    if start < 4 or start >= len(data):
        raise ValueError("Invalid MAP setup offset")
    return parse_setup(data[start:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("disc", type=Path)
    parser.add_argument("--map-path", default="MAP/MAP14/TWNA01.MAP")
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/demo/map_setup.json"))
    args = parser.parse_args()
    data = extract_iso_file(args.disc, args.map_path)
    doc = read_setup_file(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print("Camera:", doc["camera"], "tiles:", doc["widthTiles"], "x", doc["heightTiles"])

if __name__ == "__main__":
    main()
