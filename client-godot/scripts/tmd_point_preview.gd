extends Node3D
# Read-only 3D structural preview for PS1 TMD vertices; no polygon reconstruction.
const CLOUD_FILE := "res://assets/characters/model_vertices.json"
const DISPLAY_SCALE := 0.002
const MAX_POINTS := 200000

func _ready() -> void:
    var info := Label3D.new()
    info.text = "TMD vertex diagnostic (not a complete character mesh)"
    info.position = Vector3(-1.5, 2.6, 0)
    info.font_size = 40
    add_child(info)
    _load_points()
    var camera := Camera3D.new()
    camera.position = Vector3(0, 2.5, 8)
    camera.look_at_from_position(camera.position, Vector3.ZERO)
    camera.current = true
    add_child(camera)
    var ambient := WorldEnvironment.new()
    var world := Environment.new()
    world.background_mode = Environment.BG_COLOR
    world.background_color = Color(0.08, 0.1, 0.14)
    ambient.environment = world
    add_child(ambient)

func _load_points() -> void:
    if not FileAccess.file_exists(CLOUD_FILE):
        push_warning("Import local TMD vertices first: " + CLOUD_FILE)
        return
    var file := FileAccess.open(CLOUD_FILE, FileAccess.READ)
    if file == null:
        return
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    if not parsed is Dictionary or parsed.get("format", "") != "psx-tmd-vertex-cloud":
        push_warning("Not a valid TMD vertex export")
        return
    var entries: Variant = parsed.get("objects", [])
    if not entries is Array:
        return
    var mesh := ImmediateMesh.new()
    var count := 0
    mesh.surface_begin(Mesh.PRIMITIVE_POINTS)
    for entry in entries:
        if not entry is Dictionary:
            continue
        var vertices: Variant = entry.get("vertices", [])
        if not vertices is Array:
            continue
        for point in vertices:
            if not point is Array or point.size() != 3:
                continue
            if count >= MAX_POINTS:
                break
            if not (point[0] is float or point[0] is int):
                continue
            var vertex := Vector3(float(point[0]), -float(point[1]), float(point[2])) * DISPLAY_SCALE
            mesh.surface_add_vertex(vertex)
            count += 1
    mesh.surface_end()
    if count == 0:
        push_warning("TMD export contains no vertices")
        return
    var instance := MeshInstance3D.new()
    instance.mesh = mesh
    var material := StandardMaterial3D.new()
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.albedo_color = Color(0.95, 0.8, 0.24)
    material.use_point_size = true
    material.point_size = 4.0
    instance.material_override = material
    add_child(instance)
    print("TMD vertex points rendered: ", count)
