# Vista previa de animaciones del protagonista — v0.6.3

Se añadió soporte para **una hoja de sprites local y opcional** sobre los fondos originales de DW1. No se ha descifrado todavía el modelo 3D del protagonista de PlayStation: este paso prepara el controlador visual del personaje sin inventar ni publicar recursos originales.

Coloca `client-godot/assets/characters/tamer_walk.png` (PNG RGBA). La hoja debe contener exactamente 4 columnas de frames y 4 filas de direcciones: abajo, izquierda, derecha, arriba. Cada celda ha de tener idénticas dimensiones y mantener los pies anclados en el mismo punto. El renderizador utiliza filtrado nearest-neighbor y sitúa la imagen desde los pies sobre la posición del marcador.

Al caminar por teclado o clic derecho, el controlador cambia dirección y frame (8 cuadros/segundo). Al detenerse vuelve al primer frame. Sin PNG local se mantiene el marcador de diagnóstico anterior, por lo que el proyecto no depende de assets descargados de terceros. La carpeta `assets/characters/` debe mantenerse excluida de Git si se usan recursos de una copia comercial.

**Importante:** esto es una previsualización de un sprite 2D opcional, no el modelo ni la animación originales de PlayStation. Faltan extracción de modelo 3D, rig, texturas, clips, iluminación, cámara y colisiones auténticas. Todavía no se ha validado la ejecución en Godot 4.
