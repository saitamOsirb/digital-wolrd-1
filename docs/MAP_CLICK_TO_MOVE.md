# Navegación por clic sobre fondos originales — v0.6.1

Se incorporó movimiento de diagnóstico al hacer **clic derecho** sobre una posición del fondo original importado. `map_pathfinding.gd` emplea `AStarGrid2D` en una cuadrícula de **16 píxeles** para buscar una ruta entre el marcador y la posición señalada. Los polígonos bloqueados definidos manualmente en `walk_zones.json` se rasterizan como celdas no transitables.

La ruta calculada se visualiza en azul al activar la capa de depuración con **V**. El marcador sigue el camino sin teletransportarse. WASD/flechas cancelan la ruta manualmente y dan prioridad al control directo. Los cambios de escenario también cancelan la ruta vigente.

**Límites:** este algoritmo es 2D y provisional, no reproduce el pathfinding de PlayStation. En espacios estrechos, una cuadrícula de 16 píxeles puede producir pasos que no respeten exactamente el contorno de un polígono; se requiere mejorar la precisión y comprobar la ruta real antes de usarlo con personajes auténticos. La compatibilidad de esta entrega con Godot 4 todavía no se ha validado en ejecución. Los PNG originales no se publican en GitHub.
