extends RefCounted
# Local author-defined links between imported PS1 map backgrounds.
# These do not claim to be original DW1 exits or warp coordinates.
static func load_links(path: String, map_id: String) -> Array[Dictionary]:
    var result: Array[Dictionary] = []
    if not FileAccess.file_exists(path):
        return result
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return result
    var root: Variant = JSON.parse_string(file.get_as_text())
    if not root is Dictionary:
        return result
    var entries: Variant = root.get(map_id, [])
    if not entries is Array or entries.size() > 100:
        return result
    for entry in entries:
        if not entry is Dictionary:
            continue
        var destination: Variant = entry.get("to", "")
        var rect: Variant = entry.get("rect", [])
        var spawn: Variant = entry.get("spawn", [])
        if not destination is String or destination.is_empty():
            continue
        if not rect is Array or rect.size() != 4 or not spawn is Array or spawn.size() != 2:
            continue
        var values := PackedFloat32Array()
        var valid := true
        for value in rect + spawn:
            if not (value is float or value is int):
                valid = false
                break
            values.append(float(value))
        if not valid or values[2] <= 0.0 or values[3] <= 0.0:
            continue
        result.append({"to": destination, "rect": Rect2(values[0], values[1], values[2], values[3]),
            "spawn": Vector2(values[4], values[5])})
    return result

static func destination(position: Vector2, links: Array[Dictionary]) -> Dictionary:
    for link in links:
        var area: Rect2 = link["rect"]
        if area.has_point(position):
            return link
    return {}
