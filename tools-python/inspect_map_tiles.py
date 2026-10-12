"""Inspect DW1 map setup tile layout using an explicit verified offset.

dw_decomp/src/main/map.c loadMapSetup uses an int32_t*:
MAP_WIDTH[0]=*data++; MAP_HEIGHT[0]=*data++; MAP_TILES[i]=*data++.
The supplied offset MUST point to width after camera/lights/settings.
"""
import argparse
import json
import struct
from pathlib import Path

def read_tile_layout(data: bytes, offset: int) -> dict:
    if not isinstance(offset, int) or offset < 0 or offset % 4 or offset + 8 > len(data):
        raise ValueError("Invalid width offset")
    width, height = struct.unpack_from("<ii", data, offset)
    if not 1 <= width <= 128 or not 1 <= height <= 128 or width * height > 4096:
        raise ValueError("Implausible map dimensions")
    end = offset + 8 + 4 * width * height
    if end > len(data):
        raise ValueError("Truncated map tile list")
    ids = struct.unpack_from("<" + "i" * (width * height), data, offset + 8)
    if any(value < -1 or value > 65535 for value in ids):
        raise ValueError("Unexpected tile identifier")
    present = [i for i, value in enumerate(ids) if value != -1]
    return {"schemaVersion": 1, "width": width, "height": height,
            "tileIds": list(ids), "nonemptyIndices": present,
            "nonemptyCount": len(present), "widthOffset": offset,
            "listEnd": end}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Previously isolated map setup segment")
    parser.add_argument("--width-offset", type=int, required=True,
                        help="Byte offset of width int32 in map setup, determined independently")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = read_tile_layout(args.input.read_bytes(), args.width_offset)
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()
