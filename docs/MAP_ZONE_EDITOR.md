# Editor de polígonos de colisión sobre mapas — versión 0.6.0

Esta entrega incorpora una herramienta interactiva en Godot para dibujar las zonas bloqueadas sobre **fondos originales importados** de Digimon World 1. Los polígonos se guardan de forma local y por escenario; **no constituyen datos de colisión originales**.

## Uso

1. Convertir los fondos del disco local con `python tools-python/import_all_maps.py "D:\\ruta\\Digimon World (USA).bin" --limit 20`.
2. Abrir `client-godot/project.godot` y ejecutar la escena principal.
3. Pulsar **E** para activar la edición, luego **clic izquierdo** para añadir vértices de un obstáculo en coordenadas de la imagen.
4. Pulsar **Enter** con tres o más vértices para finalizar el polígono y guardarlo. **Retroceso** quita el último vértice; **Esc** descarta el polígono sin finalizar; **E** cierra el editor.
5. Pulsar **V** para mostrar/ocultar la superposición. **C** activa/desactiva el uso de las zonas bloqueadas durante el movimiento.

Los datos se almacenan en `client-godot/assets/maps/walk_zones.json`, carpeta ignorada por Git. Se preservan las zonas de los otros mapas. No se publican recursos ni datos extraídos de la copia comercial del usuario.

## Advertencias

Se trata de una herramienta de **autoría provisional**. Las coordenadas se corresponden con el PNG de fondo cargado, no con la geometría ni el motor de colisiones de PlayStation. Las zonas no están rellenadas automáticamente; es necesario dibujarlas. No incluye borrado de polígonos anteriores, ni validación avanzada de autointersecciones. El editor aún no ha sido probado ejecutando Godot; estas limitaciones se abordarán durante la fase de pruebas y correcciones.
