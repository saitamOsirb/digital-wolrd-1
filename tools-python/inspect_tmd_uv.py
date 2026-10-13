"""Survey unlit textured TMD packets (experimental UV parsing).

Supports mode 0x24 (FT3), 0x2c (FT4) with flags==1 only.
Exports raw texture coordinates and CLUT/TPAGE references, NOT textures.
"""
import argparse
import json
import struct
from pathlib import Path
from export_tmd_vertices import read_vertices

MODES = {0x24: 3, 0x2C: 4}

def inspect_uv(data: bytes, offset: int = 0) -> dict:
    report = read_vertices(data, offset)
    table = offset + 12
    table_end = table + report["objectCount"] * 28
    skipped: dict[str, int] = {}
    textured = 0
    for obj in report["objects"]:
        hdr = struct.unpack_from("<7I", data, table + obj["index"] * 28)
        primitive_ptr, primitive_count = hdr[4:6]
        cursor = table + primitive_ptr
        if primitive_count > 100000 or (primitive_count and (cursor < table_end or cursor >= len(data))):
            raise ValueError("Invalid primitive table")
        faces = []
        for _ in range(primitive_count):
            if cursor + 4 > len(data):
                raise ValueError("Truncated packet header")
            _, ilen, flags, mode = struct.unpack_from("<4B", data, cursor)
            end = cursor + 4 + ilen * 4
            if ilen == 0 or end > len(data):
                raise ValueError("Truncated packet body")
            n = MODES.get(mode)
            # RGB/code (1 word) + UV entries (n words) + packed
            # vertex indices (2 words for either triangles or quads).
            if n is not None and flags == 1 and ilen == n + 3:
                r, g, b, _ = struct.unpack_from("<4B", data, cursor + 4)
                coords = []
                clut = 0
                tpage = 0
                for i in range(n):
                    u, v, extra = struct.unpack_from("<BBH", data, cursor + 8 + i * 4)
                    coords.append([u, v])
                    if i == 0:
                        clut = extra
                    elif i == 1:
                        tpage = extra
                indices = struct.unpack_from("<" + "H" * n, data, cursor + 8 + n * 4)
                if any(i >= len(obj["vertices"]) for i in indices):
                    raise ValueError("Textured primitive vertex out of range")
                faces.append({"indices": list(indices), "uvRaw": coords,
                              "clut": clut, "tpage": tpage, "rgb": [r, g, b]})
                textured += 1
            else:
                key = f"{mode:02x}:{flags:02x}:{ilen}"
                skipped[key] = skipped.get(key, 0) + 1
            cursor = end
        obj["texturedFaces"] = faces
    report["format"] = "psx-tmd-textured-uv-survey"
    report["texturedFaceCount"] = textured
    report["skippedPackets"] = skipped
    report["warning"] = "Experimental raw UV/CLUT/TPAGE only; VRAM textures/palettes not decoded"
    return report

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("--offset", type=lambda x: int(x, 0), default=0)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = inspect_uv(args.input.read_bytes(), args.offset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Textured faces: {result['texturedFaceCount']}; skipped packets: {sum(result['skippedPackets'].values())}")

if __name__ == "__main__":
    main()
