# Transiciones de escenarios (v0.5.7)

El visor de fondos originales ahora admite **enlaces configurables entre mapas importados**. Esto permite prototipar una exploración continua de escenarios antes de reconstruir los warps auténticos del juego.

Crea localmente `client-godot/assets/maps/transitions.json`:

```json
{
  "TWNA01": [
    {"rect": [100, 40, 60, 30], "to": "TWNA02", "spawn": [350, 400]}
  ],
  "TWNA02": [
    {"rect": [325, 430, 80, 25], "to": "TWNA01", "spawn": [120, 90]}
  ]
}
```

- `rect`: zona de activación `[x, y, ancho, alto]` en píxeles de la imagen actual.
- `to`: identificador `mapId` tal como figura en el catálogo local.
- `spawn`: destino `[x, y]` sobre el fondo siguiente.

Para generar un catálogo desde tu copia extraída:

```powershell
python tools-python/import_all_maps.py "D:\\ruta\\Digimon World (USA).bin" --limit 20
```

Al entrar con el marcador en una zona de transición, el visor cambia el mapa y posiciona el marcador en `spawn`. Un breve enfriamiento evita bucles de teletransporte inmediato. Si el escenario de destino no está importado, la transición se ignora y se registra una advertencia.

**Limitaciones:** las transiciones descritas aquí son de edición manual para un prototipo, no conexiones verificadas del Digimon World original. El marcador sigue siendo una herramienta de navegación 2D; todavía no existen personaje y animaciones originales, profundidad de capas, cámara 3D PS1 ni colisiones nativas. No se han realizado pruebas en Godot sobre esta versión.
