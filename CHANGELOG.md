# Changelog

## 0.3.2 — 2026-10-12
- Añadido analizador Python de estructura preliminar TFS según `MAIN_func_800D634C` de `dw_decomp`.
- Identificado desplazamiento de 512 bytes por CLUT y bloque de 16.384 bytes por tile no vacío, más encabezado de 4 bytes.
- Añadidas pruebas sintéticas de offsets y validación de archivos incompletos.
- Documentadas las incertidumbres del formato y la dependencia de la metadata MAP_TILES.
- Se mantienen exclusivamente Godot/GDScript, C# y Python.

## 0.3.1 — 2026-10-12
- Integración diagnóstica de texturas PNG en escena Godot mediante GDScript, sin agregar TypeScript.
- Generador Python de textura TIM sintética de 16 bits y conversión a PNG.
- Pruebas unitarias del fixture y documentación del flujo Python → Godot.
- Los recursos del juego original, el escenario de File City y la fidelidad visual siguen pendientes de importación.

## 0.3.0 — 2026-10-12
- Limpieza completa del árbol de trabajo: eliminado el prototipo TypeScript, Vite, Node.js y sus archivos asociados.
- Arquitectura única: cliente Godot en GDScript, backend C# y herramientas Python.
- Reescritas README, arquitectura, roadmap y documentación de recursos para reflejar el stack oficial.
- Conservados los scripts Godot, servidor C# y herramientas Python, junto con su historial en Git.

## 0.2.3 — 2026-10-12
- Decodificador TIM 4/8/16/24 bits en Python y exportación a PNG.
- Pruebas sintéticas y documentación del formato.

## 0.2.2 — 2026-10-12
- Generador Python de colisiones sintéticas para Godot.

## 0.2.1 — 2026-10-12
- Cargador Godot de colisiones JSON.

## 0.2.0 — 2026-10-12
- Inicio de Godot/GDScript, C# y herramientas Python.
