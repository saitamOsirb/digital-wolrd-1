# Zonas de caminata opcionales — versión 0.5.6

Se añadió un sistema de **polígonos bloqueados por mapa** para preparar la exploración interactiva sobre fondos originales. Las posiciones se expresan en píxeles de la imagen del mapa importado. Esta capa es **configuración manual auxiliar**, no colisiones extraídas del juego de PlayStation.

## Archivo local

Crea `client-godot/assets/maps/walk_zones.json` con la siguiente estructura de ejemplo (coordenadas ilustrativas, no corresponden a obstáculos reales):

```json
{
  "TWNA01": [
    [[100, 100], [170, 100], [170, 150], [100, 150]]
  ],
  "TWNB01": []
}
```

El cargador valida los vértices y acepta polígonos de tres o más puntos. El visor bloquea los movimientos cuyo destino termina dentro de un polígono, con intento de deslizamiento horizontal o vertical cuando existe un obstáculo. **No hay detección continua de barrido ni colisiones tridimensionales**, por lo que movimientos rápidos pueden atravesar polígonos muy delgados.

## Controles

- WASD/flechas: mover marcador diagnóstico.
- Shift+clic: posicionar el marcador, respetando zonas bloqueadas.
- C: activar/desactivar zonas bloqueadas.
- F: seguimiento; R: encuadrar; PageUp/PageDown: cambiar fondo.

Al no existir archivo de zonas, el comportamiento es como en la versión anterior. La carpeta `assets/maps` es local y está ignorada por Git.

## Siguientes etapas

Convertir la colisión real de archivos MAP y calibrar la proyección y escala para integrar modelos originales de jugador y NPC. No se debe llamar a estos polígonos «colisiones originales» hasta decodificar y verificar los datos reales.
