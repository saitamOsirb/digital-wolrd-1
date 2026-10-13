# Descubrimiento de archivos originales CHDAT — v0.8.1

En lugar de aumentar visualizadores con nombres ficticios, esta entrega proporciona un paso **concreto para localizar los recursos originales** del protagonista en el disco de Digimon World 1.

El código descompilado en `dw_decomp/src/main/model.c` referencia rutas `CHDAT\\TMD0\\`, `CHDAT\\MMD0\\` y `CHDAT\\MTN0\\`. La herramienta `tools-python/discover_dw1_character_archives.py` enumera rutas que **realmente existen** dentro del índice ISO9660 de la copia local del usuario, reporta tamaños y opcionalmente inspecciona encabezados TMD dentro de archivos TMD0/MMD0. No extrae archivos por defecto ni considera cualquier coincidencia una identificación del protagonista.

## Ejecutar

Extrae localmente el archivo BIN de tu copia del disco (2352 bytes por sector) y ejecuta:

```powershell
cd D:\developer\digital-wolrd-1
python tools-python/discover_dw1_character_archives.py "D:\ruta\Digimon World (USA).bin" --output ".local-assets/character-archive-inventory.json"
```

Para analizar adicionalmente candidatos TMD dentro de archivos compatibles, sin escribir los datos comerciales en disco:

```powershell
python tools-python/discover_dw1_character_archives.py "D:\ruta\Digimon World (USA).bin" --scan-tmd --output ".local-assets/character-archive-inventory.json"
```

El informe contiene `archives`, `counts`, y para cada ruta candidatos `tmdCandidates` con offsets (si corresponde). El lector ISO supone imagen cruda PS1 Mode2/2352; no acepta directamente un archivo .7z ni un dump ISO 2048.

## Estado del objetivo

No se ha comprobado todavía el contenido real del disco del usuario ni identificado inequívocamente el tamer. Tener archivos en CHDAT y firmas TMD posibles es evidencia para investigar, **no garantía de que correspondan al personaje**. Las estructuras de animación MTN/MMD y la cámara de File City continúan pendientes. Sin esos binarios específicos no podemos prometer un protagonista original animado y funcional.

Esta entrega incluye pruebas unitarias aisladas con nombres sintéticos; la ejecución sobre el disco real y Godot está pendiente. No se publica contenido protegido por derechos de autor en el repositorio.
