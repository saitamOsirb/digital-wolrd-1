"""Inspect the DW1 TFS image-data structure documented in dw_decomp map.c.

Only accepts an already-isolated file provided locally by the user.
This is a structural inspector, not an extractor or full decoder.
"""
import argparse
import json
import struct
from pathlib import Path

CLUT_BYTES = 256
TILE_BYTES = 4 + 4096 * 4  # one skipped uint32 plus 16 KiB of source image words

def inspect_tfs(data: bytes, tile_count: int = 0) -> dict:
    if len(data) < 8:
        raise ValueError("TFS too short for header")
    if tile_count < 0 or tile_count > 4096:
        raise ValueError("Invalid tile count")
    unknown_header, clut_count = struct.unpack_from("<II", data)
    if clut_count > 1024:
        raise ValueError("Implausible CLUT count")
    palette_end = 8 + clut_count * CLUT_BYTES
    if palette_end > len(data):
        raise ValueError("Truncated CLUT table")
    # map.c: data++; numCluts=*data++; each CLUT advances 128 u_long
    # (512 bytes). Do not confuse LoadClut's upload width with table stride.
    palette_stride = 128 * 4
    palette_end = 8 + clut_count * palette_stride
    if palette_end > len(data):
        raise ValueError("Truncated CLUT table")
    tile_end = palette_end + tile_count * TILE_BYTES
    if tile_end > len(data):
        raise ValueError("Truncated requested tile data")
    tiles = [{"index": i, "headerOffset": palette_end + i * TILE_BYTES,
              "payloadOffset": palette_end + i * TILE_BYTES + 4,
              "payloadBytes": TILE_BYTES - 4} for i in range(tile_count)]
    return {"headerWord": unknown_header, "clutCount": clut_count,
            "clutStrideBytes": palette_stride, "clutOffsets": [
                8 + i * palette_stride for i in range(clut_count)],
            "tileCountRequested": tile_count, "tileRecords": tiles,
            "remainderStart": tile_end, "remainderBytes": len(data) - tile_end,
            "status": "candidate-layout-only"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--tiles", type=int, default=0, help="Number of nonempty tiles (externally established)")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inspect_tfs(args.input.read_bytes(), args.tiles)
    document = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(document, encoding="utf-8")
    else:
        print(document)

if __name__ == "__main__":
    main()
