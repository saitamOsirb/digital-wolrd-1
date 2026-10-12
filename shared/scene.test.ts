import assert from 'node:assert/strict';
import test from 'node:test';
import { cameraCenter, parseScene } from './scene.ts';

const fixture = () => ({
  schemaVersion: 1, id: 'test', name: 'Zona de prueba', source: 'synthetic',
  bounds: { width: 400, height: 300 }, spawn: { x: 100, y: 100 },
  collision: [{ x: 200, y: 100, w: 25, h: 30 }], decorations: []
});
test('valid scene parses', () => assert.equal(parseScene(fixture()).id, 'test'));
test('reject invalid collision bounds', () => {
  const s = fixture(); s.collision[0].x = -1;
  assert.throws(() => parseScene(s), /colisión/);
});
test('reject colliding spawn', () => {
  const s = fixture(); s.spawn = { x: 205, y: 105 };
  assert.throws(() => parseScene(s), /punto inicial/);
});
test('camera clamps on maps smaller than viewport', () => {
  const scene = parseScene(fixture());
  assert.deepEqual(cameraCenter({ x: 200, y: 200 }, scene, { x: 800, y: 600 }), { x: 0, y: 0 });
});
