# Auditoría de la conversión de personajes originales — v0.8.2

Este paso conecta los scripts de búsqueda de archivos del disco, inspección TMD, lectura de vértices y decodificación parcial de UV en **un solo informe comprobable**. La herramienta no reconstruye al protagonista ni infiere qué modelo pertenece a cada personaje. Trabaja exclusivamente con la copia local del usuario.

## Ejecutar en Windows

```powershell
cd D:\developer\digital-wolrd-1
git pull --ff-only origin main
python tools-python/audit_dw1_character_pipeline.py "D:\ruta\Digimon World (USA).bin" --output ".local-assets/character-audit.json"
```

La ruta debe apuntar al BIN real en formato PS1 raw Mode2/2352, no al contenedor 7z. El archivo JSON distingue:
- `no-tmd-signatures`: no se localizaron cabeceras candidatas.
- `signature-only`: la cabecera parece TMD, pero falla la decodificación de vértices.
- `vertex-only`: se leen vértices, pero aún no se interpretan las caras texturizadas compatibles.
- `partial-ft3-ft4-decode`: se han identificado caras del subconjunto compatible.
- `animation-or-oversize-not-scanned`: no se analiza la animación MTN ni archivos superiores al límite.
- `file-read-error`: falla la lectura del archivo concreto.

El apartado `summary` presenta recuentos de archivos, firmas candidatas y caras texturizadas interpretadas; **no** representa una cifra de modelos válidos del protagonista.

## Pendiente para completar el objetivo final

Para presentar al protagonista original caminando por File City, faltan una identificación inequívoca de sus recursos, interpretación completa de geometría y texturas, decodificación real de las animaciones MTN/MMD, calibración de cámara y profundidad y ejecución de la escena integrada en Godot. Este informe ayuda a identificar dónde se atasca la cadena real y evita atribuir identidad al personaje sin evidencias.

El informe se guarda bajo `.local-assets` y no distribuye recursos del disco. **Las pruebas sintéticas están escritas, pero la ejecución sobre datos originales y en Godot sigue pendiente.**
