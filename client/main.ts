import { move, newPlayer } from '../shared/world.ts';
import { cameraCenter, parseScene, toWorld, type Scene } from '../shared/scene.ts';
import './style.css';

const canvas = document.querySelector<HTMLCanvasElement>('#game')!;
const hud = document.querySelector<HTMLElement>('#hud')!;
const context = canvas.getContext('2d', { alpha: false })!;
const keys = new Set<string>();
const controlKeys = new Set(['arrowup','arrowdown','arrowleft','arrowright',' ','shift']);
addEventListener('keydown', event => {
  const key = event.key.toLowerCase();
  if (controlKeys.has(key)) event.preventDefault();
  keys.add(key);
});
addEventListener('keyup', e => keys.delete(e.key.toLowerCase()));
addEventListener('blur', () => keys.clear());
function resize(): void {
  const ratio = Math.min(devicePixelRatio || 1, 2);
  canvas.width = Math.round(innerWidth * ratio);
  canvas.height = Math.round(innerHeight * ratio);
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
}
addEventListener('resize', resize);
resize();
const down = (...options: string[]) => options.some(key => keys.has(key));
const colors: Record<Scene['decorations'][number]['kind'], string> = {
  tree:'#416645', water:'#4c9cb4', path:'#ceb98b', building:'#b19770'
};
function drawScene(scene: Scene, camera: { x: number; y: number }): void {
  const w = scene.bounds.width, h = scene.bounds.height;
  context.fillStyle = '#a4c576'; context.fillRect(0, 0, w, h);
  for (const decoration of scene.decorations) {
    context.fillStyle = colors[decoration.kind];
    const r = decoration.rect; context.fillRect(r.x, r.y, r.w, r.h);
  }
  context.strokeStyle = '#87a965'; context.lineWidth = 1;
  const left = Math.floor(camera.x / 80) * 80;
  const top = Math.floor(camera.y / 80) * 80;
  for (let x = left; x <= Math.min(w, camera.x + innerWidth + 80); x += 80) {
    context.beginPath(); context.moveTo(x, 0); context.lineTo(x, h); context.stroke();
  }
  for (let y = top; y <= Math.min(h, camera.y + innerHeight + 80); y += 80) {
    context.beginPath(); context.moveTo(0, y); context.lineTo(w, y); context.stroke();
  }
  context.fillStyle = '#39564aaa';
  for (const r of scene.collision) context.fillRect(r.x, r.y, r.w, r.h);
}
function drawAvatar(x: number, y: number, facing: { x: number; y: number }, moving: boolean, now: number): void {
  const bob = moving ? Math.sin(now * 0.012) * 2 : 0;
  context.beginPath(); context.ellipse(x, y + 15, 20, 9, 0, 0, Math.PI * 2);
  context.fillStyle = '#31422f66'; context.fill();
  context.beginPath(); context.arc(x, y + bob, 18, 0, Math.PI * 2);
  context.fillStyle = '#f2b451'; context.fill(); context.lineWidth = 4;
  context.strokeStyle = '#374e83'; context.stroke();
  context.beginPath(); context.moveTo(x, y + bob);
  context.lineTo(x + facing.x * 25, y + facing.y * 25 + bob);
  context.strokeStyle = '#fff'; context.lineWidth = 3; context.stroke();
}
async function start(): Promise<void> {
  const response = await fetch('/scenes/file-city-prototype.json');
  if (!response.ok) throw new Error('No se pudo cargar el escenario: HTTP ' + response.status);
  const scene = parseScene(await response.json());
  const world = toWorld(scene), player = newPlayer();
  player.position = { ...scene.spawn };
  let previous = performance.now(), fps = 60;
  function frame(now: number): void {
    const dt = Math.min((now - previous) / 1000, 0.05); previous = now;
    if (dt > 0) fps = fps * 0.94 + (1 / dt) * 0.06;
    const intent = {
      x: Number(down('d', 'arrowright')) - Number(down('a', 'arrowleft')),
      y: Number(down('s', 'arrowdown')) - Number(down('w', 'arrowup'))
    };
    const moving = intent.x !== 0 || intent.y !== 0;
    const running = down('shift');
    move(player, intent, dt, world, running);
    const camera = cameraCenter(player.position, scene, { x: innerWidth, y: innerHeight });
    context.fillStyle = '#152d37'; context.fillRect(0, 0, innerWidth, innerHeight);
    context.save(); context.translate(-camera.x, -camera.y);
    drawScene(scene, camera);
    drawAvatar(player.position.x, player.position.y, player.facing, moving, now);
    context.restore();
    hud.textContent = 'DIGITAL WORLD 1 — 0.1.1 · ' + scene.name +
      ' · X: ' + player.position.x.toFixed(0) + ' Y: ' + player.position.y.toFixed(0) +
      ' · ' + fps.toFixed(0) + ' FPS · ' + (running ? 'Corriendo' : 'Explorando') +
      ' · SIN RECURSOS DEL JUEGO ORIGINAL';
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
start().catch(error => {
  hud.textContent = 'Error al iniciar la escena: ' + (error instanceof Error ? error.message : String(error));
  console.error(error);
});
