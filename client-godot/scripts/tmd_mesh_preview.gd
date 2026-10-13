extends Node3D
# Experimental mesh preview: only polygon faces decoded from supported TMD packets.
const MODEL := "res://assets/characters/model_mesh.json"
const SCALE := 0.002

func _ready() -> void:
    var camera := Camera3D.new()
    add_child(camera)
    camera.position = Vector3(0, 2, 8)
    camera.look_at_from_position(camera.position, Vector3.ZERO)
    camera.current = true
    var environment := WorldEnvironment.new()
    add_child(environment)
    var env := Environment.new()
    env.background_mode = Environment.BG_COLOR
    env.background_color = Color(0.1, 0.12, 0.17)
    environment.environment = env
    _load_mesh()

func _load_mesh() -> void:
    if not FileAccess.file_exists(MODEL):
        push_warning("Missing local mesh JSON: " + MODEL)
        return
    var input := FileAccess.open(MODEL, FileAccess.READ)
    if input == null:
        return
    var document: Variant = JSON.parse_string(input.get_as_text())
    if not document is Dictionary or document.get("format", "") != "psx-tmd-experimental-unlit-mesh":
        push_error("Unsupported mesh export")
        return
    var objects: Variant = document.get("objects", [])
    if not objects is Array:
        return
    var faces_total := 0
    for object_data in objects:
        if not object_data is Dictionary:
            continue
        var vertices: Variant = object_data.get("vertices", [])
        var faces: Variant = object_data.get("faces", [])
        if not vertices is Array or not faces is Array:
            continue
        var surface := SurfaceTool.new()
        surface.begin(Mesh.PRIMITIVE_TRIANGLES)
        var count := 0
        for face in faces:
            if not face is Dictionary:
                continue
            var indices: Variant = face.get("indices", [])
            var rgb: Variant = face.get("rgb", [])
            if not indices is Array or indices.size() not in [3, 4] or not rgb is Array or rgb.size() != 3:
                continue
            var sequence := [0, 1, 2] if indices.size() == 3 else [0, 1, 2, 0, 2, 3]
            for vertex_id in sequence:
                var index := int(indices[vertex_id])
                if index < 0 or index >= vertices.size():
                    continue
                var coordinates: Variant = vertices[index]
                if not coordinates is Array or coordinates.size() != 3:
                    continue
                surface.set_color(Color(float(rgb[0]) / 255.0, float(rgb[1]) / 255.0, float(rgb[2]) / 255.0))
                surface.add_vertex(Vector3(float(coordinates[0]), -float(coordinates[1]), float(coordinates[2])) * SCALE)
                count += 1
        if count == 0:
            continue
        if count % 3 != 0:
            push_warning("Skipping malformed triangle stream")
            continue
        surface.generate_normals()
        var mesh := surface.commit()
        if mesh == null:
            continue
        var visual := MeshInstance3D.new()
        visual.mesh = mesh
        var mat := StandardMaterial3D.new()
        mat.vertex_color_use_as_albedo = true
        mat.cull_mode = BaseMaterial3D.CULL_DISABLED
        mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
        visual.material_override = mat
        add_child(visual)
        faces_total += count / 3
    print("Experimental TMD triangle preview: ", faces_total)
