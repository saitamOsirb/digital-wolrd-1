# Investigación real de modelos PlayStation — 0.6.5

Esta entrega incorpora una primera comprobación **binaria**, no solo por nombres, para localizar encabezados candidatos del formato TMD de PlayStation en archivos proporcionados localmente.

El código descompilado `dw_decomp/src/main/model.c` referencia las rutas `CHDAT\\TMD0\\`, `CHDAT\\MTN0\\` y `CHDAT\\MMD0\\`. La función de carga también usa `TAMER_MODEL_BUFFER`. Estas pistas **no identifican por sí solas** el archivo exacto del protagonista ni implican que un encabezado coincidente contenga su modelo.

## Ejecutar con tu propia copia
1. Extrae la imagen BIN del archivo 7z que aportaste.
2. Enumera los archivos originales para localizar candidatos:
```powershell
python tools-python/inspect_character_assets.py "D:\\ruta\\Digimon World (USA).bin"
```
3. Si has identificado una ruta binaria concreta dentro del disco, extrae una copia de trabajo a una carpeta local:
```powershell
python tools-python/psx_iso.py "D:\\ruta\\Digimon World (USA).bin" "RUTA/ARCHIVO.BIN" ".local-assets/archivo.bin"
python tools-python/scan_psx_tmd.py ".local-assets/archivo.bin" --output ".local-assets/model-candidates.json"
python -m unittest discover -s tools-python -p "test_*.py"
```
**La ruta RUTA/ARCHIVO.BIN es un marcador de ejemplo**, no un archivo confirmado dentro de este juego. Debes sustituirla por una ruta existente de su índice ISO.

El lector revisa encabezados alineados de tipo `0x41`, banderas, cantidad de objetos y tablas de siete enteros por objeto. Informa ubicaciones y recuentos plausibles. Puede reportar falsos positivos; no interpreta primitivas, texturas, esqueleto ni animaciones y **no exporta modelos 3D todavía**.

Los recursos originales y resultados de ingeniería inversa deben permanecer locales y fuera de GitHub.
