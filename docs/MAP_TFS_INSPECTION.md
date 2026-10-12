# DW1 MAP ↔ TFS inspection — 0.3.3

The decompiled `dw_decomp/src/main/map.c` function `loadMapSetup(int32_t *data)` reads map width, height, then one signed 32-bit `MAP_TILES` entry for each grid cell. A value of `-1` denotes a background tile without source-image content. In `MAIN_func_800D634C`, TFS payloads are consumed only for entries that are not -1. This means background tiles and TFS records are **not** necessarily one-to-one across all map cells.

New tools:
- `tools-python/inspect_map_tiles.py` reads the tile layout from a previously isolated map setup segment, with a **mandatory independently established byte offset** for the width field.
- `tools-python/inspect_map_tfs.py` pairs nonempty MAP entries with candidate sequential TFS blocks.
- Both refuse invalid or truncated data; they do not search arbitrary game ISOs and cannot verify unknown offsets themselves.

Example (these commands need legitimately obtained, separately extracted map setup and TFS files):

```powershell
python tools-python/inspect_map_tiles.py ".local-assets/setup.bin" --width-offset 0 --output ".local-assets/tiles.json"
python tools-python/inspect_map_tfs.py ".local-assets/setup.bin" ".local-assets/map.tfs" --width-offset 0 --output ".local-assets/map-tfs.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

**Do not assume offset 0 is correct**. It is illustrative only; identify and validate the field location in the actual isolated map setup data before passing this option. The TFS layout is still a hypothesis to be validated against real files, especially its pixel packing and palette correspondence. No File City textures or executable game resources are distributed or claimed to have been extracted.

Future tasks: determine the map-setup byte offset from the complete data structure, verify TFS image packing, composite a genuine background image, and reproduce camera placement in the GDScript client.
