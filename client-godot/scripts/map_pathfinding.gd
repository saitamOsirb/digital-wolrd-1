extends RefCounted
# Diagnostic 2D A* navigation over an imported background. Not PS1 pathfinding.
const CELL := 16
const MAX_CELLS := 20000

static func find_path(start: Vector2, goal: Vector2, image_size: Vector2, obstacles: Array[PackedVector2Array]) -> PackedVector2Array:
    var width := ceili(image_size.x / CELL)
    var height := ceili(image_size.y / CELL)
    var empty := PackedVector2Array()
    if width <= 0 or height <= 0 or width * height > MAX_CELLS:
        return empty
    var a := Vector2i(clampi(int(start.x / CELL), 0, width - 1), clampi(int(start.y / CELL), 0, height - 1))
    var b := Vector2i(clampi(int(goal.x / CELL), 0, width - 1), clampi(int(goal.y / CELL), 0, height - 1))
    var grid := AStarGrid2D.new()
    grid.region = Rect2i(0, 0, width, height)
    grid.cell_size = Vector2(CELL, CELL)
    grid.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
    grid.update()
    for y in range(height):
        for x in range(width):
            var center := Vector2(x * CELL + CELL * 0.5, y * CELL + CELL * 0.5)
            for polygon in obstacles:
                if Geometry2D.is_point_in_polygon(center, polygon):
                    grid.set_point_solid(Vector2i(x, y), true)
                    break
    if grid.is_point_solid(a) or grid.is_point_solid(b):
        return empty
    var cell_path := grid.get_id_path(a, b)
    if cell_path.is_empty():
        return empty
    var path := PackedVector2Array()
    for id in cell_path:
        path.append(Vector2(id.x * CELL + CELL * 0.5, id.y * CELL + CELL * 0.5))
    if path.size() > 0:
        path[0] = start
        path[path.size() - 1] = goal
    return path
