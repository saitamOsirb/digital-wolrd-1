# Importador gráfico inicial — PS1 TIM

Este primer paso implementa un decodificador Python para texturas **TIM** de PlayStation, con modos de 4, 8, 16 y 24 bits por píxel. Convierte un archivo **TIM ya aislado** (de material aportado localmente por el usuario) en un PNG RGBA sin instalar Pillow.

## Ejemplo
Desde la raíz del repositorio:

```powershell
python tools-python/convert_tim.py ".local-assets/texture.tim" ".local-assets/texture.png"
python tools-python/convert_tim.py ".local-assets/paletted.tim" ".local-assets/paletted-p1.png" --palette 1
python -m unittest discover -s tools-python -p "test_*.py"
```

Los TIM indexados 4bpp/8bpp contienen una o más paletas CLUT. `--palette` elige una paleta, comenzando en 0. El color BGR555 se convierte a RGBA8 y el valor 0x0000 se considera transparente por convención diagnóstica. La semitransparencia STP de PS1 requiere el modo de mezcla del material y aún **no** está representada con fidelidad.

## Límites

- No extrae automáticamente archivos TIM de una ISO, BIN ni contenedores internos de DW1.
- No detecta todavía texturas dentro de archivos empaquetados, ni modela UV, tpage, clut y orden de primitivas del escenario.
- No incluye assets propietarios, ni confirma que los escenarios de DW1 usen TIM autónomos: la descompilación muestra rutinas de carga de imágenes y texturas que deberán verificarse en su contexto.
- No hay integración de estos PNG al escenario Godot todavía.
- En este commit no hay pruebas de ejecución de Godot ni de integración con un mapa real.

El siguiente objetivo es identificar el empaquetamiento y los offsets de los bloques gráficos en `dw_decomp/src/main/map.c`, e inspeccionar `loadMapImage1`, `loadMapImage2` y los formatos de modelo de `model.c`.
