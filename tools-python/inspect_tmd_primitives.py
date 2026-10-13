"""Read conservative untextured triangle/quadrilateral TMD primitives.

Supports only known PS1 polygon packet modes: 0x20/0x28 (flat)
and 0x30/0x38 (Gouraud), without textures. Unsupported primitives are
reported and skipped; geometry must not be fabricated.
"""
import struct
from export_tmd_vertices import read_vertices

SUPPORTED = {0x20: (3, 4), 0x28: (4, 5), 0x30: (3, 6), 0x38: (4, 8)}

def decode_faces(data: bytes, offset: int = 0) -> dict:
    result = read_vertices(data, offset)
    base = offset + 12
    warnings = []
    for obj in result["objects"]:
        index = obj["index"]
        header = struct.unpack_from("<7I", data, base + index * 28)
        primitive_offset, primitive_count = header[4], header[5]
        cursor = base + primitive_offset
        faces = []
        if cursor < base + result["objectCount"] * 28 or cursor >= len(data):
            raise ValueError("Invalid primitive pointer")
        if primitive_count > 100000:
            raise ValueError("Too many primitives")
        for primitive_index in range(primitive_count):
            if cursor + 4 > len(data):
                raise ValueError("Truncated primitive header")
            olen, ilen, flags, mode = struct.unpack_from("<BBBB", data, cursor)
            # ilen is the number of 32-bit words after primitive header.
            packet_end = cursor + 4 + ilen * 4
            if ilen == 0 or packet_end > len(data):
                raise ValueError("Invalid primitive packet length")
            if mode in SUPPORTED and (mode & 4) == 0 and flags == 0:
                vertices_required, words = SUPPORTED[mode]
                if ilen >= words:
                    # Untextured polygons: rgb+code word, optional per-vertex
                    # colors/normals; the final vertex index words are packet-specific.
                    # Remain conservative until indices are verified from samples.
                    warnings.append(f"Object {index} primitive {primitive_index}: known mode {mode:#x}, indices not yet verified")
                else:
                    warnings.append(f"Object {index} primitive {primitive_index}: short packet")
            else:
                warnings.append(f"Object {index} primitive {primitive_index}: unsupported mode {mode:#x}")
            cursor = packet_end
        obj["faces"] = faces
        obj["primitiveCount"] = primitive_count
    result["format"] = "psx-tmd-primitive-survey"
    result["warnings"] = warnings
    result["warning"] = "Packet survey only: no faces emitted without verified vertex-index layouts"
    return result

def main() -> None:
    import argparse
    import json
    from pathlib import Path
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--offset", type=lambda x: int(x, 0), default=0)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    report = decode_faces(args.input.read_bytes(), args.offset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, separators=(",", ":")) + "\n", encoding="utf-8")
    print("Scanned", sum(o["primitiveCount"] for o in report["objects"]), "primitives")
    print("Warnings:", len(report["warnings"]))

if __name__ == "__main__":
    main()
