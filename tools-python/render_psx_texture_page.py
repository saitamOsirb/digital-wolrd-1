"""Render a PS1 VRAM texture page to PNG using locally supplied TIM blocks.

TPage and CLUT values come from inspect_tmd_uv.py. This yields a 256x256
RGBA diagnostic texture page, not a verified character material.
"""
import argparse
from pathlib import Path
from convert_tim import encode_png
from psx_vram import Vram
from inspect_psx_texture_pages import tpage_fields

def render_page(gpu: Vram, tpage: int, clut: int) -> bytes:
    depth = tpage_fields(tpage)["depthBpp"]
    if depth not in (4, 8, 16):
        raise ValueError("Unsupported TPAGE depth")
    rgba = bytearray(256 * 256 * 4)
    for y in range(256):
        for x in range(256):
            at = (y * 256 + x) * 4
            rgba[at:at+4] = bytes(gpu.texel(tpage, clut, x, y))
    return encode_png(256, 256, rgba)

def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("tim", nargs="+", type=Path, help="Local TIM files loaded into VRAM in the specified order")
    cli.add_argument("--tpage", type=lambda v: int(v, 0), required=True)
    cli.add_argument("--clut", type=lambda v: int(v, 0), default=0)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    gpu = Vram()
    for path in args.tim:
        gpu.load_tim(path.read_bytes())
    png = render_page(gpu, args.tpage, args.clut)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(png)
    print("Rendered 256x256 texture page:", args.output)

if __name__ == "__main__":
    main()
