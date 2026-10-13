"""Batch convert locally owned PS1 TFS backgrounds for browsing in Godot.

Per-map errors are reported; failures never silently become synthetic maps.
No extracted commercial assets are committed to the repository.
"""
import argparse
import json
from pathlib import Path
from list_disc_maps import list_disc_files
from import_disc_tfs import convert_disc_tfs

def batch_import(disc: Path, output: Path, limit: int = 0, palette: int = 0) -> dict:
    if limit < 0 or limit > 2000:
        raise ValueError("limit must be between 0 and 2000")
    if palette < 0 or palette > 63:
        raise ValueError("palette must be between 0 and 63")
    files = list_disc_files(disc, ".TFS")
    if limit:
        files = files[:limit]
    output.mkdir(parents=True, exist_ok=True)
    entries, errors = [], []
    for item in files:
        path = item["path"]
        relative = Path(path)
        target = output / relative.parent / (relative.stem + ".png")
        try:
            metadata = convert_disc_tfs(disc, path, target, palette)
            entries.append({"name": metadata["mapId"], "image": target.relative_to(output).as_posix(),
                            "width": metadata["widthPixels"], "height": metadata["heightPixels"],
                            "discPath": path})
        except (ValueError, OSError) as error:
            errors.append({"discPath": path, "reason": str(error)})
    manifest = {"schemaVersion": 1, "source": "local-extraction",
                "maps": entries, "failed": errors}
    (output / "catalog.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc", type=Path)
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/maps"))
    parser.add_argument("--limit", type=int, default=0, help="Maximum number, 0 for all")
    parser.add_argument("--palette", type=int, default=0)
    args = parser.parse_args()
    result = batch_import(args.disc, args.output, args.limit, args.palette)
    print(f"Imported {len(result['maps'])} maps; {len(result['failed'])} unsupported/failed")
    for failure in result["failed"][:12]:
        print("SKIPPED", failure["discPath"], failure["reason"])

if __name__ == "__main__":
    main()
