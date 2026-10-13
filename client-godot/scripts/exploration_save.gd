extends RefCounted
# Local exploration save; map ids are resolved against the imported map catalog.
const SAVE_PATH := "user://exploration_save.json"
const VERSION := 1

static func write_state(map_id: String, position: Vector2, follow: bool, zoom: float) -> bool:
    if map_id.is_empty() or not is_finite(position.x) or not is_finite(position.y):
        return false
    if not is_finite(zoom) or zoom <= 0.0:
        return false
    var state := {"version": VERSION, "mapId": map_id,
        "position": [position.x, position.y], "follow": follow, "zoom": zoom}
    var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if file == null:
        push_warning("Cannot write exploration save: " + str(FileAccess.get_open_error()))
        return false
    file.store_string(JSON.stringify(state))
    file.close()
    return true

static func read_state() -> Dictionary:
    if not FileAccess.file_exists(SAVE_PATH):
        return {}
    var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
    if file == null:
        return {}
    var value: Variant = JSON.parse_string(file.get_as_text())
    if not value is Dictionary or value.get("version", -1) != VERSION:
        return {}
    var map_id: Variant = value.get("mapId", "")
    var point: Variant = value.get("position", [])
    var zoom: Variant = value.get("zoom", 1.0)
    var follow: Variant = value.get("follow", false)
    if not map_id is String or map_id.is_empty():
        return {}
    if not point is Array or point.size() != 2:
        return {}
    for coordinate in point:
        if not (coordinate is float or coordinate is int) or not is_finite(float(coordinate)):
            return {}
    if not (zoom is float or zoom is int) or not is_finite(float(zoom)) or zoom <= 0.0:
        return {}
    if not follow is bool:
        return {}
    return {"mapId": map_id, "position": Vector2(float(point[0]), float(point[1])),
        "follow": follow, "zoom": clampf(float(zoom), 0.25, 6.0)}
