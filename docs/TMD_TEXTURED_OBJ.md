# Mallas TMD con texturas experimentales — v0.7.8

La herramienta `tools-python/export_tmd_textured_obj.py` conecta las caras FT3/FT4 decodificadas con páginas PNG previamente reconstruidas desde VRAM. Genera Wavefront OBJ con índices de vértices y UV (`vt`) y MTL apuntando al archivo PNG. Solo incluye caras cuyos **TPAGE y CLUT coinciden exactamente** con los solicitados, para evitar asociar texturas incorrectas.

## Flujo local
```powershell
python tools-python/inspect_tmd_uv.py ".local-assets/modelo.bin" --offset 0x0 --output ".local-assets/modelo-uv.json"
python tools-python/render_psx_texture_page.py ".local-assets/textura.tim" --tpage 0x80 --clut 0x0 --output ".local-assets/pagina.png"
python tools-python/export_tmd_textured_obj.py ".local-assets/modelo-uv.json" --tpage 0x80 --clut 0x0 --texture ".local-assets/pagina.png" --output ".local-assets/modelo-texturizado.obj"
```

Los valores anteriores son **ejemplos**, no ubicaciones verificadas del protagonista. Usa los valores del informe de tu modelo real y las texturas TIM correspondientes. La imagen PNG y el OBJ deben estar en el mismo directorio. Abre el OBJ en Blender o impórtalo en Godot para estudiar el material.

**Limitaciones:** el conversor cubre solo los paquetes FT3/FT4 sin iluminación que entiende `inspect_tmd_uv.py`; las demás caras se omiten. Las UV se normalizan a una página de 256 píxeles, con convención V invertida para OBJ; esto no garantiza una imagen fiel si la secuencia de cargas TIM/CLUT no corresponde al juego. No se han reconstruido modelo completo, rig, animaciones ni integración en File City, y las pruebas de ejecución siguen pendientes.

Los binarios y modelos extraídos de la copia del usuario se mantienen locales y fuera de Git.
