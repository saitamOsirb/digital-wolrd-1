"""Inspect PlayStation GPU TPAGE and CLUT fields from TMD UV reports.

This resolves texture-page coordinates and palette coordinates; matching
a decoded TIM image to VRAM is still a separate task.
"""
import argparse
import json
from pathlib import Path

def tpage_fields(value: int) -> dict:
    if not 0 <= value <= 0xFFFF:
        raise ValueError("TPAGE outside uint16")
    return {"raw": value, "x": (value & 0x0F) * 64,
            "y": ((value >> 4) & 1) * 256,
            "depthBpp": (4, 8, 16, 0)[(value >> 7) & 3],
            "semiTransparencyMode": (value >> 5) & 3,
            "textureDisable": bool(value & (1 << 11))}

def clut_fields(value: int) -> dict:
    if not 0 <= value <= 0xFFFF:
        raise ValueError("CLUT outside uint16")
    return {"raw": value, "x": (value & 0x3F) * 16, "y": (value >> 6) & 0x1FF}

def annotate(report: dict) -> dict:
    if report.get("format") != "psx-tmd-textured-uv-survey":
        raise ValueError("Expected UV survey JSON")
    count = 0
    for obj in report.get("objects", []):
        for face in obj.get("texturedFaces", []):
            face["texturePage"] = tpage_fields(face["tpage"])
            face["palette"] = clut_fields(face["clut"])
            count += 1
    report["gpuMetadataFaceCount"] = count
    report["warning"] = "GPU coordinates only. TIM VRAM placement and palette matching not reconstructed."
    return report

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    result = annotate(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Annotated textured faces:", result["gpuMetadataFaceCount"])

if __name__ == "__main__":
    main()
