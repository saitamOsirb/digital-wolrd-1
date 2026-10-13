extends RefCounted
# Local editor for hand-authored blocked polygons, NOT decoded PS1 collisions.
static func save_polygons(path: String, map_id: String, polygons: Array[PackedVector2Array]) -> bool:
    if map_id.is_empty() or polygons.size() > 500:
        return false
    var root: Dictionary = {}
    if FileAccess.file_exists(path):
        var old := FileAccess.open(path, FileAccess.READ)
        if old != null:
            var parsed: Variant = JSON.parse_string(old.get_as_text())
            if parsed is Dictionary:
                root = parsed
    var rows: Array = []
    for polygon in polygons:
        if polygon.size() < 3 or polygon.size() > 200:
            return false
        var points: Array = []
        for point in polygon:
            if not is_finite(point.x) or not is_finite(point.y):
                return false
            points.append([point.x, point.y])
        rows.append(points)
    root[map_id] = rows
    var dir := ProjectSettings.globalize_path(path.get_base_dir())
    if DirAccess.make_dir_recursive_absolute(dir) != OK:
        return false
    var file := FileAccess.open(path, FileAccess.WRITE)
    if file == null:
        return false
    file.store_string(JSON.stringify(root, "\t") + "\n")
    file.close()
    return true
