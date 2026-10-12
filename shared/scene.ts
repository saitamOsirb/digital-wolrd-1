import type { Rect, Vec2, World } from './world.ts';

export type Scene = {
  schemaVersion: 1;
  id: string;
  name: string;
  source: 'synthetic' | 'local-extraction';
  bounds: { width: number; height: number };
  spawn: Vec2;
  collision: Rect[];
  decorations: Array<{ kind: 'tree' | 'water' | 'path' | 'building'; rect: Rect }>;
};

const finite = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v);
function rect(v: unknown, width: number, height: number): v is Rect {
  if (!v || typeof v !== 'object') return false;
  const r = v as Partial<Rect>;
  return finite(r.x) && finite(r.y) && finite(r.w) && finite(r.h) &&
    r.x >= 0 && r.y >= 0 && r.w > 0 && r.h > 0 && r.x + r.w <= width && r.y + r.h <= height;
}
export function parseScene(input: unknown): Scene {
  if (!input || typeof input !== 'object') throw new Error('El documento de escena debe ser un objeto');
  const obj = input as Partial<Scene>;
  if (obj.schemaVersion !== 1) throw new Error('Versión de esquema de escena no soportada');
  if (typeof obj.id !== 'string' || !/^[a-z0-9_-]{1,64}$/.test(obj.id)) throw new Error('ID de escena inválido');
  if (typeof obj.name !== 'string' || obj.name.trim().length === 0 || obj.name.length > 100) throw new Error('Nombre de escena inválido');
  if (obj.source !== 'synthetic' && obj.source !== 'local-extraction') throw new Error('Origen de escena inválido');
  const w = obj.bounds?.width, h = obj.bounds?.height;
  if (!finite(w) || !finite(h) || w < 128 || h < 128 || w > 65536 || h > 65536) throw new Error('Límites de escena inválidos');
  if (!obj.spawn || !finite(obj.spawn.x) || !finite(obj.spawn.y) ||
    obj.spawn.x < 0 || obj.spawn.y < 0 || obj.spawn.x > w || obj.spawn.y > h) throw new Error('Punto inicial inválido');
  if (!Array.isArray(obj.collision) || obj.collision.length > 20000 || !obj.collision.every(r => rect(r, w, h))) throw new Error('Geometría de colisión inválida');
  if (!Array.isArray(obj.decorations) || obj.decorations.length > 20000 ||
    !obj.decorations.every(d => d && ['tree', 'water', 'path', 'building'].includes(d.kind) && rect(d.rect, w, h)))
    throw new Error('Decoraciones inválidas');
  const radius = 18;
  if (obj.collision.some(r => {
    const px = Math.max(r.x, Math.min(obj.spawn!.x, r.x + r.w));
    const py = Math.max(r.y, Math.min(obj.spawn!.y, r.y + r.h));
    return (px - obj.spawn!.x) ** 2 + (py - obj.spawn!.y) ** 2 < radius ** 2;
  })) throw new Error('El punto inicial está dentro de una colisión');
  return obj as Scene;
}
export function toWorld(scene: Scene): World {
  return { width: scene.bounds.width, height: scene.bounds.height, obstacles: scene.collision };
}
export function cameraCenter(position: Vec2, scene: Scene, viewport: Vec2): Vec2 {
  return {
    x: Math.max(0, Math.min(Math.max(0, scene.bounds.width - viewport.x), position.x - viewport.x / 2)),
    y: Math.max(0, Math.min(Math.max(0, scene.bounds.height - viewport.y), position.y - viewport.y / 2))
  };
}
