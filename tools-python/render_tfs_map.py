"""Decode complete DW1 TFS tiled background into RGBA.

Verified against an original US-disc map stream: header contains uint16 width,
uint16 height, uint32 number of 256-color palettes; tile records follow palettes
and contain 4-byte metadata plus 128x128 8bpp indices each.
"""
import argparse
from pathlib import Path
import struct
from convert_tim import encode_png

TILE_SIDE = 128
TILE_PIXELS = 16384
TILE_RECORD_SIZE = 4 + TILE_PIXELS
PALETTE_BYTES = 512

def psx_color(value: int) -> tuple[int, int, int, int]:
    # Direct display of map backgrounds is opaque: zero-valued black is visible.
    return ((value & 31) * 255 // 31,
            ((value >> 5) & 31) * 255 // 31,
            ((value >> 10) & 31) * 255 // 31, 255)

def decode_tfs_map(data: bytes, palette_index: int = 0) -> tuple[int, int, bytes]:
    if len(data) < 8:
        raise ValueError("Truncated TFS header")
    width_tiles, height_tiles, count = struct.unpack_from("<HHI", data)
    if not (1 <= width_tiles <= 16 and 1 <= height_tiles <= 16):
        raise ValueError("Invalid TFS map dimensions")
    if count < 1 or count > 64 or not 0 <= palette_index < count:
        raise ValueError("Invalid TFS palette index/count")
    palettes_end = 8 + count * PALETTE_BYTES
    tile_count = width_tiles * height_tiles
    expected = palettes_end + tile_count * TILE_RECORD_SIZE
    if len(data) < expected:
        raise ValueError("Truncated TFS tile data")
    # Some maps include padding or extra data; do not require strict equality.
    colors = struct.unpack_from("<256H", data, 8 + palette_index * PALETTE_BYTES)
    palette = [bytes(psx_color(pixel)) for pixel in colors]
    image_width = width_tiles * TILE_SIDE
    image_height = height_tiles * TILE_SIDE
    result = bytearray(image_width * image_height * 4)
    for tile_index in range(tile_count):
        col = tile_index % width_tiles
        row = tile_index // width_tiles
        tile_data_offset = palettes_end + tile_index * TILE_RECORD_SIZE + 4
        for y in range(TILE_SIDE):
            offset = tile_data_offset + y * TILE_SIDE
            dst = ((row * TILE_SIDE + y) * image_width + col * TILE_SIDE) * 4
            result[dst:dst + TILE_SIDE * 4] = b"".join(palette[p] for p in data[offset:offset + TILE_SIDE])
    return image_width, image_height, bytes(result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Isolated original .TFS")
    parser.add_argument("output", type=Path, help="Target PNG, kept locally")
    parser.add_argument("--palette", type=int, default=0)
    args = parser.parse_args()
    width, height, rgba = decode_tfs_map(args.input.read_bytes(), args.palette)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encode_png(width, height, rgba))
    print(f"Rendered genuine TFS background: {width}x{height} -> {args.output}")

if __name__ == "__main__":
    main()
