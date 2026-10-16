"""One-command local PS1 model preview build for Godot 4.

Consumes a previously identified TMD binary and known TIM loads. Produces
a scene-data manifest and texture pages for the Godot 3D preview. Supports
only FT3/FT4 unlit TMD packets currently understood by inspect_tmd_uv.
"""
import argparse
import json
from pathlib import Path
from inspect_tmd_uv import inspect_uv
from psx_vram import Vram
from render_psx_texture_page import render_page

def build_preview(model: bytes, tims: list[bytes], output: Path, offset: int = 0, expected_faces: int | None = None) -> dict:
    report = inspect_uv(model, offset)
    pages = sorted({(face["tpage"], face["clut"])
                    for obj in report["objects"] for face in obj["texturedFaces"]})
    if not pages:
        raise ValueError("No FT3/FT4 faces; cannot build a verified preview")
    actual_faces = sum(len(obj["texturedFaces"]) for obj in report["objects"])
    if expected_faces is not None and actual_faces != expected_faces:
        raise ValueError(f"Audit mismatch: expected {expected_faces} faces but decoded {actual_faces}")
    gpu = Vram()
    for tim in tims:
        gpu.load_tim(tim)
    generated = {}
    for tpage, clut in pages:
        generated[f"{tpage:04x}_{clut:04x}"] = render_page(gpu, tpage, clut)
    # Only write after all pages render correctly.
    output.mkdir(parents=True, exist_ok=True)
    for key, png in generated.items():
        (output / (key + ".png")).write_bytes(png)
    items = []
    for obj in report["objects"]:
        items.append({"index": obj["index"], "vertices": obj["vertices"],
                      "faces": [{"indices": face["indices"], "uvRaw": face["uvRaw"],
                                 "page": f"{face['tpage']:04x}_{face['clut']:04x}"}
                                for face in obj["texturedFaces"]]})
    manifest = {"schemaVersion": 1, "format": "dw1-textured-preview", "objects": items,
                "pages": {key: key + ".png" for key in generated},
                "skippedPackets": report["skippedPackets"],
                "experimental": True,
                "note": "Not confirmed to be protagonist; no skeleton, animation or full TMD support."}
    (output / "model.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")
    return manifest

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("model", type=Path)
    cli.add_argument("--tim", nargs="+", type=Path, required=True)
    cli.add_argument("--offset", type=lambda x: int(x, 0), default=0)
    cli.add_argument("--output", type=Path, default=Path("client-godot/assets/characters/preview"))
    args = cli.parse_args()
    result = build_preview(args.model.read_bytes(), [p.read_bytes() for p in args.tim],
                           args.output, args.offset)
    print(f"Exported {len(result['pages'])} pages and {sum(len(o['faces']) for o in result['objects'])} faces")

if __name__ == "__main__":
    main()
