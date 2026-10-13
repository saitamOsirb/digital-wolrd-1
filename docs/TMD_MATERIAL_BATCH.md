# Exportación por lotes de materiales TMD — v0.7.9

Se incorpora `tools-python/build_tmd_materials.py`, que unifica los convertidores experimentales anteriores para exportar **todas las combinaciones TPAGE + CLUT encontradas** dentro de un modelo TMD compatible. Por cada grupo genera una página PNG de 256×256, un OBJ con UV y un MTL. También genera `manifest.json` con rutas, recuentos y paquetes no admitidos.

## Uso local

```powershell
python tools-python/build_tmd_materials.py ".local-assets/modelo.bin" --tim ".local-assets/textura-a.tim" ".local-assets/textura-b.tim" --offset 0x0 --output ".local-assets/modelo-materiales"
```

Los archivos TIM se cargan en orden a VRAM, por lo que **debes conocer la secuencia correcta** para evitar resultados incorrectos. Los ejemplos son nombres ficticios: el sistema aún no ha identificado ni extraído el modelo auténtico del protagonista. El directorio de salida recibe `manifest.json` y archivos `page_TPAGE_CLUT.obj/.mtl/.png`. Cada OBJ agrupa solo las caras de su correspondiente combinación de página y paleta.

El proceso interpreta únicamente primitivas FT3/FT4 sin iluminación admitidas por el inspector anterior; omite los demás modos y documenta sus cantidades. No reconstruye rig, huesos, animaciones, todas las caras del modelo ni asigna modelos automáticamente en File City. Los PNG dependen del contenido local de la copia del usuario, nunca se suben al repositorio.

Pruebas de ejecución en Godot y con contenido original: **pendientes**.
