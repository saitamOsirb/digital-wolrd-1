"""Inspect DW1 map offset tables without extracting protected game assets.

The decompiled loadMap() treats GENERAL_BUFFER_PTR as int32 offsets.
This tool validates and prints little-endian offsets from a user-supplied
already isolated map data file, never from an ISO.
"""
import argparse
import json
import struct
from pathlib import Path

def inspect_offsets(data: bytes, count: int) -> dict:
    if count < 1 or count > 256:
        raise ValueError("count must be 1..256")
    if len(data) < 4 * count:
        raise ValueError("short offset table")
    offsets = list(struct.unpack_from("<" + "I" * count, data))
    if any(offset >= len(data) or offset < 4 * count for offset in offsets):
        raise ValueError("offset outside payload or inside table")
    if any(a > b for a, b in zip(offsets, offsets[1:])):
        raise ValueError("descending offsets")
    return {"fileSize": len(data), "offsetCount": count, "offsets": offsets,
            "segments": [{"offset": current, "length": following-current}
                         for current, following in zip(offsets, offsets[1:] + [len(data)])]}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inspect_offsets(args.input.read_bytes(), args.count)
    value = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(value + "\n", encoding="utf-8")
    else:
        print(value)

if __name__ == "__main__":
    main()
