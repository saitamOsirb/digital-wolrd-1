# Investigación de UV de PlayStation TMD — v0.7.4

El nuevo script `tools-python/inspect_tmd_uv.py` inspecciona **experimentalmente** primitivas texturizadas sin iluminación de un TMD estándar con punteros relativos. Admite paquetes candidatos FT3 (`0x24`) y FT4 (`0x2C`) con bandera de no iluminación igual a 1. Exporta índices, coordenadas UV de 8 bits, CLUT, TPAGE y RGB del paquete; los modos restantes quedan cuantificados sin inventar información.

```powershell
python tools-python/inspect_tmd_uv.py ".local-assets/modelo.bin" --offset 0x0 --output ".local-assets/modelo-uv.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

Los archivos de entrada deben proceder de una extracción local autorizada, y se requiere comprobar su estructura real contra el código descompilado y los recursos originales. Las UV son **coordenadas crudas de PlayStation**: todavía no representan UV normalizadas listas para un material de Godot. Las referencias CLUT/TPAGE tampoco son imágenes; falta reconstruir el espacio VRAM y aplicar las paletas para obtener texturas.

**Estado:** etapa de investigación; no se ha confirmado el modelo original del protagonista, ni se han cargado texturas auténticas. Las pruebas integradas permanecen pendientes. No se distribuye contenido comercial.
