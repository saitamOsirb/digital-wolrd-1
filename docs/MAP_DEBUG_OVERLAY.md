# Superposición de depuración de escenarios — 0.5.9

El visualizador de Godot permite activar con **V** una capa de diagnóstico sobre el fondo original del escenario. Dibuja en rojo los polígonos definidos en `client-godot/assets/maps/walk_zones.json` y en verde las áreas rectangulares de `client-godot/assets/maps/transitions.json`.

La superposición se reconstruye al cambiar de mapa y comparte exactamente la misma transformación de escala y posición del fondo importado. El dibujo es únicamente una herramienta visual: no modifica el PNG original, no añade colisiones ni implica que estos polígonos se hayan extraído de los datos auténticos de PlayStation.

Otros controles: **C** alterna la aplicación de zonas bloqueadas, **F** alterna seguimiento, **PageUp/PageDown** cambia de mapa, **F5** guarda la sesión, **F9** la restaura. Los atajos se utilizan en la ventana del juego.

Esta entrega queda pendiente de validación ejecutando Godot 4. El siguiente trabajo prioritario sigue siendo reemplazar estas zonas manuales por datos originales, extraer el protagonista y calibrar cámara/profundidad.
