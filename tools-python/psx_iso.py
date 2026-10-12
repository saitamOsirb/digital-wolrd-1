"""Extract a named MAP/TFS file from a locally provided PS1 Mode2/2352 BIN.

Disc reading uses 2048-byte ISO9660 sectors starting 24 bytes into each
2352-byte raw sector. Does not publish or bundle copyrighted assets.
"""
import argparse
from pathlib import Path

SECTOR_SIZE = 2352
DATA_OFFSET = 24
LOGICAL_SIZE = 2048

def read_extent(handle, lba: int, length: int) -> bytes:
    if lba < 0 or length < 0:
        raise ValueError("Invalid extent")
    out = bytearray()
    count = (length + LOGICAL_SIZE - 1) // LOGICAL_SIZE
    for sector in range(count):
        handle.seek((lba + sector) * SECTOR_SIZE + DATA_OFFSET)
        piece = handle.read(LOGICAL_SIZE)
        if len(piece) != LOGICAL_SIZE:
            raise ValueError("Truncated disc image")
        out.extend(piece)
    return bytes(out[:length])

def directory_entries(data: bytes):
    pos = 0
    while pos < len(data):
        length = data[pos]
        if length == 0:
            pos = (pos // LOGICAL_SIZE + 1) * LOGICAL_SIZE
            continue
        entry = data[pos:pos + length]
        pos += length
        if len(entry) < 34:
            raise ValueError("Malformed directory record")
        name_length = entry[32]
        name = entry[33:33 + name_length].decode("ascii", "replace")
        if name in ("\\x00", "\\x01"):
            continue
        yield {"name": name.split(";")[0], "lba": int.from_bytes(entry[2:6], "little"),
               "size": int.from_bytes(entry[10:14], "little"),
               "directory": bool(entry[25] & 2)}

def extract_iso_file(path: Path, target: str) -> bytes:
    components = [segment.upper() for segment in target.replace("\\", "/").split("/") if segment]
    if not components or any(part in (".", "..") for part in components):
        raise ValueError("Invalid internal path")
    with path.open("rb") as handle:
        descriptor = read_extent(handle, 16, LOGICAL_SIZE)
        if descriptor[:7] != b"\\x01CD001\\x01":
            raise ValueError("Not an ISO9660 primary volume descriptor in Mode2/2352")
        root = descriptor[156:190]
        current_lba = int.from_bytes(root[2:6], "little")
        current_size = int.from_bytes(root[10:14], "little")
        for i, component in enumerate(components):
            if current_size > 16 * 1024 * 1024:
                raise ValueError("Directory too large")
            entries = directory_entries(read_extent(handle, current_lba, current_size))
            found = next((entry for entry in entries if entry["name"].upper() == component), None)
            if found is None:
                raise FileNotFoundError("Missing file on disc: " + "/".join(components[:i+1]))
            if i < len(components) - 1 and not found["directory"]:
                raise ValueError("Expected directory: " + component)
            current_lba, current_size = found["lba"], found["size"]
        if found["directory"] or current_size > 64 * 1024 * 1024:
            raise ValueError("Invalid or too-large file")
        return read_extent(handle, current_lba, current_size)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bin", type=Path)
    parser.add_argument("path", help="e.g. MAP/MAP14/TWNA01.TFS")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = extract_iso_file(args.bin, args.path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(f"Extracted {args.path}: {len(data)} bytes")

if __name__ == "__main__":
    main()
