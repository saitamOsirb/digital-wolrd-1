"""Convert an experimental TMD mesh JSON into Wavefront OBJ + MTL.

Only already-decoded polygon faces are exported; no geometry is guessed.
The OBJ can be inspected in Blender or imported as a 3D model in Godot.
"""
import argparse
import json
from pathlib import Path

def convert(document: dict, scale: float = 0.002) -> tuple[str, str]:
    if document.get("format") != "psx-tmd-experimental-unlit-mesh":
        raise ValueError("Unsupported mesh document")
    if not 0 < scale <= 1:
        raise ValueError("scale must be in (0,1]")
    lines = ["# Experimental TMD mesh: no textures, rig or animation", "mtllib model.mtl"]
    material_lines = ["# Flat per-face materials reconstructed from decoded RGB values"]
    materials: set[tuple[int, int, int]] = set()
    vertex_offset = 0
    for obj in document.get("objects", []):
        vertices = obj.get("vertices", [])
        faces = obj.get("faces", [])
        lines.append("o object_%d" % int(obj.get("index", 0)))
        for point in vertices:
            if len(point) != 3:
                raise ValueError("Malformed vertex")
            x, y, z = (float(value) for value in point)
            lines.append(f"v {x*scale:.8f} {-y*scale:.8f} {z*scale:.8f}")
        for face in faces:
            indices = face.get("indices", [])
            rgb = face.get("rgb", [])
            if len(indices) not in (3, 4) or len(rgb) != 3:
                raise ValueError("Malformed face")
            if any(type(i) is not int or i < 0 or i >= len(vertices) for i in indices):
                raise ValueError("Face references missing vertex")
            if any(type(value) is not int or value < 0 or value > 255 for value in rgb):
                raise ValueError("Invalid RGB color")
            color = tuple(rgb)
            name = "rgb_%02x%02x%02x" % color
            if color not in materials:
                materials.add(color)
                material_lines.extend([f"newmtl {name}", "Kd %.6f %.6f %.6f" % tuple(value/255 for value in color), "Ka 0 0 0", ""])
            lines.append(f"usemtl {name}")
            # Reverse winding because changing the handedness (inverting Y) reverses normals.
            lines.append("f " + " ".join(str(vertex_offset + i + 1) for i in reversed(indices)))
        vertex_offset += len(vertices)
    return "\n".join(lines) + "\n", "\n".join(material_lines) + "\n"

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--output", type=Path, required=True, help="Output .obj path; .mtl written alongside it")
    cli.add_argument("--scale", type=float, default=0.002)
    args = cli.parse_args()
    if args.output.suffix.lower() != ".obj":
        cli.error("--output must be .obj")
    obj, mtl = convert(json.loads(args.input.read_text(encoding="utf-8")), args.scale)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Use model.mtl for a stable name referenced by the OBJ document.
    args.output.write_text(obj, encoding="utf-8")
    (args.output.parent / "model.mtl").write_text(mtl, encoding="utf-8")
    print("Wrote OBJ and MTL:", args.output)

if __name__ == "__main__":
    main()
