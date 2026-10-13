"""Local PlayStation VRAM reconstruction from TIM image/CLUT blocks.

VRAM is 1024x512 16-bit words. Supports 4/8/16bpp texture sampling
using TMD TPAGE+CLUT and raw 8-bit UV. No STP blending simulation.
"""
import struct
from psx_tim import color
from inspect_psx_texture_pages import tpage_fields, clut_fields

WIDTH, HEIGHT = 1024, 512

class Vram:
    def __init__(self):
        self.words = bytearray(WIDTH * HEIGHT * 2)

    def upload(self, x: int, y: int, width: int, height: int, payload: bytes) -> None:
        if min(x, y, width, height) < 0 or x + width > WIDTH or y + height > HEIGHT:
            raise ValueError("VRAM upload outside bounds")
        if len(payload) != width * height * 2:
            raise ValueError("VRAM upload length mismatch")
        for row in range(height):
            dest = ((y + row) * WIDTH + x) * 2
            src = row * width * 2
            self.words[dest:dest+width*2] = payload[src:src+width*2]

    def load_tim(self, data: bytes) -> None:
        if len(data) < 20 or struct.unpack_from("<I", data)[0] != 0x10:
            raise ValueError("Invalid TIM magic")
        flags = struct.unpack_from("<I", data, 4)[0]
        mode = flags & 7
        if mode > 3 or flags & ~15:
            raise ValueError("Invalid TIM flags")
        cursor = 8
        blocks = 2 if flags & 8 else 1
        for _ in range(blocks):
            if cursor + 12 > len(data):
                raise ValueError("Truncated TIM block")
            size, x, y, w, h = struct.unpack_from("<IHHHH", data, cursor)
            if size < 12 or cursor + size > len(data):
                raise ValueError("Invalid TIM block size")
            self.upload(x, y, w, h, data[cursor+12:cursor+size])
            cursor += size

    def _word(self, x: int, y: int) -> int:
        if not 0 <= x < WIDTH or not 0 <= y < HEIGHT:
            raise ValueError("VRAM coordinate outside bounds")
        return struct.unpack_from("<H", self.words, (y * WIDTH + x) * 2)[0]

    def texel(self, tpage: int, clut: int, u: int, v: int) -> tuple[int, int, int, int]:
        if not 0 <= u < 256 or not 0 <= v < 256:
            raise ValueError("UV must be one byte")
        page = tpage_fields(tpage)
        palette = clut_fields(clut)
        depth = page["depthBpp"]
        if depth not in (4, 8, 16):
            raise ValueError("Unsupported texture depth")
        x = page["x"] + u // (16 // depth)
        y = page["y"] + v
        packed = self._word(x, y)
        if depth == 16:
            return color(packed)
        if depth == 8:
            index = (packed >> ((u & 1) * 8)) & 255
        else:
            index = (packed >> ((u & 3) * 4)) & 15
        return color(self._word(palette["x"] + index, palette["y"]))
