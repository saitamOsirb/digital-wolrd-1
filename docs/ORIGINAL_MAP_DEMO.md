# Mapa original TWNA01 — File City

Se verificó el archivo original `MAP/MAP14/TWNA01.TFS` de la edición USA de Digimon World aportada por el usuario. Contiene 6×5 tiles de 128 píxeles, 3 paletas CLUT de 256 colores y produce una imagen auténtica de 768×640 píxeles.

Para ejecutar desde Windows, extraer primero el BIN del archivo 7z y utilizar:

```powershell
python tools-python/import_original_map.py "D:\\ruta\\Digimon World (USA).bin" --map TWNA01
python -m unittest discover -s tools-python -p "test_*.py"
```

Abrir `client-godot/project.godot` en Godot 4 y ejecutar F5. El mapa original se muestra mediante `client-godot/assets/demo/map.png`, directorio excluido del repositorio. El mapa es un fondo prerenderizado; sigue pendiente integrar las animaciones y modelos originales, cámara exacta, overlays y colisiones. No subir recursos extraídos comercialmente a GitHub.
