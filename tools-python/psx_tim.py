"""Parse PlayStation TIM texture containers (4/8/16/24 bpp) without external packages.

Converts TIM data to RGBA bytes. Handles STP as a diagnostic alpha flag;
texture blending semantics must be validated per material.
"""
from dataclasses import dataclass
import struct

@dataclass(frozen=True)
class Image:
    width: int
    height: int
    rgba: bytes
    mode: int

def u32(data: bytes, pos: int) -> int:
    if pos + 4 > len(data):
        raise ValueError("Truncated TIM")
    return struct.unpack_from("<I", data, pos)[0]

def block(data: bytes, offset: int):
    size = u32(data, offset)
    if size < 12 or offset + size > len(data):
        raise ValueError("Invalid TIM block size")
    x, y, width, height = struct.unpack_from("<HHHH", data, offset + 4)
    return offset + size, width, height, data[offset + 12:offset + size]

def color(pixel: int) -> tuple[int, int, int, int]:
    r = (pixel & 31) * 255 // 31
    g = ((pixel >> 5) & 31) * 255 // 31
    b = ((pixel >> 10) & 31) * 255 // 31
    alpha = 0 if pixel == 0 else 255
    return r, g, b, alpha

def decode(data: bytes, palette_index: int = 0) -> Image:
    if len(data) < 20 or u32(data, 0) != 0x10:
        raise ValueError("Not a TIM")
    flags = u32(data, 4)
    mode = flags & 7
    if mode > 3 or flags & ~0xF:
        raise ValueError("Unsupported TIM flags")
    has_clut = bool(flags & 8)
    if has_clut != (mode in (0, 1)):
        raise ValueError("TIM palette flag does not match pixel mode")
    offset = 8
    palette = []
    if has_clut:
        offset, pw, ph, colors = block(data, offset)
        if len(colors) != pw * ph * 2:
            raise ValueError("Invalid CLUT payload")
        size = 16 if mode == 0 else 256
        if pw * ph % size != 0 or palette_index < 0 or palette_index >= pw * ph // size:
            raise ValueError("Invalid palette index")
        start = palette_index * size * 2
        palette = struct.unpack_from("<" + "H" * size, colors, start)
    elif palette_index != 0:
        raise ValueError("No palettes in truecolor TIM")
    offset, words, height, pixels = block(data, offset)
    width = words * (4 if mode == 0 else 2 if mode == 1 else 1 if mode == 2 else 2 / 3)
    if not isinstance(width, int):
        if width != int(width):
            raise ValueError("24bpp row width is not integral")
        width = int(width)
    if width <= 0 or height <= 0 or width * height > 16_000_000:
        raise ValueError("Invalid TIM dimensions")
    if len(pixels) != words * 2 * height:
        raise ValueError("Invalid pixel data length")
    result = bytearray()
    row_bytes = words * 2
    for row in range(height):
        scan = pixels[row * row_bytes:(row + 1) * row_bytes]
        if mode == 0:
            indices = [c for byte in scan for c in (byte & 15, byte >> 4)]
            for index in indices:
                result.extend(color(palette[index]))
        elif mode == 1:
            for index in scan:
                result.extend(color(palette[index]))
        elif mode == 2:
            for i in range(0, len(scan), 2):
                result.extend(color(int.from_bytes(scan[i:i + 2], "little")))
        else:
            for i in range(0, width * 3, 3):
                result.extend((*scan[i:i + 3], 255))
    return Image(width, height, bytes(result), mode)
