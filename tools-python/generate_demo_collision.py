"""Generate synthetic fixtures for Godot; no original game assets."""
import argparse
import json
from pathlib import Path
from import_collision import collision_rectangles

def make_grid():
    grid = bytearray(10000)
    for i in range(100):
        grid[i] = 128
        grid[9900 + i] = 128
        grid[i * 100] = 128
        grid[i * 100 + 99] = 128
    for y in range(20, 32):
        for x in range(22, 38):
            grid[y * 100 + x] = 128
    return bytes(grid)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/diagnostic/collision.json"))
    args = parser.parse_args()
    payload = {
        "schemaVersion": 1, "gridWidth": 100, "gridHeight": 100,
        "solidBit": 128, "source": "synthetic",
        "rectangles": collision_rectangles(make_grid()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()
