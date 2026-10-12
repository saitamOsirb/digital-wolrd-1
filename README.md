# Digital World 1 Online

Reimplementación web experimental inspirada en el flujo de exploración de Digimon World (PS1).

## Estado — 0.1.0
Primera *vertical slice* jugable: mapa de prueba, avatar temporal, cámara, colisiones y movimiento continuo por teclado. **Todavía no renderiza los escenarios ni los modelos originales**: estos requieren extracción legal, conversión y validación de formatos. La demo usa gráficos geométricos propios para comprobar el motor sin redistribuir material protegido.

## Ejecutar
Requisitos: Node.js 22.10+ y pnpm 9+.

```bash
pnpm install
pnpm dev
```

Abrir la URL indicada por Vite. Movimiento: WASD o flechas, Shift para correr. Panel de diagnóstico: posición, FPS y estado de colisiones. Las pruebas de lógica: `pnpm test`.

## Referencias técnicas
- [dw_decomp](https://github.com/saitamOsirb/dw_decomp): decompilación en progreso del **Digimon World de PS1**. Referencia principal para reconstruir comportamiento.
- [DW1-Code](https://github.com/saitamOsirb/DW1-Code): anotaciones y rutinas de ingeniería inversa de DW1 (movimiento, colisiones, cámara y entidades).
- [DWDDRandomizer](https://github.com/saitamOsirb/DWDDRandomizer): **Dawn/Dusk de Nintendo DS**, no DW1. Útil solo como referencia de herramientas y calidad, nunca como fuente de mapas de PS1.

## Arquitectura prevista
`client/`: Vite + TypeScript + Canvas2D (motor de pruebas). `shared/`: geometría y simulación pura. `server/`: autoridad multijugador, aún sin implementar. `tools/`: importadores futuros de recursos extraídos legalmente.

## Política de recursos
No subir ISOs, archivos extraídos de juegos comerciales ni modelos/texturas originales sin contar con los derechos necesarios. Un extractor local debería recibir archivos del usuario y escribir en una ruta ignorada por git.

## Evolución
Ver [CHANGELOG.md](CHANGELOG.md) y [docs/ROADMAP.md](docs/ROADMAP.md).
