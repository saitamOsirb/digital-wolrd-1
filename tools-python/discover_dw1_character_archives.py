"""Discover DW1 character archives on a locally supplied PlayStation disc.

Use the actual ISO9660 directory index and optionally inspect TMD signatures.
Does not guess that archive filenames identify the protagonist.
"""
import argparse
import json
from pathlib import Path
from list_disc_maps import list_disc_files
from psx_iso import extract_iso_file
from scan_psx_tmd import scan_tmd

FOLDERS = ("CHDAT/TMD0/", "CHDAT/MMD0/", "CHDAT/MTN0/")
MAX_SCAN_BYTES = 32 * 1024 * 1024

def find_character_archives(files: list[dict]) -> list[dict]:
    results = []
    for entry in files:
        name = str(entry["path"]).replace("\\", "/")
        normalized = name.upper()
        kind = next((prefix.split("/")[1] for prefix in FOLDERS
                     if normalized.startswith(prefix)), None)
        if kind is not None:
            results.append({"path": name, "size": int(entry["size"]), "kind": kind})
    return sorted(results, key=lambda item: item["path"])

def inventory(disc: Path, scan: bool = False) -> dict:
    candidates = find_character_archives(list_disc_files(disc, suffix=""))
    for candidate in candidates:
        candidate["tmdCandidates"] = []
        if scan and candidate["size"] <= MAX_SCAN_BYTES and candidate["kind"] in ("TMD0", "MMD0"):
            data = extract_iso_file(disc, candidate["path"])
            candidate["tmdCandidates"] = [
                {"offset": hit["byteOffset"], "objects": hit["objects"]}
                for hit in scan_tmd(data, max_hits=100)]
    return {
        "schemaVersion": 1,
        "archiveDirectories": list(FOLDERS),
        "archives": candidates,
        "counts": {key.split("/")[1]: sum(a["kind"] == key.split("/")[1] for a in candidates)
                   for key in FOLDERS},
        "warning": "These are archive candidates, not verified tamer geometry or animations."
    }

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("disc", type=Path, help="User-owned raw BIN (Mode2/2352)")
    cli.add_argument("--scan-tmd", action="store_true", help="Inspect TMD signatures without exporting game data")
    cli.add_argument("--output", type=Path, default=Path(".local-assets/character-archive-inventory.json"))
    args = cli.parse_args()
    result = inventory(args.disc, args.scan_tmd)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Character archive candidates:", len(result["archives"]))
    print("Report:", args.output)

if __name__ == "__main__":
    main()
