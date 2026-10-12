import { move, newPlayer, world } from '../shared/world.ts';
import './style.css';
const canvas = document.querySelector<HTMLCanvasElement>('#game')!;
const hud = document.querySelector<HTMLElement>('#hud')!;
const context = canvas.getContext('2d', { alpha: false })!;
const player = newPlayer();
const pressed = new Set<string>();
const controlKeys = new Set(['arrowup','arrowdown','arrowleft','arrowright',' ','shift']);
addEventListener('keydown', e => { const k = e.key.toLowerCase(); if (controlKeys.has(k)) e.preventDefault(); pressed.add(k); });
addEventListener('keyup', e => pressed.delete(e.key.toLowerCase()));
addEventListener('blur', () => pressed.clear());
function resize(): void {
  const ratio = Math.min(devicePixelRatio || 1, 2);
  canvas.width = Math.round(innerWidth * ratio);
  canvas.height = Math.round(innerHeight * ratio);
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
}
addEventListener('resize', resize); resize();
const down = (...keys: string[]) => keys.some(k => pressed.has(k));
let previous = performance.now(), fps = 60;
function render(now: number): void {
  const dt = Math.min((now - previous) / 1000, 0.05); previous = now;
  fps = fps * 0.94 + (dt > 0 ? 1 / dt : 60) * 0.06;
  const intent = { x: Number(down('d', 'arrowright')) - Number(down('a', 'arrowleft')), y: Number(down('s', 'arrowdown')) - Number(down('w', 'arrowup')) };
  const running = down('shift');
  move(player, intent, dt, world, running);
  const width = innerWidth, height = innerHeight;
  const cameraX = Math.max(0, Math.min(world.width - width, player.position.x - width / 2));
  const cameraY = Math.max(0, Math.min(world.height - height, player.position.y - height / 2));
  context.fillStyle = '#8fb46a'; context.fillRect(0, 0, width, height);
  context.save(); context.translate(-cameraX, -cameraY);
  context.fillStyle = '#aacb79'; context.fillRect(65, 65, world.width - 130, world.height - 130);
  context.strokeStyle = '#91b365'; context.lineWidth = 1;
  for (let x = 65; x < world.width; x += 80) { context.beginPath(); context.moveTo(x, 65); context.lineTo(x, world.height - 65); context.stroke(); }
  for (let y = 65; y < world.height; y += 80) { context.beginPath(); context.moveTo(65, y); context.lineTo(world.width - 65, y); context.stroke(); }
  for (const r of world.obstacles) {
    context.fillStyle = '#324f3c'; context.fillRect(r.x, r.y, r.w, r.h);
    context.fillStyle = '#537d54'; context.fillRect(r.x + 7, r.y + 7, Math.max(0, r.w - 14), Math.max(0, r.h - 14));
  }
  context.beginPath(); context.ellipse(player.position.x, player.position.y + 15, 20, 9, 0, 0, Math.PI * 2);
  context.fillStyle = '#31422f66'; context.fill();
  context.beginPath(); context.arc(player.position.x, player.position.y, player.radius, 0, Math.PI * 2);
  context.fillStyle = '#f2b451'; context.fill(); context.lineWidth = 4; context.strokeStyle = '#374e83'; context.stroke();
  context.beginPath(); context.moveTo(player.position.x, player.position.y);
  context.lineTo(player.position.x + player.facing.x * 25, player.position.y + player.facing.y * 25);
  context.strokeStyle = '#ffffff'; context.lineWidth = 3; context.stroke();
  context.restore();
  hud.textContent = 'DIGITAL WORLD 1 — prototipo 0.1.0  |  X: ' + player.position.x.toFixed(0) + '  Y: ' + player.position.y.toFixed(0) + '  |  ' + fps.toFixed(0) + ' FPS  |  ' + (running ? 'Corriendo' : 'Explorando') + '  |  Escenario sintético (sin assets PS1)';
  requestAnimationFrame(render);
}
requestAnimationFrame(render);
