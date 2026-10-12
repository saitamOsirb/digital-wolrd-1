"""Convert any explicitly named TFS file from a user-supplied PS1 BIN.

Only writes local output. No game imagery is added to the repository.
"""
import argparse
import json
from pathlib import Path
from psx_iso import extract_iso_file
from render_tfs_map import decode_tfs_map
from convert_tim import encode_png

def convert_disc_tfs(disc: Path, internal_path: str, output: Path, palette: int = 0) -> dict:
    normalized = internal_path.replace("\\", "/")
    if not normalized.upper().endswith(".TFS"):
        raise ValueError("Only .TFS map image resources are supported")
    if any(part in ("", ".", "..") for part in normalized.split("/")):
        raise ValueError("Invalid internal path")
    tfs = extract_iso_file(disc, normalized)
    width, height, rgba = decode_tfs_map(tfs, palette)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encode_png(width, height, rgba))
    data = {"schemaVersion": 1, "source": "local-extraction",
            "mapId": Path(normalized).stem.upper(), "discPath": normalized,
            "texture": output.name, "widthPixels": width,
            "heightPixels": height, "paletteIndex": palette}
    output.with_suffix(".json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("disc", type=Path)
    cli.add_argument("internal_path", help="Example: MAP/MAP14/TWNA01.TFS")
    cli.add_argument("--palette", type=int, default=0)
    cli.add_argument("--output", type=Path, default=Path("client-godot/assets/demo/map.png"))
    args = cli.parse_args()
    report = convert_disc_tfs(args.disc, args.internal_path, args.output, args.palette)
    print("Imported", report["mapId"], report["widthPixels"], "x", report["heightPixels"])

if __name__ == "__main__":
    main()
