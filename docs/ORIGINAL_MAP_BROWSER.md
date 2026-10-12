# Explorar escenarios originales — v0.5.4

El visor Godot ahora muestra el identificador del mapa cargado desde `map.json`, en lugar de asumir que siempre es TWNA01. Los mapas son fondos de PlayStation obtenidos de archivos TFS; el indicador que se mueve es diagnóstico, no el protagonista original.

## Encontrar todos los TFS del disco
Extrae localmente el BIN de tu copia y ejecuta desde la raíz:

```powershell
python tools-python/list_disc_maps.py "D:\\ruta\\Digimon World (USA).bin" --output ".local-assets/tfs-index.json"
```

Este comando lista las rutas internas y tamaños, sin copiar los recursos.

## Importar un escenario específico
```powershell
python tools-python/import_disc_tfs.py "D:\\ruta\\Digimon World (USA).bin" "MAP/MAP14/TWNA01.TFS"
```

Para otro escenario, reemplazar la ruta interna por una de las encontradas. El archivo `client-godot/assets/demo/map.png` será reemplazado por el nuevo fondo y `map.json` por su metadato. **No modificar archivos originales ni subir datos extraídos a GitHub**.

Abrir `client-godot/project.godot` y pulsar F5 para visualizarlo. Si Godot ya estaba abierto, reiniciar la escena.

```powershell
python -m unittest discover -s tools-python -p "test_*.py"
```

## Limitaciones
- El renderizador TFS actual asume un orden de tiles secuencial y puede no reconstruir correctamente escenas que incluyen entradas vacías u otros formatos. Verificar visualmente cada exportación.
- Esta etapa añade exploración por archivos TFS, no cámara PS1, objetos delante/detrás de personajes, interacción ni movimiento auténtico.
- Las rutas generadas se mantienen bajo una carpeta ignorada por Git.
