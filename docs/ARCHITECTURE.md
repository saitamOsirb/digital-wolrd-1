# Arquitectura oficial

| Capa | Lenguaje | Tecnología |
| --- | --- | --- |
| Cliente | GDScript | Godot 4 |
| Servidor | C# | ASP.NET Core / .NET 8 |
| Herramientas | Python | Biblioteca estándar y utilidades de conversión |

Se eliminó por completo el antiguo cliente TypeScript del árbol de la rama principal. Su historial permanece accesible mediante Git.

## Responsabilidades
`client-godot/`: render 3D, cámara, entrada, movimiento, UI e integración de recursos.
`server/`: lógica futura de mundo, instancias y sincronización autoritativa. Por el momento únicamente incluye diagnóstico HTTP y WebSocket.
`tools-python/`: análisis y conversión de datos extraídos localmente, más pruebas automatizadas.

## Ejecutar
```powershell
dotnet run --project server/DigitalWorld.Server.csproj
python -m unittest discover -s tools-python -p "test_*.py"
python tools-python/generate_demo_collision.py
```
Abrir `client-godot/project.godot` con Godot 4 y ejecutar F5.

## Próximo hito
Validar los importadores Python con datos sintéticos y luego con archivos legítimamente disponibles. Mapas, texturas, cámara y modelos originales todavía no están integrados a Godot.
