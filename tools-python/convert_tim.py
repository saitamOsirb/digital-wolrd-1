"""Convert a locally supplied PS1 TIM file into PNG (RGBA, stdlib only)."""
import argparse
from pathlib import Path
import struct
import zlib
from psx_tim import decode

def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

def encode_png(width: int, height: int, rgba: bytes) -> bytes:
    if width <= 0 or height <= 0 or len(rgba) != width * height * 4:
        raise ValueError("Invalid RGBA raster")
    stride = width * 4
    raw = b"".join(b"\x00" + rgba[y * stride:(y + 1) * stride] for y in range(height))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--palette", type=int, default=0)
    args = parser.parse_args()
    image = decode(args.input.read_bytes(), args.palette)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encode_png(image.width, image.height, image.rgba))
    print(f"Decoded {image.width}x{image.height} TIM mode={image.mode}: {args.output}")

if __name__ == "__main__":
    main()
