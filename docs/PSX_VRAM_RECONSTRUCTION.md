# Reconstrucción experimental de VRAM PlayStation — v0.7.6

Se incorpora `tools-python/psx_vram.py`, módulo Python que reproduce una superficie local de VRAM PS1 de **1024 × 512 palabras de 16 bits**, recibe bloques de imagen y CLUT del formato TIM en sus coordenadas originales y permite consultar píxeles RGBA con referencias `TPAGE`, `CLUT` y coordenadas UV de 8 bits.

Ofrece `Vram.load_tim(bytes)` para cargar un TIM íntegro, `Vram.upload(x, y, width, height, bytes)` para cargar palabras de forma manual, y `Vram.texel(tpage, clut, u, v)` para consultar texeles indexados de 4/8 bpp o directos de 16 bpp.

Se añadieron pruebas sintéticas para TIM 16 bpp, paleta CLUT 4 bpp, CLUT 8 bpp y límites de memoria. Ejecutar con `python -m unittest discover -s tools-python -p 'test_*.py'` desde la raíz del repositorio.

**Alcance:** no se ha identificado todavía la secuencia verdadera de cargas de TIM del protagonista; tampoco reproduce blending de STP, comportamiento de caché o los modos especiales de GPU, ni combina automáticamente estos texeles con el visualizador de Godot. No se han reconstruido aún los materiales originales del protagonista. Los datos comerciales se mantienen fuera del repositorio y la integración sigue pendiente de validación.
