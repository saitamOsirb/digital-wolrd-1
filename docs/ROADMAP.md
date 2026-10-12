# Roadmap técnico

## Etapa 1 — Vertical slice (0.1.0)
- [x] Canvas de prueba de exploración.
- [x] Mover avatar y cámara; resolver colisiones de obstáculos.
- [x] Separar estado/simulación de la presentación.
- [ ] Importar un mapa real con su geometría y texturas (dependiente de extractor).
- [ ] Importar el modelo original del protagonista y sus animaciones.
- [ ] Validar orientación, cámara y límites contra emulador.

## Etapa 2 — Fidelidad gráfica
Estudiar formato de escenarios, geometría PS1, texturas y animaciones; crear convertidores offline con fixtures sintéticos para CI. Probar WebGL2/WebGPU para escenas 3D (no convertir prematuramente los fondos en tiles 2D). Aplicar oclusión y profundidad reales.

## Etapa 3 — Comportamiento
Control y movimiento canónicos, seguidor, transiciones de zona, triggers y NPC. Pruebas de regresión de colisiones y navegación.

## Etapa 4 — Online
Servidor TypeScript con estado autoritativo, instancias de mapa, sincronización de posiciones, autenticación y persistencia.

**Nota de investigación:** `dw_decomp` y `DW1-Code` corresponden a DW1; `DWDDRandomizer` es para Dawn/Dusk de NDS, por lo que sus datos no corresponden a los escenarios PS1.
