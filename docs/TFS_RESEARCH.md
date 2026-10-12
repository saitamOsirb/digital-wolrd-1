# TFS image stream investigation — 0.3.2

A review of `dw_decomp/src/main/map.c`, function `MAIN_func_800D634C`, establishes that the TFS stream starts with an unidentified 32-bit word and a 32-bit CLUT count. The routine advances by **128 uint32 (512 bytes) per CLUT**. For each *non-empty* background tile, it skips 1 uint32 and advances 4096 uint32 (16,384 bytes) of image payload.

This does not yet establish a full file format specification, tile pixel ordering, palette interpretation, or how emptiness is represented: the game uses MAP_TILES from another source.

`tools-python/inspect_tfs.py` safely reports candidate CLUT offsets and candidate tile segment offsets in a **user-supplied, already separated** TFS stream. The required `--tiles` count refers to known non-empty tile entries; it cannot be guessed from total map width/height. No original-game assets are included.

Example:

```powershell
python tools-python/inspect_tfs.py ".local-assets/map.tfs" --tiles 0 --output ".local-assets/report.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

A nonzero `--tiles` value must only be supplied after confirming it from the map's tile metadata. Output offsets are **candidates** to cross-check against real files, not proof that an arbitrary file matches the format.

Important: the map scene is a 2D tiled background with 3D character rendering, so the extraction roadmap must handle background compositing and projection separately from models.

Next: reconstruct MAP_TILES and map dimensions from the map metadata, identify background tile pixel packing and CLUT usage, and implement a Python renderer for an independently created synthetic fixture before importing the composited background into Godot.
