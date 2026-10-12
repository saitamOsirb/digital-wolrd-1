extends RefCounted
class_name CollisionLoader

static func load_map(path: String) -> Array[Dictionary]:
    var output: Array[Dictionary] = []
    if not FileAccess.file_exists(path):
        return output
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return output
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    if not parsed is Dictionary:
        push_error("Invalid collision data")
        return output
    var data: Dictionary = parsed
    if data.get("schemaVersion") != 1 or data.get("gridWidth") != 100 or data.get("gridHeight") != 100:
        push_error("Invalid collision dimensions")
        return output
    var rectangles: Variant = data.get("rectangles")
    if not rectangles is Array or rectangles.size() > 10000:
        return output
    for item in rectangles:
        if not item is Dictionary:
            return []
        var rect: Dictionary = item
        for key in ["x", "y", "width", "height"]:
            if not rect.has(key) or not rect[key] is int:
                return []
        if rect["x"] < 0 or rect["y"] < 0 or rect["width"] < 1 or rect["height"] < 1:
            return []
        if rect["x"] + rect["width"] > 100 or rect["y"] + rect["height"] > 100:
            return []
        output.append(rect)
    return output

static func add_colliders(parent: Node3D, rectangles: Array[Dictionary]) -> void:
    for rect in rectangles:
        var body := StaticBody3D.new()
        body.position = Vector3(float(rect["x"]) + float(rect["width"]) / 2.0 - 50.0, 0.6, float(rect["y"]) + float(rect["height"]) / 2.0 - 50.0)
        var shape := BoxShape3D.new()
        shape.size = Vector3(rect["width"], 1.2, rect["height"])
        var collider := CollisionShape3D.new()
        collider.shape = shape
        body.add_child(collider)
        var visual := MeshInstance3D.new()
        var cube := BoxMesh.new()
        cube.size = shape.size
        visual.mesh = cube
        var material := StandardMaterial3D.new()
        material.albedo_color = Color(0.7, 0.28, 0.25)
        visual.material_override = material
        body.add_child(visual)
        parent.add_child(body)
