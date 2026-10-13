# Exportación experimental TMD → OBJ/MTL — 0.7.3

El nuevo script `tools-python/export_tmd_obj.py` convierte las caras **ya decodificadas** por `export_tmd_mesh.py` en archivos Wavefront OBJ y MTL, que pueden inspeccionarse en Blender o importarse en Godot. Preserva objetos por separado, triangulación/quads y materiales planos RGB; invierte el eje Y y corrige el orden de vértices. No extrae caras nuevas de archivos PS1, no reconstruye UV/texturas ni anima personajes.

```powershell
python tools-python/export_tmd_mesh.py ".local-assets/modelo.bin" --offset 0x0 --output ".local-assets/modelo.json"
python tools-python/export_tmd_obj.py ".local-assets/modelo.json" --output ".local-assets/modelo.obj"
python -m unittest discover -s tools-python -p "test_*.py"
```

El segundo comando produce `modelo.obj` y `modelo.mtl`. Usa un TMD válido extraído localmente de una copia del juego que poseas; el ejemplo no identifica al protagonista. Actualmente solo se exportan las primitivas limitadas que interpreta el conversor experimental precedente. **No es todavía el modelo 3D auténtico ni una malla completa del protagonista.** El proyecto sigue necesitando identificación de recursos, primitivas texturizadas, UV, texturas, rig y animaciones.

No se incluyen archivos protegidos en GitHub y estas herramientas todavía no han sido validadas en el entorno de juego de Godot.
