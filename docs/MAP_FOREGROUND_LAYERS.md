# Capas de primer plano sobre mapas originales — versión 0.6.2

Godot admite ahora una **capa PNG RGBA transparente por escenario** encima del marcador de exploración. Permite ensayar la profundidad visual: un personaje puede pasar por detrás de la copa de un árbol o de un elemento frontal mientras el fondo original permanece intacto.

Coloca manualmente la imagen transparente en `client-godot/assets/maps/overlays/TWNA01.png` (sustituye el identificador si corresponde a otro escenario). Sus dimensiones deben coincidir exactamente con `map.png` o el fondo del catálogo; en caso contrario, el visor ignora el overlay y emite una advertencia. La imagen se carga sin filtros de suavizado y sigue el mismo zoom y desplazamiento que el fondo.

**Alcance:** es soporte de renderizado de primer plano, **no** un extractor automático de máscaras de oclusión del juego original. Las capas deben suministrarse localmente. La carpeta `client-godot/assets/maps/` continúa ignorada en Git para no publicar recursos comerciales. El marcador aún es provisional y falta integrar protagonista 3D, profundidad real, animaciones y cámara PS1. Pendiente validar en Godot.
