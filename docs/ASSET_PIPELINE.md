# Importación de recursos originales: investigación y contrato 0.1.1

## Lo confirmado en las fuentes
- `dw_decomp/src/main/map.c`, `map_collision.c`, `model.c`, `anim.c` son puntos concretos para investigar formatos y carga.
- `DW1-Code/checkMapCollision.asm` documenta consultas de colisión por eje.
- `DW1-Code/entityMoveForward.asm` registra movimiento sobre ejes X/Z con matrices de rotación.
- El archivo `renderCharacter.asm` **renderiza glifos/texto**, NO el protagonista; no usarlo como fuente del modelo 3D.
- `DWDDRandomizer` trabaja con Dawn/Dusk (NDS), no con los recursos de DW1 (PS1).

## Contrato de escena temporal
`public/scenes/file-city-prototype.json` usa `schemaVersion: 1`, `id`, `name`, `source`, `bounds`, `spawn`, `collision` y `decorations`.
Las coordenadas son 2D en unidades internas de la demo; **no equivalen a coordenadas extraídas de DW1**.

El cliente valida dimensiones, colisiones, ubicación de spawn y límites antes de activar la escena. Los assets actuales son sintéticos y no representan la topología real de File City.

## Siguiente investigación
1. Identificar el contenedor de cada zona, listas de geometría, UV, texturas y paletas.
2. Determinar la escala, orientación y matriz de cámara original; documentar valores medidos.
3. Crear un importador local que consuma solo recursos aportados por el usuario.
4. Exportar un formato intermedio con geometría, materiales, colisiones y triggers, y validar contra fixtures.
5. Implementar render 3D web y animación del protagonista; no simular fidelidad con mapas de bloques.
6. Asegurar que ninguno de los recursos originales se suba a GitHub ni se sirva automáticamente desde el repositorio.

Limitación: hasta disponer de archivos originales extraídos legalmente, la geometría real no puede comprobarse.
