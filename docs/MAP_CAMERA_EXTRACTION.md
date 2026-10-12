# Original MAP camera metadata — v0.5.3

The Python tools now extract camera and tile-layout metadata from the original PlayStation map setup, separate from the already reconstructed background image. This information is based on `dw_decomp/src/main/map.c` `loadMapSetup` and the first segment reference in `loadMap`.

From the repository root, with your own locally extracted USA disc image:

```powershell
python tools-python/import_original_map.py "D:\\ruta\\Digimon World (USA).bin" --map TWNA01
python tools-python/import_map_setup.py "D:\\ruta\\Digimon World (USA).bin"
python -m unittest discover -s tools-python -p "test_*.py"
```

The new output `client-godot/assets/demo/map_setup.json` contains:
- `camera.position` and `camera.target` as read from the map setup; each coordinate multiplied by 2, mirroring the decompiled loader.
- `camera.projectionDistance` from the original PlayStation configuration.
- `widthTiles`, `heightTiles`, `tileIds` and `nonemptyTiles`.

**This is a camera-metadata extraction milestone, not accurate Godot camera projection.** The map viewer remains a 2D background viewer with a diagnostic marker until coordinate transformations and overlays have been reconstructed and verified. The binary MAP file is not uploaded to GitHub, and exported local JSON remains gitignored.

The extraction assumes the first 32-bit little-endian pointer in the separate MAP file locates the `loadMapSetup` structure. This must be cross-checked on actual map files: invalid dimensions or truncation are rejected, but a plausible false-positive header is possible. Tests use constructed byte fixtures.
