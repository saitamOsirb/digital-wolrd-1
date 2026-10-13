"""Export PS1 TMD vertex point clouds for structural verification in Godot.

Supports standard offset-based TMD (flags=0). Object pointers are relative
to the object table base (TMD header + 12). This is a vertex inspector, not
a mesh/rig/animation converter; no faces or materials are inferred.
"""
import argparse
import json
import struct
from pathlib import Path

def read_vertices(blob: bytes, base: int = 0, max_vertices: int = 200000) -> dict:
    if base < 0 or base % 4 or base + 12 > len(blob):
        raise ValueError("Invalid TMD offset")
    magic, flags, count = struct.unpack_from("<III", blob, base)
    if magic != 0x41 or flags != 0 or not 1 <= count <= 128:
        raise ValueError("Only conventional relative-pointer TMD files are supported")
    table_base = base + 12
    if table_base + 28 * count > len(blob):
        raise ValueError("Truncated TMD object table")
    objects = []
    total = 0
    for index in range(count):
        values = struct.unpack_from("<7I", blob, table_base + index * 28)
        vertex_offset, vertex_count, _, _, _, _, scale = values
        total += vertex_count
        if vertex_count > max_vertices or total > max_vertices or scale > 32:
            raise ValueError("Unreasonable vertex count or scale")
        start = table_base + vertex_offset
        end = start + vertex_count * 8
        if start < table_base + count * 28 or end > len(blob):
            raise ValueError("Vertex pointer outside valid geometry buffer")
        vertices = []
        for at in range(start, end, 8):
            x, y, z, padding = struct.unpack_from("<hhhh", blob, at)
            vertices.append([x, y, z])
        objects.append({"index": index, "scaleExponent": scale, "vertices": vertices})
    return {"schemaVersion": 1, "format": "psx-tmd-vertex-cloud",
            "sourceOffset": base, "objectCount": count, "vertexCount": total,
            "objects": objects, "warning": "POINT CLOUD ONLY; no polygons, textures, skeleton or animations"}

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--offset", type=lambda x: int(x, 0), default=0)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    result = read_vertices(args.input.read_bytes(), args.offset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    print("TMD objects:", result["objectCount"], "vertices:", result["vertexCount"])

if __name__ == "__main__":
    main()
