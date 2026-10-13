# Conversión experimental de caras TMD — versión 0.7.2

Se añade `tools-python/export_tmd_mesh.py`: decodificador **experimental y limitado** de primitivas TMD planas, sin iluminación ni texturas, para triángulos (modo `0x20`, flag sin iluminación) y cuadriláteros (modo `0x28`, flag sin iluminación). No interpreta el resto de los paquetes: los contabiliza en `skippedModes`. Valida referencias a vértices antes de exportarlas.

Para usar un archivo TMD previamente extraído de una copia propia:

```powershell
python tools-python/export_tmd_mesh.py ".local-assets/modelo.bin" --offset 0x0 --output "client-godot/assets/characters/model_mesh.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

En Godot 4 abre `res://scenes/tmd_mesh_preview.tscn` y ejecuta **F6**. La escena genera una malla de triángulos coloreados a partir del JSON. El modelo, offset y formato deben verificarse antes de confiar en el resultado; el ejemplo no corresponde a un fichero del protagonista confirmado. **No se ha probado en Godot y no se ha extraído aún el protagonista original.** Tampoco existe soporte para primitivas texturizadas, UV, huesos ni clips de animación. La escena es un visualizador de investigación independiente y no modifica la demo de mapas.

Los recursos protegidos quedan exclusivamente en las carpetas locales ignoradas por Git; solo se publican las herramientas y escenas.
