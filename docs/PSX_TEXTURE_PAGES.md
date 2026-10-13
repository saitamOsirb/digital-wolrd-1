# Metadatos de páginas de texturas PlayStation — 0.7.5

La nueva herramienta `tools-python/inspect_psx_texture_pages.py` amplía el inspector UV de modelos TMD con la interpretación de bitfields **TPAGE** y **CLUT** de PlayStation. Convierte las referencias de 16 bits en coordenadas GPU: página X/Y, profundidad nominal de textura (4, 8 o 16 bits por píxel), modo de semitransparencia y posición X/Y de paleta.

```powershell
python tools-python/inspect_tmd_uv.py ".local-assets/modelo.bin" --offset 0x0 --output ".local-assets/modelo-uv.json"
python tools-python/inspect_psx_texture_pages.py ".local-assets/modelo-uv.json" --output ".local-assets/modelo-gpu.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

El TMD de entrada debe extraerse localmente desde una copia del juego del usuario; los ejemplos no señalan al protagonista real. Los campos se agregan a cada cara texturizada del informe JSON. Una profundidad codificada reservada se informa como `0` y no se interpreta como formato válido.

**Límite fundamental:** decodificar direcciones CLUT/TPAGE no equivale a reconstruir texturas. Todavía falta cargar bloques TIM en posiciones de VRAM, asociar paletas y generar atlas/UV normalizadas para Godot. Tampoco se ha identificado de manera inequívoca el modelo del protagonista ni convertido sus animaciones. Las pruebas de integración permanecen pendientes.
