"""Cross-check sparse MAP tile metadata with candidate TFS tile records."""
import argparse
import json
from pathlib import Path
from inspect_map_tiles import read_tile_layout
from inspect_tfs import inspect_tfs

def build_report(map_setup: bytes, width_offset: int, tfs: bytes) -> dict:
    layout = read_tile_layout(map_setup, width_offset)
    texture = inspect_tfs(tfs, layout["nonemptyCount"])
    entries = []
    for index, record in zip(layout["nonemptyIndices"], texture["tileRecords"]):
        entries.append({"tileIndex": index, "tileId": layout["tileIds"][index],
                        "column": index % layout["width"], "row": index // layout["width"],
                        "candidatePayloadOffset": record["payloadOffset"],
                        "candidatePayloadBytes": record["payloadBytes"]})
    return {"schemaVersion": 1, "width": layout["width"], "height": layout["height"],
            "tilePixelSize": 128, "nonemptyCount": len(entries),
            "clutCount": texture["clutCount"], "tiles": entries,
            "status": "candidate-layout-only"}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("map_setup", type=Path)
    parser.add_argument("tfs", type=Path)
    parser.add_argument("--width-offset", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_report(args.map_setup.read_bytes(), args.width_offset, args.tfs.read_bytes())
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()
