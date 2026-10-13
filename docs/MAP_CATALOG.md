# Catálogo de mapas originales — 0.5.5

Esta versión permite convertir un conjunto de fondos TFS reales de una copia local y navegar entre ellos directamente desde Godot, sin alterar el código del visor después de cada importación.

## Windows / PowerShell

Descomprime el BIN desde tu archivo 7z y, desde la raíz del repositorio:

```powershell
python tools-python/import_all_maps.py "D:\\ruta\\Digimon World (USA).bin" --limit 20
python -m unittest discover -s tools-python -p "test_*.py"
```

Para intentar todos los mapas reconocidos, omite `--limit 20`. El convertidor guarda PNG por ruta de archivo en `client-godot/assets/maps/`, y genera `catalog.json` con éxitos y fallos por archivo. Los recursos originales y el manifiesto están ignorados por git y no se distribuyen en el repositorio.

Abre `client-godot/project.godot` y pulsa F5. Usa **PageUp/PageDown** para pasar entre mapas, rueda para zoom, arrastrar para mover el lienzo, WASD/flechas para el marcador de diagnóstico, Shift+clic para posicionarlo, F para seguimiento y R para reencuadrar.

Si no se ha preparado el catálogo, el visor conserva compatibilidad con el PNG individual `client-godot/assets/demo/map.png`.

## Alcance real

El resultado son **fondos gráficos originales** del juego, no niveles 3D interactivos. El marcador no es el protagonista y no usa el posicionamiento ni colisiones de PS1. La conversión de TFS aún requiere contrastar escenas con tiles vacíos, overlays y variantes de paleta. Algunas escenas pueden fallar: se informa cada error en `catalog.json`. No se han ejecutado pruebas end-to-end dentro del editor de Godot.
