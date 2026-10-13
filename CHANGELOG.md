# Changelog

## 0.7.9 — 2026-10-12
- Herramienta Python que exporta por lotes todas las combinaciones TPAGE/CLUT de caras TMD FT3/FT4 compatibles.
- Para cada combinación genera PNG de VRAM, malla OBJ con UV y material MTL; incluye manifest.json de grupos y paquetes omitidos.
- Pruebas sintéticas de generación de artefactos y rechazo de modelos sin caras texturizadas reconocibles.
- Sigue pendiente comprobar recursos auténticos del protagonista, formatos de animación e integración del modelo en File City.

## 0.7.8 — 2026-10-12
- Exportador experimental OBJ/MTL texturizado para caras FT3/FT4 extraídas de TMD, usando UV y página PNG VRAM.
- Filtro estricto por TPAGE+CLUT y coordenadas UV normalizadas por página de 256×256.
- Pruebas sintéticas de exportación, selección de página y comprobación de índices, más documentación del flujo de importación.
- El protagonista original no está todavía reconstruido ni integrado en File City; pruebas con recursos reales y Godot pendientes.

## 0.7.7 — 2026-10-12
- Exportador PNG de páginas de textura GPU PS1 de 256×256 utilizando los TIM cargados en VRAM local.
- Muestreo de 4/8/16 bpp por TPAGE/CLUT/UV y CLI para importar varios TIM en orden.
- Pruebas sintéticas de contenido PNG y rechazo de profundidad de textura inválida.
- Sigue pendiente verificar la secuencia de TIM reales y conectar los materiales texturizados con las mallas en Godot.

## 0.7.6 — 2026-10-12
- Memoria VRAM PS1 experimental (1024×512 palabras de 16 bits) con carga de bloques TIM y CLUT en coordenadas originales.
- Muestreo de texeles de 4, 8 y 16 bpp mediante TPAGE, CLUT y UV, entregando RGBA para futuros materiales.
- Pruebas sintéticas de color, paletas y validación de límites y documentación de la nueva API.
- Pendientes de validación: cargas reales de texturas del protagonista, modo de blending, asociación de UV a mallas y ejecución en Godot.

## 0.7.5 — 2026-10-12
- Decodificación de campos TPAGE y CLUT del GPU PlayStation a coordenadas de páginas de textura, profundidad de color y posición de paleta.
- Anotación de informes UV experimentales TMD con metadatos GPU para preparar la reconstrucción de VRAM.
- Pruebas sintéticas de decodificación de bitfields y validación de valores fuera de rango.
- No se extraen todavía las texturas ni el protagonista real; conversión de TIM a VRAM y validación integrada pendientes.

## 0.7.4 — 2026-10-12
- Inspector Python experimental de primitivas TMD texturizadas sin iluminación (FT3/FT4).
- Extracción de UV crudas, CLUT, TPAGE, color e índices de vértices; modos no compatibles registrados sin inventar geometría.
- Pruebas sintéticas de triángulos, cuadriláteros, banderas no admitidas y buffers truncados.
- Documentación sobre el espacio VRAM y la recuperación pendiente de texturas, protagonista 3D y animaciones; integración Godot sin validar.

## 0.7.3 — 2026-10-12
- Exportación Wavefront OBJ/MTL de las superficies experimentales TMD previamente decodificadas, para inspección en Blender y Godot.
- Materiales planos derivados de RGB, objetos separados, cambio de eje y orientación de caras, con validación de índices.
- Pruebas sintéticas de formatos, caras y materiales y documentación de flujo de conversión local.
- Sigue pendiente identificar y recuperar el modelo completo del protagonista, sus UV, texturas y animaciones; validación integrada pendiente.

## 0.7.2 — 2026-10-12
- Exportador experimental de caras TMD planas sin textura: triángulos y cuadriláteros de paquetes sin iluminación compatibles.
- Escena Godot independiente que construye triángulos 3D coloreados desde JSON importado localmente.
- Validación de índices y registro de paquetes no compatibles sin inventar geometría; pruebas con fixtures sintéticos.
- Documentado que todavía no está identificado ni extraído el protagonista 3D ni recuperadas sus texturas y animaciones.
- La ejecución en Godot sigue pendiente de validación.

## 0.7.1 — 2026-10-12
- Inspector Python de paquetes de primitivas TMD: recorre registros y clasifica modos comunes de triángulos y cuadriláteros.
- Validación de límites y longitudes sin fabricar caras ni UV no verificadas.
- CLI para exportar un informe JSON local y pruebas con estructuras sintéticas.
- Documentación sobre límites de la interpretación, pendiente de muestras reales y pruebas integradas en Godot.

## 0.7.0 — 2026-10-12
- Primer conversor estructural TMD a nube de vértices 3D en JSON, con verificación de punteros relativos y límites.
- Escena Godot GDScript para previsualizar vértices importados de forma local, separada del visualizador de escenarios.
- Pruebas sintéticas de lectura de vértices y validación de binarios incompletos.
- Documentación para localizar TMD candidatos y cargar la vista 3D.
- Esta fase NO reconstruye caras, texturas, esqueleto ni animaciones; la identidad del modelo original sigue por comprobar.
- Pruebas integradas Godot pendientes.

## 0.6.5 — 2026-10-12
- Analizador de encabezados candidatos TMD de PlayStation en recursos binarios extraídos localmente.
- Contraste con referencias `CHDAT/TMD0`, `CHDAT/MTN0`, `CHDAT/MMD0` y `TAMER_MODEL_BUFFER` del código descompilado.
- Pruebas sintéticas de estructuras TMD, detección de offsets y rechazo de cabeceras inválidas.
- Documentación de flujo de investigación; la extracción/interpretación del protagonista 3D original aún no está resuelta.

## 0.6.4 — 2026-10-12
- Inventario Python de archivos PS1 orientado a identificar posibles recursos de personajes, modelos, texturas y animaciones.
- Informe JSON local con extensiones y rutas candidatas, sin exportar recursos gráficos protegidos.
- Pruebas unitarias sintéticas de clasificación de archivos y documentación del alcance.
- Este inventario no extrae el modelo del protagonista; la identificación binaria auténtica y conversión a Godot siguen pendientes.

## 0.6.3 — 2026-10-12
- Controlador GDScript para visualizar una hoja local opcional de animación 2D del protagonista sobre fondos originales.
- Direcciones abajo/izquierda/derecha/arriba, 4 frames por dirección y cambio a pose de reposo al detenerse.
- Integración con movimiento por teclado y navegación por clic derecho; se conserva el marcador cuando faltan sprites.
- Protección de recursos locales del personaje en `.gitignore` y documentación de formato y limitaciones.
- La extracción del modelo/animaciones 3D originales de PS1 sigue pendiente; ejecución en Godot no validada.

## 0.6.2 — 2026-10-12
- Soporte de capas de primer plano transparentes por escenario en Godot, por encima del marcador diagnóstico.
- Carga local de PNG RGBA según el identificador del mapa, con comprobación de dimensiones y filtrado nearest-neighbor.
- Se conserva la escala y desplazamiento del fondo sin publicar recursos comerciales en Git.
- Las máscaras son opcionales y manuales; no se han extraído las oclusiones originales del juego. Pendiente verificar ejecución Godot.

## 0.6.1 — 2026-10-12
- Navegación por clic derecho en fondos originales: cálculo de rutas con `AStarGrid2D` sobre celdas de 16 píxeles.
- Celdas bloqueadas basadas en los polígonos locales configurables, con trazado de la ruta en la superposición de depuración.
- Desplazamiento progresivo del marcador por la ruta y cancelación al usar WASD/flechas o cambiar de mapa.
- Documentadas las limitaciones: navegación provisional 2D, no es el pathfinding auténtico de PlayStation.
- Cambios pendientes de validación en ejecución con Godot 4.

## 0.6.0 — 2026-10-12
- Editor de zonas bloqueadas directamente sobre el fondo original importado en Godot: E para editar, clic para vértices, Enter para guardar.
- Edición de polígonos con Backspace para deshacer vértices y Esc para cancelar el polígono en curso.
- Persistencia por mapa en `walk_zones.json`, preservando los polígonos creados en otros escenarios.
- Superposición diagnóstica en el visualizador y documentación del flujo de autoría.
- Esta herramienta manual no equivale a colisiones originales de PS1; pendiente ejecutar y validar en Godot.

## 0.5.9 — 2026-10-12
- Capa visual de depuración de polígonos bloqueados (rojo) y zonas de transición (verde) sobre el fondo PS1 importado.
- Atajo V para mostrar/ocultar áreas, manteniendo zoom, desplazamiento y cambio de escenario.
- La superposición reutiliza las zonas configurables locales sin alterar las imágenes originales.
- Pendiente ejecutar y validar el cliente Godot; estos polígonos no constituyen colisiones auténticas del juego.

## 0.5.8 — 2026-10-12
- Guardado local de exploración desde Godot: mapa seleccionado, posición del marcador, seguimiento y zoom.
- Recuperación al iniciar el visualizador y atajos F5/F9 para guardar/restaurar.
- Validación de formato y valores del guardado para evitar restaurar coordenadas corruptas.
- Sin cambios al backend C# ni distribución de recursos gráficos comerciales.
- La exploración continúa siendo diagnóstica, no una recreación jugable fiel del original; pendiente de pruebas en Godot.

## 0.5.7 — 2026-10-12
- Transiciones configurables entre escenarios originales ya importados, mediante zonas rectangulares y puntos de aparición.
- Carga de `assets/maps/transitions.json` por mapa y cambio automático de fondo al entrar en una zona.
- Protección básica contra ciclos inmediatos y aviso cuando el mapa destino no está importado.
- Documentación de configuración; estas transiciones son provisionales y no equivalen a los warps PS1 originales.
- Pendiente validación ejecutando Godot, extracción de transiciones originales y protagonista 3D.

## 0.5.6 — 2026-10-12
- Sistema optativo de polígonos bloqueados por escenario, definidos en un JSON local en coordenadas de imagen.
- Marcador de exploración con rechazo de movimientos dentro de áreas bloqueadas y deslizamiento aproximado por eje.
- Atajo C para activar/desactivar estas zonas y cambio automático de configuración al seleccionar otro mapa.
- Documentación sobre el formato y límites de esta capa auxiliar: no sustituye colisiones originales de PS1.
- Godot continúa pendiente de validación ejecutable; no se modificó el servidor C#.

## 0.5.5 — 2026-10-12
- Conversión por lotes de los fondos TFS originales desde la copia local de PlayStation a PNG, con catálogo JSON.
- Navegación por mapas importados dentro del visor GDScript mediante PageUp/PageDown.
- Conservada la compatibilidad con el fondo original individual y la inspección de coordenadas.
- Registro explícito de archivos que no pudieron convertirse; pruebas Python del catálogo y validación de parámetros.
- Ignorados los recursos extraídos para evitar su publicación en GitHub.
- Movimiento/calibración original y modelo 3D del protagonista siguen pendientes.

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
