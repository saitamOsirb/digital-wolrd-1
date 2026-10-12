import assert from 'node:assert/strict';
import test from 'node:test';
import { blocked, move, newPlayer, world } from './world.ts';

test('avatar remains inside playable bounds', () => {
  const p = newPlayer();
  for (let i = 0; i < 1000; i++) move(p, { x: -1, y: 0 }, 1 / 60, world);
  assert.ok(p.position.x >= 65 + p.radius - 0.01);
});
test('movement is normalized diagonally', () => {
  const a = newPlayer(), b = newPlayer();
  move(a, { x: 1, y: 0 }, 0.016, world);
  move(b, { x: 1, y: 1 }, 0.016, world);
  assert.ok(Math.abs(Math.hypot(b.position.x - 770, b.position.y - 700) - (a.position.x - 770)) < 0.01);
});
test('collision rejects obstacle interior', () => {
  assert.equal(blocked(400, 350, 18, world), true);
  assert.equal(blocked(770, 700, 18, world), false);
});
