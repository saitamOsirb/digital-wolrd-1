"""Create a synthetic 16-bpp PlayStation TIM and PNG for testing Godot texture display."""
import argparse
from pathlib import Path
import struct
from psx_tim import decode
from convert_tim import encode_png

def make_tim(width=32, height=32):
    if width <= 0 or height <= 0 or width > 256 or height > 256:
        raise ValueError("Invalid fixture size")
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            # Alternating 8x8 blocks in RGB555.
            red = 31 if (x // 8 + y // 8) % 2 else 6
            green = 12 if x // 8 % 2 else 28
            blue = 27 if y // 8 % 2 else 5
            value = red | (green << 5) | (blue << 10)
            pixels += struct.pack("<H", value)
    return (struct.pack("<II", 0x10, 2)
            + struct.pack("<IHHHH", 12 + len(pixels), 0, 0, width, height)
            + pixels)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("client-godot/assets/diagnostic/texture.png"))
    options = parser.parse_args()
    tim = make_tim()
    decoded = decode(tim)
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_bytes(encode_png(decoded.width, decoded.height, decoded.rgba))
    print("Generated synthetic preview:", options.output)

if __name__ == "__main__":
    main()
