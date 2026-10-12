"""Decode camera and map metadata from a previously isolated DW1 MAP setup segment.

Layout follows dw_decomp/src/main/map.c loadMapSetup(int32_t *data):
6 viewpoint words, 18 light words, 3 reserved, projection, 8 region,
width and height followed by tile identifiers.
"""
import struct

WIDTH_WORD = 6 + 18 + 3 + 1 + 8
MIN_WORDS = WIDTH_WORD + 2

def parse_setup(data: bytes) -> dict:
    if len(data) < MIN_WORDS * 4:
        raise ValueError("Map setup header truncated")
    words = struct.unpack_from("<" + "i" * MIN_WORDS, data)
    width, height = words[WIDTH_WORD:WIDTH_WORD + 2]
    if not (1 <= width <= 128 and 1 <= height <= 128 and width * height <= 4096):
        raise ValueError("Invalid map dimensions")
    tile_end = (MIN_WORDS + width * height) * 4
    if len(data) < tile_end:
        raise ValueError("Map setup tile list truncated")
    tiles = struct.unpack_from("<" + "i" * (width * height), data, MIN_WORDS * 4)
    viewpoint = [value * 2 for value in words[:6]]
    return {
        "schemaVersion": 1,
        "camera": {"position": viewpoint[:3], "target": viewpoint[3:6],
                   "projectionDistance": words[27]},
        "widthTiles": width, "heightTiles": height,
        "tileIds": list(tiles),
        "nonemptyTiles": sum(value != -1 for value in tiles),
        "source": "local-extraction",
        "warning": "PS1 camera parameters only; no projection/calibration in Godot yet",
    }
