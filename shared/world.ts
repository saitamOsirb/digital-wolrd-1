export type Vec2 = { x: number; y: number };
export type Rect = { x: number; y: number; w: number; h: number };
export type World = { width: number; height: number; obstacles: Rect[] };
export type Player = { position: Vec2; facing: Vec2; radius: number; speed: number };
export const world: World = {
  width: 2200, height: 1500,
  obstacles: [
    { x: 0, y: 0, w: 2200, h: 65 }, { x: 0, y: 1435, w: 2200, h: 65 },
    { x: 0, y: 0, w: 65, h: 1500 }, { x: 2135, y: 0, w: 65, h: 1500 },
    { x: 370, y: 290, w: 240, h: 160 }, { x: 1050, y: 580, w: 350, h: 160 },
    { x: 1650, y: 220, w: 170, h: 350 }, { x: 450, y: 950, w: 170, h: 320 },
    { x: 1430, y: 1070, w: 420, h: 120 }
  ]
};
export const newPlayer = (): Player => ({
  position: { x: 770, y: 700 }, facing: { x: 0, y: 1 }, radius: 18, speed: 185
});
function intersectsCircleRect(cx: number, cy: number, radius: number, r: Rect): boolean {
  const px = Math.max(r.x, Math.min(cx, r.x + r.w));
  const py = Math.max(r.y, Math.min(cy, r.y + r.h));
  return (cx - px) ** 2 + (cy - py) ** 2 < radius ** 2;
}
export function blocked(x: number, y: number, radius: number, map: World): boolean {
  return x - radius < 0 || y - radius < 0 || x + radius > map.width || y + radius > map.height ||
    map.obstacles.some(r => intersectsCircleRect(x, y, radius, r));
}
export function move(player: Player, intent: Vec2, dt: number, map: World, running = false): void {
  if (!Number.isFinite(dt) || dt <= 0) return;
  const mag = Math.hypot(intent.x, intent.y);
  if (mag < 0.001) return;
  const dx = intent.x / mag, dy = intent.y / mag;
  player.facing = { x: dx, y: dy };
  const distance = player.speed * (running ? 1.6 : 1) * Math.min(dt, 0.05);
  // Discrete substeps prevent tunneling through thin obstacles at high speed.
  const n = Math.ceil(distance / Math.max(1, player.radius / 2));
  for (let i = 0; i < n; i++) {
    const sx = dx * distance / n, sy = dy * distance / n;
    if (!blocked(player.position.x + sx, player.position.y, player.radius, map)) player.position.x += sx;
    if (!blocked(player.position.x, player.position.y + sy, player.radius, map)) player.position.y += sy;
  }
}
