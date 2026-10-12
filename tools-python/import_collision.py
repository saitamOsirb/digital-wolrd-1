"""DW1 100x100 diagnostic collision matrix -> JSON for future Godot importer.

Input is an already-isolated 10,000-byte grid from user-owned game files.
No copyrighted data is included or downloaded by this tool.
"""
import argparse
import json
from pathlib import Path

GRID_SIZE = 100
SOLID_MASK = 0x80

def collision_rectangles(grid: bytes) -> list[dict[str, int]]:
    if len(grid) != GRID_SIZE * GRID_SIZE:
        raise ValueError("Se esperan exactamente 10000 bytes")
    rectangles = []
    previous = {}
    for y in range(GRID_SIZE):
        current = {}
        x = 0
        while x < GRID_SIZE:
            if not grid[y * GRID_SIZE + x] & SOLID_MASK:
                x += 1
                continue
            begin = x
            while x < GRID_SIZE and grid[y * GRID_SIZE + x] & SOLID_MASK:
                x += 1
            key = (begin, x)
            if key in previous:
                rectangle = previous[key]
                rectangle["height"] += 1
            else:
                rectangle = {"x": begin, "y": y, "width": x - begin, "height": 1}
                rectangles.append(rectangle)
            current[key] = rectangle
        previous = current
    return rectangles

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Archivo binario de exactamente 10.000 bytes")
    parser.add_argument("output", type=Path, help="Archivo JSON de diagnóstico")
    options = parser.parse_args()
    rectangles = collision_rectangles(options.input.read_bytes())
    document = {"schemaVersion": 1, "gridWidth": 100, "gridHeight": 100,
                "source": "local-extraction", "solidBit": 128, "rectangles": rectangles}
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(document, indent=2), encoding="utf-8")
    print(f"Generados {len(rectangles)} rectángulos -> {options.output}")

if __name__ == "__main__":
    main()
