# Changelog

## 0.2.3 — 2026-10-12
- Primer decodificador de texturas PlayStation TIM en Python (4/8/16/24 bpp, CLUT).
- Conversión local de TIM a PNG RGBA sin dependencias externas.
- Pruebas con datos sintéticos para los cuatro modos, validación de errores y formato PNG.
- Documentada la semitransparencia PS1 y las limitaciones del importador; no se incluyen texturas comerciales.
- Todavía no existe extracción de contenedores de mapa ni renderización de File City auténtico.

## 0.2.2 — 2026-10-12
- Generador Python de un fixture sintético 100×100 para visualizar las colisiones en Godot.
- Uso: `python tools-python/generate_demo_collision.py`.
- El escenario real de File City sigue pendiente.


## 0.2.1 — 2026-10-12
- Se añadió un cargador Godot para obstáculos rectangulares provenientes de JSON de diagnóstico.
- Se integró opcionalmente en la escena principal, preservando el mapa sintético anterior como fallback.
- Se requiere un JSON local válido para activar la visualización; aún no representa File City.
- No se verificó ejecución en Godot.

## 0.2.0 — 2026-10-12
- Arquitectura oficializada: Godot 4/GDScript para cliente, C# ASP.NET Core para servidor, Python para herramientas.
- Añadida escena Godot 3D sintética para validar movimiento, cámara, gravedad y colisión.
- Añadido servicio C# de salud y WebSocket de diagnóstico (NO multijugador completo).
- Añadido importador Python de matriz de colisiones DW1 100×100 y tests.
- Preservado prototipo anterior de TypeScript sin revertir cambios.

## 0.1.1 — 2026-10-12
- Separada definición del escenario de la simulación y del cliente mediante JSON con validación estricta.
- Cámara limitada a los márgenes de cada escenario, incluso con viewport más grande que el mapa.
- Renderizado de capas sintéticas de un escenario y animación provisional de movimiento.
- Pruebas de carga de escenas, spawn, colisiones y cámara.

## 0.1.0 — 2026-10-12
- Inicialización del cliente web en TypeScript.
- Primera escena de exploración con cámara, movimiento y colisiones.
