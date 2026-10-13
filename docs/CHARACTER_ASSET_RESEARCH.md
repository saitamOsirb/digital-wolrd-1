# Inventario de recursos del protagonista — v0.6.4

Se incorpora la herramienta Python `tools-python/inspect_character_assets.py` para hacer un **inventario exploratorio de archivos del disco PS1**, buscando posibles recursos de modelos, personajes, texturas y animaciones por nombre y extensión.

## Uso
```powershell
python tools-python/inspect_character_assets.py "D:\\ruta\\Digimon World (USA).bin" --output ".local-assets/model-inventory.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

El informe incluye número total de archivos, frecuencias por extensión y rutas cuyos nombres contienen patrones como `MODEL`, `CHAR`, `TAMER`, `ANIM`, `TMD`, `TIM` o `EMD`. **Los resultados son candidatos según su nombre, no modelos confirmados**. Muchos recursos originales pueden estar dentro de contenedores con nombres genéricos y por tanto no aparecerán; también puede haber falsos positivos.

Esta herramienta **no exporta ni convierte la geometría del protagonista**. El próximo trabajo requiere identificar en la copia original los archivos o contenedores correctos y verificar su formato antes de escribir conversores de modelos, texturas, rig y animaciones. Todo recurso del juego permanece local; no se sube al repositorio.

La demo Godot conserva el controlador opcional de sprites 2D anterior. No se ha realizado validación de ejecución en el editor Godot.
