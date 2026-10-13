"""Experimental PS1 TMD unlit flat-polygon mesh export.

Only untextured no-lighting packets with (mode 0x20/0x28, flags bit 0)
are interpreted. Other modes are skipped with diagnostics. Faces are not
claimed to reproduce the game's complete skinned character models.
"""
import argparse
import json
import struct
from pathlib import Path
from export_tmd_vertices import read_vertices

def decode_unlit_mesh(data: bytes, offset: int = 0) -> dict:
    result = read_vertices(data, offset)
    table_base = offset + 12
    table_end = table_base + result["objectCount"] * 28
    skipped = {}
    triangles = 0
    for obj in result["objects"]:
        index = obj["index"]
        record = struct.unpack_from("<7I", data, table_base + index * 28)
        primitive_pointer, count = record[4:6]
        cursor = table_base + primitive_pointer
        if count > 100000 or (count and (cursor < table_end or cursor >= len(data))):
            raise ValueError("Invalid primitive pointer or count")
        faces = []
        for _ in range(count):
            if cursor + 4 > len(data):
                raise ValueError("Truncated TMD primitive header")
            olen, ilen, flags, mode = struct.unpack_from("<BBBB", data, cursor)
            end = cursor + 4 + ilen * 4
            if ilen == 0 or end > len(data):
                raise ValueError("Invalid primitive packet length")
            key = f"mode={mode:02x},flags={flags:02x}"
            # In a no-lighting untextured flat polygon, the packet contains
            # one RGB/code word followed by packed uint16 vertex indices.
            if mode in (0x20, 0x28) and flags & 1 and not (flags & ~1):
                vertices_per_face = 3 if mode == 0x20 else 4
                expected_words = 3
                if ilen != expected_words:
                    skipped[key + "-unexpected-length"] = skipped.get(key + "-unexpected-length", 0) + 1
                else:
                    r, g, b, code = struct.unpack_from("<BBBB", data, cursor + 4)
                    indices = struct.unpack_from("<" + "H" * vertices_per_face, data, cursor + 8)
                    if any(i >= len(obj["vertices"]) for i in indices):
                        raise ValueError("TMD polygon references missing vertex")
                    faces.append({"indices": list(indices), "rgb": [r, g, b]})
                    triangles += vertices_per_face - 2
            else:
                skipped[key] = skipped.get(key, 0) + 1
            cursor = end
        obj["faces"] = faces
        obj["primitiveCount"] = count
    result["format"] = "psx-tmd-experimental-unlit-mesh"
    result["triangleCount"] = triangles
    result["skippedModes"] = skipped
    result["warning"] = "Experimental flat untextured faces only; no UV, normals, bones, skinning or animations"
    return result

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--offset", type=lambda value: int(value, 0), default=0)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    result = decode_unlit_mesh(args.input.read_bytes(), args.offset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Objects: {result['objectCount']} triangles: {result['triangleCount']} skipped: {sum(result['skippedModes'].values())}")

if __name__ == "__main__":
    main()
