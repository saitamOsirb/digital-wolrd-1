# Guardado de la sesión de exploración — 0.5.8

El visualizador de fondos originales permite guardar la sesión localmente con **F5** y recuperarla con **F9**; también intenta recuperar la última sesión guardada al abrir la escena. El archivo se almacena en `user://exploration_save.json` mediante el API de Godot (no se incluye en el repositorio).

Se conservan: identificador del mapa importado, posición del marcador diagnóstico expresada en píxeles, zoom y modo de seguimiento. Si el mapa ya no figura en el catálogo, el visor conserva el mapa que esté cargado. Los datos malformados se ignoran.

**Importante:** este sistema no es un sistema de partidas de Digimon World: no guarda mascotas, inventario ni estado del juego. El marcador sigue siendo provisional y las colisiones y transiciones originales están pendientes de extracción y calibración.

El editor Godot y el cliente en ejecución pueden tener usos distintos de F5; los atajos indicados se refieren a la ventana del juego, no a la del editor. Esta entrega aún no ha sido verificada ejecutando Godot.
