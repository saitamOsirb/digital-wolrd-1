"""Analyze original PS1 game archive filenames without assuming 3D file formats.

Read a locally owned raw BIN and report common model/animation candidates.
No commercial model bytes are exported or uploaded.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from list_disc_maps import list_disc_files

def model_inventory(disc: Path) -> dict:
    entries = list_disc_files(disc, suffix="")
    candidates = []
    model_terms = ("MODEL", "CHAR", "TAMER", "ANIM", "MESH", "SPRITE", "MMD", "TMD", "EMD", "TIM")
    for entry in entries:
        location = entry["path"].upper()
        if any(term in location for term in model_terms):
            candidates.append(entry)
    return {
        "schemaVersion": 1,
        "totalFiles": len(entries),
        "extensionCounts": dict(sorted(Counter(Path(item["path"]).suffix.upper() or "(none)" for item in entries).items())),
        "candidateFiles": candidates,
        "status": "filename-candidates-not-verified-models"
    }

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("disc", type=Path)
    cli.add_argument("--output", type=Path, default=Path(".local-assets/model-inventory.json"))
    args = cli.parse_args()
    report = model_inventory(args.disc)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {report['totalFiles']} files; {len(report['candidateFiles'])} model/animation filename candidates")
    print("Report:", args.output)

if __name__ == "__main__":
    main()
