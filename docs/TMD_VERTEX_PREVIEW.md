# Inspección 3D de vértices TMD — 0.7.0

Nuevo avance en la recuperación de modelos de Digimon World 1 para PlayStation: un convertidor de geometría **de solo vértices** que recibe un TMD obtenido de una copia legítima del disco y produce un JSON que Godot puede mostrar como una nube de puntos.

## Preparar los datos

Primero localiza un archivo binario que contenga un TMD utilizando `tools-python/inspect_character_assets.py`, la documentación de `dw_decomp` y `tools-python/scan_psx_tmd.py`. El escáner devuelve los desplazamientos **candidatos**; no todos son modelos válidos ni corresponden al protagonista.

```powershell
python tools-python/export_tmd_vertices.py ".local-assets/modelo.bin" --offset 0x0 --output "client-godot/assets/characters/model_vertices.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

Reemplaza `.local-assets/modelo.bin` y `0x0` por el archivo y el desplazamiento verificados. El convertidor acepta TMD con punteros relativos (flags=0), verifica las tablas y límites, y exporta los vértices agrupados por objeto. **No genera mallas cerradas, caras, UV, texturas, esqueleto ni animaciones**.

## Vista de Godot

Abre `client-godot/project.godot`, selecciona la escena `res://scenes/tmd_point_preview.tscn` y ejecuta **F6** para previsualizar los vértices 3D. Se trata de un visor de ingeniería inversa independiente: no reemplaza el visor de mapas ni añade automáticamente el protagonista a File City. La escala e inversión del eje Y son provisionales.

Los recursos extraídos permanecen en `assets/characters/` (gitignored). No se incluyen modelos originales comerciales en el repositorio. **La nueva escena y el conversor todavía no se han ejecutado conjuntamente en Godot**, por lo que el resultado requiere validación posterior.
