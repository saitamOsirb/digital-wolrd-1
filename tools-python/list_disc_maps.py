"""List ISO9660 files from a locally supplied raw PS1 BIN.

This is a metadata-only indexer: it does not copy or publish game resources.
"""
import argparse
import json
from pathlib import Path
from psx_iso import read_extent, directory_entries, LOGICAL_SIZE

def list_disc_files(path: Path, suffix: str = ".TFS") -> list[dict]:
    output = []
    with path.open("rb") as disc:
        volume = read_extent(disc, 16, LOGICAL_SIZE)
        if volume[:7] != bytes([1]) + b"CD001" + bytes([1]):
            raise ValueError("Expected Mode2/2352 ISO9660 image")
        root = volume[156:190]
        folders = [("", int.from_bytes(root[2:6], "little"), int.from_bytes(root[10:14], "little"), 0)]
        visited = set()
        while folders:
            folder, lba, size, depth = folders.pop()
            if depth > 16 or size > 16 * 1024 * 1024:
                raise ValueError("Directory exceeds safety limits")
            if (lba, size) in visited:
                continue
            visited.add((lba, size))
            for item in directory_entries(read_extent(disc, lba, size)):
                filename = folder + item["name"]
                if item["directory"]:
                    folders.append((filename + "/", item["lba"], item["size"], depth + 1))
                elif filename.upper().endswith(suffix.upper()):
                    output.append({"path": filename, "size": item["size"]})
                if len(output) > 15000:
                    raise ValueError("Too many directory entries")
    return sorted(output, key=lambda entry: entry["path"])

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("disc", type=Path)
    cli.add_argument("--suffix", default=".TFS")
    cli.add_argument("--output", type=Path)
    args = cli.parse_args()
    files = list_disc_files(args.disc, args.suffix)
    output = json.dumps({"format": "ps1-iso9660", "count": len(files), "files": files}, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)

if __name__ == "__main__":
    main()
