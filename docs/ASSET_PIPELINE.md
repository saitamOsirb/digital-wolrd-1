# Pipeline de recursos: Python → Godot

Fuentes de investigación: `dw_decomp/src/main/map.c`, `map_collision.c`, `model.c`, `anim.c` y rutinas correspondientes de `DW1-Code`.

Las herramientas Python en `tools-python/` reciben datos que el usuario tiene derecho a utilizar. Actualmente:
- `import_collision.py` convierte una matriz aislada de 10.000 bytes a JSON diagnóstico.
- `convert_tim.py` convierte un TIM aislado a PNG.
- `inspect_map_offsets.py` inspecciona una tabla de offsets de un archivo de mapa previamente aislado.
- `generate_demo_collision.py` produce colisiones sintéticas para comprobar la carga en Godot.

El cliente GDScript consume `res://assets/diagnostic/collision.json` si existe. Los archivos generados con recursos de terceros no deben incluirse en el repositorio. Los mapas, modelos y texturas auténticos requieren investigación y validación adicionales.

No se utilizará TypeScript, Vite ni renderizado web personalizado.
