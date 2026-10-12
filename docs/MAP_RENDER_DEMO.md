# Demo de renderizado de mapas — v0.4.0

## Resultado
El cliente Godot ahora presenta **un escenario 2D compuesto de tiles de 128×128**, como textura sobre una superficie 3D. El protagonista provisional se mueve sobre esa superficie, que conserva el sistema de colisiones 3D. Se puede ejecutar sin preparar archivos: GDScript genera un fondo **sintético** por defecto.

También se puede reemplazar por una textura PNG de 512×512 compuesta por Python. **Todavía NO es File City original:** falta decodificar de forma validada los bloques de imagen de los archivos TFS y su composición exacta. Esta demo es un paso funcional del renderizador, no una extracción del juego comercial.

## Probar directamente
```powershell
cd D:\developer\digital-wolrd-1
git pull --ff-only origin main
```
Abre `client-godot/project.godot` en Godot 4 y ejecuta **F5**. Aparecerá suelo texturizado con camino y estanque, cámara de seguimiento, avatar cápsula y bloques sólidos. No requiere Python para funcionar.

## Probar el pipeline Python → Godot
```powershell
python tools-python/render_map_demo.py
python -m unittest discover -s tools-python -p "test_*.py"
```
Vuelve a ejecutar Godot. La aplicación carga el mapa PNG desde `res://assets/demo/map.png` y lo representa en el plano del suelo. Se genera también un archivo `map.json` con las dimensiones y el origen sintético.

El directorio `client-godot/assets/demo/` está ignorado por Git para evitar publicar por accidente mapas convertidos desde material protegido. La imagen de prueba es creada por código, sin recursos originales.

## Arquitectura del flujo
```text
Python: 4×4 tiles RGBA de 128×128
         │
         └── composición → map.png (512×512)
                                      │
GDScript: Image.load → ImageTexture → PlaneMesh
                                      │
                        Personaje 3D + colisiones 3D
```

## Limitaciones siguientes
1. Verificar en Godot 4 las dimensiones del plano, UV, profundidad y orientación.
2. Construir lector de datos de tiles TFS probado con capturas y archivos permitidos.
3. Conservar la información de paletas CLUT, orden de dibujo y overlays.
4. Importar la verdadera imagen de escenario, cámara/proyección y protagonista 3D.
5. Añadir pruebas de integración Godot y C# de forma automatizada.

Se mantienen exclusivamente GDScript, C# y Python.
