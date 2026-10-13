"""Inspect possible PlayStation TMD objects in an explicitly extracted binary.

A TMD starts with uint32 magic 0x41, flags, and object count. Candidate
signatures are not sufficient to identify the tamer model. This tool never
exports geometry or proprietary textures.
"""
import argparse
import json
import struct
from pathlib import Path

TMD_MAGIC = 0x41
MAX_OBJECTS = 128

def scan_tmd(data: bytes, max_hits: int = 200) -> list[dict]:
    if max_hits < 1:
        raise ValueError("max_hits must be positive")
    hits = []
    for offset in range(0, len(data) - 12, 4):
        if data[offset:offset + 4] != b"\x41\x00\x00\x00":
            continue
        _, flags, objects = struct.unpack_from("<III", data, offset)
        if flags & ~1 or not 1 <= objects <= MAX_OBJECTS:
            continue
        table_end = offset + 12 + objects * 28
        if table_end > len(data):
            continue
        headers = []
        plausible = True
        for index in range(objects):
            vertex_ptr, vertex_count, normal_ptr, normal_count, primitive_ptr, primitive_count, scale = struct.unpack_from(
                "<7I", data, offset + 12 + index * 28)
            if vertex_count > 65536 or normal_count > 65536 or primitive_count > 65536 or scale > 32:
                plausible = False
                break
            if vertex_count == 0 or primitive_count == 0:
                plausible = False
                break
            headers.append({"vertices": vertex_count, "normals": normal_count, "primitives": primitive_count,
                            "vertexPointer": vertex_ptr, "normalPointer": normal_ptr,
                            "primitivePointer": primitive_ptr, "scale": scale})
        if plausible:
            hits.append({"byteOffset": offset, "flags": flags, "objects": objects,
                         "headers": headers, "status": "candidate-unverified"})
            if len(hits) >= max_hits:
                break
    return hits

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Binary extracted locally from user-owned disc")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    hits = scan_tmd(args.input.read_bytes())
    report = {"file": args.input.name, "candidates": hits, "candidateCount": len(hits)}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()
