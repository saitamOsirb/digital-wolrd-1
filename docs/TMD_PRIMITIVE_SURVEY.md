# Inspección de primitivas TMD — 0.7.1

Este avance agrega `tools-python/inspect_tmd_primitives.py` para examinar, **sin inventar polígonos**, los registros de primitivas de modelos TMD con punteros relativos. Recorre paquetes según su longitud, identifica modos habituales de triángulos y cuadriláteros no texturizados y registra los que aún no se interpretan.

```powershell
python tools-python/inspect_tmd_primitives.py ".local-assets/modelo.bin" --offset 0x0 --output ".local-assets/primitive-report.json"
python -m unittest discover -s tools-python -p "test_*.py"
```

El archivo y su offset deben proceder de un recurso realmente identificado en la copia original del usuario. **La herramienta no exporta caras válidas ni modelos texturizados**: todavía tenemos que contrastar el formato exacto de los índices con datos originales antes de generar triangulación para Godot. Se rechazan buffers truncados y paquetes de longitud inválida.

No se publican archivos de juego en GitHub; solo herramientas y pruebas sobre datos sintéticos. Pruebas de integración pendientes.
