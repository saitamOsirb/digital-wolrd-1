# Exportación de páginas de textura PS1 — v0.7.7

La herramienta `tools-python/render_psx_texture_page.py` genera **una página diagnóstica PNG RGBA de 256×256** a partir de uno o más TIM extraídos localmente. Carga los TIM a la memoria VRAM simulada en orden, aplica TPAGE y CLUT y muestrea los texeles en profundidades de 4, 8 y 16 bpp.

```powershell
python tools-python/render_psx_texture_page.py ".local-assets/textura.tim" --tpage 0x80 --clut 0x0 --output ".local-assets/textura-page.png"
python -m unittest discover -s tools-python -p "test_*.py"
```

Los valores TPAGE y CLUT deben proceder de un paquete del modelo inspeccionado, por ejemplo con `inspect_tmd_uv.py` e `inspect_psx_texture_pages.py`. Se pueden pasar varios TIM antes de los argumentos `--tpage`, `--clut` y `--output`, en el orden en que se desea reconstruir la VRAM.

**Limitaciones:** el resultado puede ser vacío o incorrecto si no se proporcionan todos los TIM o no se conoce el orden auténtico de carga del juego. El PNG de esta etapa es solo una previsualización; no se ha asociado todavía automáticamente a caras del modelo en Godot, no reconstruye STP blending ni se ha identificado el modelo original del protagonista. Las pruebas de ejecución integrada permanecen pendientes. Los archivos comerciales siguen siendo locales y no se publican en GitHub.
