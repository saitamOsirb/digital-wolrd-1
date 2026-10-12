"""Composite 128x128 RGBA tiles into a PNG scene; stdlib only.

A deterministic procedural fixture demonstrates the complete PNG->Godot map
pipeline. Separately provided RGBA files may be used to validate placement.
This does not decode DW1 TFS tile payloads.
"""
import argparse
import json
import math
from pathlib import Path
from convert_tim import encode_png

TILE = 128
MAX_TILES = 256

def demo_tile(col: int, row: int) -> bytes:
    result = bytearray(TILE * TILE * 4)
    for y in range(TILE):
        for x in range(TILE):
            px, py = col * TILE + x, row * TILE + y
            stream = 18 * math.sin(px / 39) + 13 * math.cos(py / 33)
            grass = (59, 119 + int(stream / 5), 66, 255)
            road = abs(px - 256 + 29 * math.sin(py / 73)) < 47
            pond = (px - 135) ** 2 / 110 ** 2 + (py - 135) ** 2 / 73 ** 2 < 1
            if road:
                color = (165 + int(stream / 7), 141, 94, 255)
            elif pond:
                color = (45, 116 + int(stream / 4), 154, 255)
            else:
                color = grass
            if (px * 17 + py * 31) % 97 < 3 and not road and not pond:
                color = (108, 152, 73, 255)
            offset = (y * TILE + x) * 4
            result[offset:offset + 4] = bytes(color)
    return bytes(result)

def composite(width: int, height: int, pixels: dict[tuple[int, int], bytes]) -> bytes:
    if width < 1 or height < 1 or width * height > MAX_TILES:
        raise ValueError("Invalid tile grid")
    output_width = width * TILE
    image = bytearray(output_width * height * TILE * 4)
    for (col, row), tile in pixels.items():
        if not (0 <= col < width and 0 <= row < height) or len(tile) != TILE * TILE * 4:
            raise ValueError("Invalid tile coordinate or RGBA length")
        for y in range(TILE):
            destination = ((row * TILE + y) * output_width + col * TILE) * 4
            source = y * TILE * 4
            image[destination:destination + TILE * 4] = tile[source:source + TILE * 4]
    return bytes(image)

def create_scene(output: Path, width=4, height=4) -> dict:
    tiles = {(x, y): demo_tile(x, y) for y in range(height) for x in range(width)}
    rgba = composite(width, height, tiles)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encode_png(width * TILE, height * TILE, rgba))
    report = {"schemaVersion": 1, "source": "synthetic", "widthTiles": width,
              "heightTiles": height, "tilePixels": TILE,
              "image": output.name, "widthPixels": width * TILE,
              "heightPixels": height * TILE}
    output.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/demo/map.png"))
    args = parser.parse_args()
    result = create_scene(args.output)
    print(f"Generated synthetic map {result['widthPixels']}x{result['heightPixels']}: {args.output}")

if __name__ == "__main__":
    main()
