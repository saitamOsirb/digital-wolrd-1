# Entrega integrada de recuperación visual — v0.8.0

Esta entrega sustituye varios pasos manuales por un **pipeline único de previsualización TMD + TIM → Godot 4**, para trabajar con datos extraídos localmente de una copia legítima de Digimon World 1.

## Comando

```powershell
cd D:\developer\digital-wolrd-1
python tools-python/build_godot_character_preview.py ".local-assets/modelo.bin" --tim ".local-assets/textura.tim" --offset 0x0 --output "client-godot/assets/characters/preview"
```

Luego abre `client-godot/project.godot`, selecciona `res://scenes/tmd_textured_preview.tscn` y presiona **F6**.

El pipeline inspecciona los paquetes texturizados FT3/FT4 admitidos, carga los TIM suministrados a la VRAM experimental, separa por TPAGE/CLUT y genera `model.json` más los PNG necesarios. La nueva escena Godot construye triángulos con UV y texturas nearest-neighbor, conservando el punto de inspección independiente del visor de File City.

## Limitaciones que impiden afirmar que el juego está terminado

**No se dispone en el repositorio de un modelo del protagonista identificado y validado**, ni de los archivos originales de animación y su especificación completa. Por eso, este pipeline no recupera automáticamente su identidad, jerarquía de huesos, animaciones, texturas auténticas en orden exacto de carga ni el comportamiento de cámara y colisiones de DW1. Los archivos comercialmente protegidos no se suben a GitHub.

Para llegar a la demo auténtica quedan pasos que requieren los **datos originales concretos**: localizar los buffers del protagonista y clips de movimiento; completar variantes TMD/MMD/MTN que se usen realmente; comprobar cargas TIM de VRAM; calibrar geometría y renderizado del héroe con el fondo y cámara; incorporar el controlador de movimiento y animaciones a File City. No puede verificarse ni considerarse completado sin esos recursos.

**Estado de validación:** cambios publicados en código fuente; pruebas integradas de Godot y uso con datos del juego todavía pendientes.
