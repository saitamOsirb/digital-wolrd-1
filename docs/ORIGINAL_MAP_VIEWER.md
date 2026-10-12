# Visualizador de mapa auténtico — v0.5.1

El cliente Godot abre ahora una escena independiente 2D diseñada para **inspeccionar el PNG extraído del juego**, sin alterar el color con luces, proyectarlo en un suelo 3D ni mezclarlo con el mapa de prueba.

## Preparación en Windows
1. Descomprimir el archivo `Digimon World (USA).7z` localmente con 7-Zip.
2. Desde la raíz del repositorio:

```powershell
python tools-python/import_original_map.py "D:\\ruta\\Digimon World (USA).bin" --map TWNA01
```

3. Importar `client-godot/project.godot` en Godot 4 y pulsar **F5**.

Se visualizará `client-godot/assets/demo/map.png` con ajuste de encuadre a ventana y filtrado nearest-neighbor. Si falta el PNG, la interfaz muestra instrucciones de importación **en vez de generar un mapa sintético**.

**Controles:** rueda del ratón para zoom alrededor del cursor; botón izquierdo y arrastrar para mover; R para volver a encuadrar.

La escena anterior 3D `res://scenes/world.tscn` se conserva para investigar movimiento, cámara y colisiones. Solo la escena inicial cambia: ahora es `res://scenes/original_map_viewer.tscn`.

## Limitaciones
El visualizador muestra exclusivamente el fondo estático original. Todavía no reproduce cámara/proyección de PS1, profundidad, overlays, tamer 3D ni colisiones exactas, y no constituye una demo jugable original. El PNG convertido se mantiene fuera de GitHub.

Godot y .NET no están disponibles en el entorno donde se preparó esta entrega, por lo que la ejecución de la escena en el editor todavía debe validarse.

## Navegación de coordenadas (0.5.2)
El visor muestra ahora un **marcador temporal** sobre el fondo gráfico importado y sus coordenadas en píxeles. WASD o flechas mueven el marcador; Shift + clic lo posiciona en un punto del fondo; F activa/desactiva que el mapa siga el marcador; R recupera el encuadre. Se mantiene el arrastre con mouse y zoom mediante rueda.

Estas posiciones **NO son coordenadas del mundo PS1** y no tienen aún colisiones, perspectiva ni modelo original del protagonista. Es una herramienta de calibración para preparar la transformación 3D→2D con datos originales. El fondo no se altera.
