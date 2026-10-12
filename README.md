# Digital World 1 Online

Proyecto para recrear la exploración de Digimon World 1 con un cliente Godot, un servidor C# y herramientas Python.

## Stack definitivo
- **Cliente:** Godot 4, exclusivamente **GDScript**.
- **Backend:** C# / ASP.NET Core (.NET 8).
- **Herramientas y pruebas de conversión:** Python 3.11+.

No se utiliza Node.js, npm, Vite ni TypeScript. El prototipo anterior se retiró del árbol de trabajo; su historial permanece en Git.

## Ejecución

**Cliente:** importar `client-godot/project.godot` en Godot 4 y ejecutar F5. La escena inicial es un **visualizador del fondo original** de TWNA01, si se ha generado el PNG local desde la copia del usuario (ver [guía](docs/ORIGINAL_MAP_VIEWER.md)). Si no se ha importado, muestra instrucciones. La antigua prueba de personaje y movimiento 3D continúa en `client-godot/scenes/world.tscn`; la perspectiva y jugabilidad originales aún no están reproducidas.

**Servidor:**
```powershell
dotnet run --project server/DigitalWorld.Server.csproj
```

**Herramientas Python:**
```powershell
python -m unittest discover -s tools-python -p "test_*.py"
python tools-python/generate_demo_collision.py
```
El segundo comando crea `client-godot/assets/diagnostic/collision.json`, consumido por Godot para mostrar colisiones sintéticas.

## Estructura
- `client-godot/`: cliente y escenas en GDScript.
- `server/`: servidor C#.
- `tools-python/`: conversores, analizadores y pruebas en Python.
- `docs/`: arquitectura, roadmap e investigación técnica.

## Referencias
- [dw_decomp](https://github.com/saitamOsirb/dw_decomp): ingeniería inversa del juego de PlayStation.
- [DW1-Code](https://github.com/saitamOsirb/DW1-Code): rutinas documentadas de DW1.
- [DWDDRandomizer](https://github.com/saitamOsirb/DWDDRandomizer): es de Dawn/Dusk (Nintendo DS), no de DW1; solo referencia secundaria.

## Recursos
El repositorio no distribuye copias del juego, ROM, ISO ni recursos originales comerciales. Las herramientas consumen recursos que el usuario tenga derecho a utilizar y los resultados extraídos deben mantenerse locales.
