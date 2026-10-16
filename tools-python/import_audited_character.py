"""Build a local Godot 3D preview from an audited DW1 CHDAT candidate.

The candidate archive path and byte offset MUST be selected explicitly from
an audit JSON report. TIM sources are likewise explicit ISO paths. This tool
never infers that a model belongs to the original protagonist.
"""
import argparse
import json
from pathlib import Path

from psx_iso import extract_iso_file
from build_godot_character_preview import build_preview

def select_candidate(audit: dict, archive: str, offset: int) -> dict:
    if audit.get("format") != "dw1-character-archive-audit":
        raise ValueError("Expected character audit JSON")
    matches = [row for row in audit.get("archives", [])
               if row.get("path") == archive and row.get("kind") in ("TMD0", "MMD0")]
    if len(matches) != 1:
        raise ValueError("Archive is absent or ambiguous in the audit")
    candidates = [model for model in matches[0].get("models", [])
                  if model.get("offset") == offset and
                  model.get("status") == "partial-ft3-ft4-decode" and
                  model.get("texturedFaces", 0) > 0]
    if len(candidates) != 1:
        raise ValueError("Selected offset has no supported audited FT3/FT4 faces")
    return candidates[0]

def build_from_disc(disc: Path, audit: dict, archive: str, offset: int,
                    tim_paths: list[str], output: Path) -> dict:
    if not tim_paths:
        raise ValueError("At least one actual TIM ISO path is required")
    candidate = select_candidate(audit, archive, offset)
    model = extract_iso_file(disc, archive)
    tims = [extract_iso_file(disc, path) for path in tim_paths]
    result = build_preview(model, tims, output, offset, expected_faces=candidate["texturedFaces"])
    decoded = sum(len(obj["faces"]) for obj in result["objects"])
    if decoded != candidate["texturedFaces"]:
        raise ValueError("Audited face count differs from actual decoded face count")
    # Do not include raw original data in the provenance report.
    (output / "provenance.json").write_text(json.dumps({
        "format": "dw1-character-preview-provenance",
        "archive": archive,
        "offset": offset,
        "timIsoPaths": tim_paths,
        "faces": decoded,
        "verifiedTamer": False,
        "verifiedAnimation": False,
    }, indent=2) + "\n", encoding="utf-8")
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disc", type=Path)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--archive", required=True, help="Exact archive ISO path from audit JSON")
    parser.add_argument("--offset", required=True, type=lambda x: int(x, 0))
    parser.add_argument("--tim-path", required=True, action="append",
                        help="Full ISO9660 path to a TIM resource; repeat as needed")
    parser.add_argument("--output", type=Path,
                        default=Path("client-godot/assets/characters/preview"))
    args = parser.parse_args()
    report = json.loads(args.audit.read_text(encoding="utf-8"))
    result = build_from_disc(args.disc, report, args.archive, args.offset,
                             args.tim_path, args.output)
    print("Generated local Godot preview with", sum(len(o["faces"]) for o in result["objects"]), "faces")
    print("Open res://scenes/tmd_textured_preview.tscn in Godot")

if __name__ == "__main__":
    main()
