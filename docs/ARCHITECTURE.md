# Arquitectura oficial — 0.2.0

**Cliente:** Godot 4.x con GDScript (3D, no C#).
**Servidor:** C# con ASP.NET Core y .NET 8.
**Herramientas de extracción y conversión:** Python 3.11+.

## Estructura
- `client-godot/` nuevo cliente principal.
- `server/` servidor de red; solo /health y prueba de handshake WebSocket por ahora.
- `tools-python/` herramientas offline de importación a formatos intermedios.
- `client/` + `shared/` + raíz de Vite: prototipo TypeScript previo **conservado** por trazabilidad, no es el cliente objetivo.

La escena Godot contiene geometría sintética y un cuerpo de prueba; ningún recurso comercial está distribuido. El próximo hito es usar archivos locales obtenidos legalmente para estudiar material, formato de geometría, modelos y cámara. No se deben subir ROM, ISO ni recursos propietarios extraídos.

## Rutas de ejecución
Godot: abrir `client-godot/project.godot` en Godot 4 y ejecutar F6/F5.
Servidor: `dotnet run --project server/DigitalWorld.Server.csproj`.
Python: `python -m unittest discover -s tools-python -p 'test_*.py'`.

## Estado actual
Render, movimiento y colisiones de **escenario sintético**; servidor solo para verificar conectividad, sin cuentas ni sincronización de jugadores. No confundir el prototipo con una restauración visual completa.
