"""Export all identified TMD texture-page groups from locally extracted assets.

Each (TPAGE, CLUT) group gets its own PNG, OBJ, and MTL. Unsupported
primitives remain excluded and are counted in a manifest.
"""
import argparse
import json
from pathlib import Path
from inspect_tmd_uv import inspect_uv
from psx_vram import Vram
from render_psx_texture_page import render_page
from export_tmd_textured_obj import export_textured

def build(model: bytes, tims: list[bytes], output: Path, offset: int = 0) -> dict:
    report = inspect_uv(model, offset)
    groups: dict[tuple[int, int], int] = {}
    for obj in report["objects"]:
        for face in obj["texturedFaces"]:
            key = (face["tpage"], face["clut"])
            groups[key] = groups.get(key, 0) + 1
    if not groups:
        raise ValueError("No supported textured faces found; no output created")
    gpu = Vram()
    for tim in tims:
        gpu.load_tim(tim)
    artifacts = []
    # Decode all pages in memory before writing any output.
    for (tpage, clut), expected in sorted(groups.items()):
        stem = f"page_{tpage:04x}_{clut:04x}"
        png_name = stem + ".png"
        obj_name = stem + ".obj"
        mtl_name = stem + ".mtl"
        png = render_page(gpu, tpage, clut)
        obj, mtl, count = export_textured(report, tpage, clut, png_name, mtl_name=mtl_name)
        if count != expected:
            raise ValueError("Texture-page group count mismatch")
        artifacts.append((stem, png, obj, mtl, tpage, clut, count))
    output.mkdir(parents=True, exist_ok=True)
    entries = []
    for stem, png, obj, mtl, tpage, clut, count in artifacts:
        (output / (stem + ".png")).write_bytes(png)
        (output / (stem + ".obj")).write_text(obj, encoding="utf-8")
        (output / (stem + ".mtl")).write_text(mtl, encoding="utf-8")
        entries.append({"tpage": tpage, "clut": clut, "faces": count,
                        "obj": stem + ".obj", "mtl": stem + ".mtl", "png": stem + ".png"})
    manifest = {"schemaVersion": 1, "status": "experimental-incomplete-tmd",
                "textureGroups": entries, "exportedFaces": sum(groups.values()),
                "skippedPackets": report["skippedPackets"],
                "warning": "Model, textures and animation NOT verified against original game."}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("model", type=Path)
    cli.add_argument("--tim", type=Path, nargs="+", required=True)
    cli.add_argument("--offset", type=lambda value: int(value, 0), default=0)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    manifest = build(args.model.read_bytes(), [path.read_bytes() for path in args.tim], args.output, args.offset)
    print("Texture groups:", len(manifest["textureGroups"]), "faces:", manifest["exportedFaces"])

if __name__ == "__main__":
    main()
