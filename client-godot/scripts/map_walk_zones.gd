extends RefCounted
# Optional local authoring data, not collision data extracted from original DW1.
# JSON stores blocked polygons in source image pixel coordinates for each map.
static func load_polygons(path: String, map_name: String) -> Array[PackedVector2Array]:
    var result: Array[PackedVector2Array] = []
    if not FileAccess.file_exists(path):
        return result
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return result
    var root: Variant = JSON.parse_string(file.get_as_text())
    if not root is Dictionary:
        return result
    var map_data: Variant = root.get(map_name, [])
    if not map_data is Array:
        return result
    for polygon_data in map_data:
        if not polygon_data is Array or polygon_data.size() < 3 or polygon_data.size() > 200:
            continue
        var vertices := PackedVector2Array()
        for position_data in polygon_data:
            if not position_data is Array or position_data.size() != 2:
                vertices.clear()
                break
            var x: Variant = position_data[0]
            var y: Variant = position_data[1]
            if not (x is float or x is int) or not (y is float or y is int):
                vertices.clear()
                break
            vertices.append(Vector2(float(x), float(y)))
        if vertices.size() >= 3:
            result.append(vertices)
    return result

static func is_blocked(position: Vector2, polygons: Array[PackedVector2Array]) -> bool:
    for polygon in polygons:
        if Geometry2D.is_point_in_polygon(position, polygon):
            return true
    return false
