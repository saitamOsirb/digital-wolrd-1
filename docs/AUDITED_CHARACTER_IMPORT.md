# Importación directa desde la auditoría — v0.8.3

Esta entrega une tres etapas que antes estaban desconectadas: **auditoría del disco real → selección explícita de candidato → visualización texturizada en Godot**.

## Pasos

1. Extrae localmente el BIN raw Mode2/2352 de tu copia del disco y ejecuta la auditoría:

```powershell
python tools-python/audit_dw1_character_pipeline.py "D:\ruta\Digimon World (USA).bin" --output ".local-assets/character-audit.json"
```

2. Inspecciona el JSON. Selecciona **la ruta exacta** de un archivo `CHDAT/TMD0` o `CHDAT/MMD0` cuyo candidato tenga `status: "partial-ft3-ft4-decode"` y `texturedFaces` superior a cero.

3. Cuando sepas las rutas ISO de los TIM correctos para ese modelo, ejecuta:

```powershell
python tools-python/import_audited_character.py "D:\ruta\Digimon World (USA).bin" --audit ".local-assets/character-audit.json" --archive "CHDAT/MMD0/EJEMPLO.BIN" --offset 0x20 --tim-path "RUTA/REAL/TEXTURA.TIM" --output "client-godot/assets/characters/preview"
```

**Atención:** las rutas del comando de ejemplo son marcadores ilustrativos. No afirmamos que existan en el disco. Deben reemplazarse por los nombres auténticos del informe y por rutas TIM efectivamente presentes en la imagen del juego. Se pueden repetir opciones `--tim-path` para respetar el orden de carga.

4. En Godot abre `res://scenes/tmd_textured_preview.tscn` y ejecuta **F6**.

El script produce `model.json`, páginas PNG por TPAGE/CLUT y `provenance.json` que registra la selección y deja `verifiedTamer` y `verifiedAnimation` en `false`. Los recursos comerciales siguen exclusivamente en carpetas locales ignoradas por Git.

## Limitaciones

La auditoría verifica solo un subconjunto experimental de primitivas FT3/FT4, por lo que no garantiza decodificación completa. **Todavía no identificamos el modelo original del protagonista, sus TIM correctos ni sus clips de animación**; la herramienta tampoco integra un modelo 3D en File City. Esta entrega agrega el enlace operativo para avanzar con resultados reales, no una demo finalizada. La ejecución integrada con el BIN original y Godot sigue pendiente.
