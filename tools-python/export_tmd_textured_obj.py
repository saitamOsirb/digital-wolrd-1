"""Export experimentally decoded FT3/FT4 TMD faces as textured OBJ.

Requires a single separately reconstructed 256x256 PNG texture page,
and selects only faces matching the supplied TPAGE and CLUT. No automatic
VRAM layout detection, rigging or character identification.
"""
import argparse
import json
from pathlib import Path

def export_textured(report: dict, tpage: int, clut: int, png_name: str,
                    scale: float = 0.002, mtl_name: str = "textured.mtl") -> tuple[str, str, int]:
    if report.get("format") != "psx-tmd-textured-uv-survey":
        raise ValueError("Input must be a TMD textured UV survey")
    if not (0 < scale <= 1) or not (0 <= tpage <= 65535 and 0 <= clut <= 65535):
        raise ValueError("Invalid scale or GPU parameters")
    out = ["# Experimental TMD textured export", f"mtllib {mtl_name}"]
    offset = 0
    uv_offset = 0
    exported = 0
    for obj in report.get("objects", []):
        vertices = obj.get("vertices", [])
        out.append(f"o object_{int(obj['index'])}")
        for p in vertices:
            if len(p) != 3:
                raise ValueError("Invalid vertex")
            out.append("v %.8f %.8f %.8f" % (p[0] * scale, -p[1] * scale, p[2] * scale))
        for face in obj.get("texturedFaces", []):
            if face.get("tpage") != tpage or face.get("clut") != clut:
                continue
            indices, uv = face["indices"], face["uvRaw"]
            if len(indices) not in (3, 4) or len(indices) != len(uv):
                raise ValueError("Invalid face UV structure")
            if any(not isinstance(i, int) or i < 0 or i >= len(vertices) for i in indices):
                raise ValueError("Invalid face index")
            out.append("usemtl texture_page")
            for u, v in uv:
                if not (0 <= u <= 255 and 0 <= v <= 255):
                    raise ValueError("Invalid raw UV")
                out.append("vt %.8f %.8f" % ((u + 0.5) / 256, 1 - (v + 0.5) / 256))
            pairs = [f"{offset + i + 1}/{uv_offset + n + 1}" for n, i in enumerate(indices)]
            out.append("f " + " ".join(reversed(pairs)))
            uv_offset += len(uv)
            exported += 1
        offset += len(vertices)
    mtl = "\n".join(["newmtl texture_page", "Ka 0 0 0", "Kd 1 1 1", f"map_Kd {png_name}", ""])
    return "\n".join(out) + "\n", mtl, exported

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--tpage", type=lambda v: int(v, 0), required=True)
    parser.add_argument("--clut", type=lambda v: int(v, 0), required=True)
    parser.add_argument("--texture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.suffix.lower() != ".obj":
        parser.error("--output must be an OBJ file")
    if args.texture.parent.resolve() != args.output.parent.resolve():
        parser.error("--texture and --output must be in the same directory")
    obj, mtl, count = export_textured(json.loads(args.input.read_text(encoding="utf-8")),
                                      args.tpage, args.clut, args.texture.name,
                                      mtl_name=args.output.with_suffix(".mtl").name)
    if count == 0:
        parser.error("No faces match the selected TPAGE+CLUT")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(obj, encoding="utf-8")
    args.output.with_suffix(".mtl").write_text(mtl, encoding="utf-8")
    print(f"Exported {count} textured faces to {args.output}")

if __name__ == "__main__":
    main()
