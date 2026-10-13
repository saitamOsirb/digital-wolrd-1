"""Audit DW1 CHDAT model candidates directly from a local raw PlayStation BIN.

This report identifies which files contain TMD structures decodable by the
project's current tooling, and which decoder step fails. It does not identify
the canonical tamer or export copyrighted data.
"""
import argparse
import json
from pathlib import Path

from discover_dw1_character_archives import (
    MAX_SCAN_BYTES, find_character_archives,
)
from list_disc_maps import list_disc_files
from psx_iso import extract_iso_file
from scan_psx_tmd import scan_tmd
from export_tmd_vertices import read_vertices
from inspect_tmd_uv import inspect_uv

def audit(disc: Path, max_files: int = 400) -> dict:
    archives = find_character_archives(list_disc_files(disc, suffix=""))
    if len(archives) > max_files:
        raise ValueError("Too many candidate files; increase --max-files explicitly")
    items = []
    for entry in archives:
        item = dict(entry)
        item["models"] = []
        if entry["kind"] not in ("TMD0", "MMD0") or entry["size"] > MAX_SCAN_BYTES:
            item["status"] = "animation-or-oversize-not-scanned"
            items.append(item)
            continue
        try:
            binary = extract_iso_file(disc, entry["path"])
            hits = scan_tmd(binary, max_hits=64)
            for hit in hits:
                location = hit["byteOffset"]
                record = {"offset": location, "objects": hit["objects"]}
                try:
                    model = read_vertices(binary, location)
                    record["vertexCount"] = model["vertexCount"]
                    try:
                        surface = inspect_uv(binary, location)
                        record["texturedFaces"] = surface["texturedFaceCount"]
                        record["skippedPackets"] = sum(surface["skippedPackets"].values())
                        record["status"] = "partial-ft3-ft4-decode"
                    except (ValueError, IndexError, KeyError, TypeError, OverflowError) as exc:
                        record["status"] = "vertex-only"
                        record["reason"] = type(exc).__name__
                except (ValueError, IndexError, KeyError, TypeError, OverflowError) as exc:
                    record["status"] = "signature-only"
                    record["reason"] = type(exc).__name__
                item["models"].append(record)
            item["status"] = "candidates-found" if hits else "no-tmd-signatures"
        except (OSError, ValueError) as exc:
            item["status"] = "file-read-error"
            item["reason"] = type(exc).__name__
        items.append(item)
    return {
        "schemaVersion": 1,
        "format": "dw1-character-archive-audit",
        "archives": items,
        "summary": {
            "archives": len(items),
            "tmdCandidates": sum(len(x["models"]) for x in items),
            "ft3ft4Faces": sum(m.get("texturedFaces", 0) for x in items for m in x["models"]),
        },
        "warning": "A decoded candidate is not proof of a protagonist model. MTN/MMD animations are not decoded.",
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc", type=Path, help="Locally owned Mode2/2352 PlayStation BIN")
    parser.add_argument("--max-files", type=int, default=400)
    parser.add_argument("--output", type=Path, default=Path(".local-assets/character-audit.json"))
    args = parser.parse_args()
    if args.max_files <= 0 or args.max_files > 10000:
        parser.error("--max-files must be between 1 and 10000")
    result = audit(args.disc, args.max_files)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Archives:", result["summary"]["archives"])
    print("TMD candidates:", result["summary"]["tmdCandidates"])
    print("Supported textured faces:", result["summary"]["ft3ft4Faces"])
    print("Report:", args.output)

if __name__ == "__main__":
    main()
