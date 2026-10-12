# Changelog

## 0.5.4 — 2026-10-12
- Indexador Python de archivos TFS originales dentro de un BIN PS1 local, sin distribuir sus recursos.
- Importador de cualquier ruta TFS encontrada en el disco a `map.png` y `map.json` para Godot.
- El visualizador GDScript muestra el identificador del mapa importado, sin asumir siempre TWNA01.
- Pruebas Python de validación de rutas y documentación de uso.
- No se ha verificado la ejecución completa en Godot; modelos 3D, cámara y colisiones originales pendientes.

## 0.5.3 — 2026-10-12
- Nuevo parser Python de metadatos de cámara, distancia de proyección, dimensiones y tiles desde la estructura MAP setup original.
- Extracción local desde la copia PlayStation del usuario y exportación de `map_setup.json`.
- Pruebas unitarias con fixtures binarios para cámara y tabla de tiles.
- Documentado que la correspondencia de coordenadas PS1→Godot aún no está calibrada; se mantiene el visor del mapa original.

## 0.5.2 — 2026-10-12
- Añadido marcador de diagnóstico sobre el fondo original de TWNA01, con coordenadas en píxeles.
- Movimiento de prueba por WASD/flechas, posicionamiento por Shift+clic y seguimiento opcional con F.
- Se mantienen zoom y desplazamiento del visor original, sin añadir escenarios sintéticos ni TypeScript.
- El marcador aún no es el protagonista real; las coordenadas de PS1, colisiones y proyección siguen pendientes.
- No se ha podido comprobar la escena en una ejecución local de Godot.

## 0.5.1 — 2026-10-12
- Añadido visualizador 2D GDScript del mapa real importado de PS1, con zoom, arrastre y encuadre.
- El visualizador es ahora la escena de inicio de Godot; se conserva la prueba 3D anterior.
- Si falta el PNG extraído, se muestran instrucciones; no se genera un mapa sintético en esta pantalla.
- Actualizados README y guía de ejecución. La fidelidad de cámara/personaje, overlays y colisiones originales sigue pendiente.
- Pendiente prueba de ejecución en el editor Godot.

## 0.5.0 — 2026-10-12
- Extraído y decodificado localmente el escenario original `TWNA01.TFS` de File City desde la copia USA aportada por el usuario.
- Nuevo lector Python de ISO9660 desde imágenes PS1 BIN Mode2/2352 y convertidor de TFS a PNG con paletas CLUT.
- Escenario real validado a 768×640 (6×5 tiles de 128×128) y visualizado mediante PNG.
- Godot preserva ahora la proporción de la textura original; no se distribuyen assets comerciales en GitHub.
- Añadidas pruebas sintéticas para el orden de tiles, colores y archivos TFS incompletos.
- Pendientes cámara de PS1, overlays, colisiones originales y modelo/animación del protagonista.

## 0.4.0 — 2026-10-12
- Demo de renderizado de un escenario completo en Godot/GDScript con fondo compuesto por tiles de 128×128.
- Fondo sintético de emergencia generado dentro de Godot para ejecutar F5 sin depender de herramientas externas.
- Herramienta Python para componer una imagen de mapa 512×512 y exportar un PNG/manifest para Godot.
- Conservadas las colisiones 3D y el movimiento del avatar; añadidas pruebas Python de composición.
- Documentación para ejecutar ambas rutas y exclusión de los mapas locales generados de Git.
- **No representa File City real**: la decodificación TFS de contenido comercial continúa pendiente.

## 0.3.3 — 2026-10-12
- Nuevo inspector Python de dimensión y lista de tiles MAP utilizando enteros de 32 bits como en `loadMapSetup`.
- Correlación de tiles no vacíos con bloques candidatos de datos TFS, sin asumir que todos los tiles ocupan payload.
- Pruebas con mapas sintéticos de ocupación dispersa y detección de datos truncados.
- La geometría, texturas y presentación original de File City aún no han sido recuperadas.

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
