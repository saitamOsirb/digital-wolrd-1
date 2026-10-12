# Godot texture preview — 0.3.1

This pipeline is strictly Godot (GDScript) + Python. No TypeScript.

## Reproducible diagnostic scene (synthetic assets)

From the repository root:

```powershell
python tools-python/generate_demo_collision.py
python tools-python/generate_demo_texture.py
python -m unittest discover -s tools-python -p "test_*.py"
```

Open `client-godot/project.godot` with Godot 4 and press F5. The camera follows the temporary capsule character. Obstacles load from `res://assets/diagnostic/collision.json`. A new square at the back of the map previews a PNG at `res://assets/diagnostic/texture.png` using nearest-neighbor sampling. The preview image is generated from a fully synthetic 16bpp TIM fixture; it does not reproduce any copyrighted texture.

## Inspecting a local texture you are authorized to use

```powershell
python tools-python/convert_tim.py ".local-assets/example.tim" "client-godot/assets/diagnostic/texture.png"
```

The generated diagnostic directory is ignored by git. Do not commit original game files or extracted graphics.

## Scope and limitations

- This is a **texture conversion end-to-end preview**, not map reconstruction.
- The actual DW1 map's TFS texture sheets, CLUT placement, tiles and overlays require additional format work.
- DW1 uses PlayStation 2D map imagery and 3D characters; do not infer full 3D landscape geometry from the diagnostic boxes.
- No C# networking modifications are included. Server is unchanged.
- Godot execution still requires verification in the editor.
