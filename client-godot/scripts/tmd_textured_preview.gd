extends Node3D
# Preview for locally converted TMD+TIM resources (FT3/FT4 only).
# This is NOT a verified Digimon World 1 tamer or animation loader.
const MANIFEST := "res://assets/characters/preview/model.json"
const BASE := "res://assets/characters/preview/"
const MODEL_SCALE := 0.002
var rotation_speed := 0.35
var model_root: Node3D

func _ready() -> void:
    model_root = Node3D.new()
    add_child(model_root)
    var camera := Camera3D.new()
    add_child(camera)
    camera.position = Vector3(0, 2.3, 7)
    camera.look_at_from_position(camera.position, Vector3.ZERO)
    camera.current = true
    var environment := WorldEnvironment.new()
    add_child(environment)
    var env := Environment.new()
    env.background_mode = Environment.BG_COLOR
    env.background_color = Color(0.08, 0.09, 0.12)
    environment.environment = env
    _load_preview()

func _process(delta: float) -> void:
    model_root.rotate_y(delta * rotation_speed)

func _load_preview() -> void:
    if not FileAccess.file_exists(MANIFEST):
        push_warning("Run tools-python/build_godot_character_preview.py with local PS1 resources")
        return
    var file := FileAccess.open(MANIFEST, FileAccess.READ)
    if file == null:
        return
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    if not parsed is Dictionary or parsed.get("format", "") != "dw1-textured-preview":
        push_error("Invalid preview manifest")
        return
    var material_cache: Dictionary = {}
    var pages: Variant = parsed.get("pages", {})
    if not pages is Dictionary:
        return
    for page_key in pages:
        var name := str(pages[page_key])
        if "/" in name or "\\" in name or ".." in name:
            continue
        var path := BASE + name
        if not FileAccess.file_exists(path):
            continue
        var image := Image.new()
        if image.load(ProjectSettings.globalize_path(path)) != OK:
            continue
        var mat := StandardMaterial3D.new()
        mat.albedo_texture = ImageTexture.create_from_image(image)
        mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
        mat.cull_mode = BaseMaterial3D.CULL_DISABLED
        mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
        material_cache[str(page_key)] = mat
    var objects: Variant = parsed.get("objects", [])
    if not objects is Array:
        return
    var triangles_total := 0
    for obj in objects:
        if not obj is Dictionary:
            continue
        var verts: Variant = obj.get("vertices", [])
        var faces: Variant = obj.get("faces", [])
        if not verts is Array or not faces is Array:
            continue
        var per_page: Dictionary = {}
        for face in faces:
            if not face is Dictionary:
                continue
            var page_key := str(face.get("page", ""))
            if not material_cache.has(page_key):
                continue
            var indices: Variant = face.get("indices", [])
            var uv: Variant = face.get("uvRaw", [])
            if not indices is Array or indices.size() not in [3, 4] or not uv is Array or uv.size() != indices.size():
                continue
            var valid := true
            for value in indices:
                if not value is int or value < 0 or value >= verts.size():
                    valid = false
                    break
            if not valid:
                continue
            if not per_page.has(page_key):
                per_page[page_key] = []
            var corners := [0, 2, 1] if indices.size() == 3 else [0, 2, 1, 0, 3, 2]
            for corner in corners:
                var position: Variant = verts[indices[corner]]
                var coord: Variant = uv[corner]
                if not position is Array or position.size() != 3 or not coord is Array or coord.size() != 2:
                    valid = false
                    break
                per_page[page_key].append({"position": position, "uv": coord})
            if not valid:
                per_page[page_key].clear()
        for page_key in per_page:
            var records: Array = per_page[page_key]
            if records.is_empty() or records.size() % 3 != 0:
                continue
            var surface := SurfaceTool.new()
            surface.begin(Mesh.PRIMITIVE_TRIANGLES)
            for item in records:
                var p: Array = item["position"]
                var uv: Array = item["uv"]
                surface.set_uv(Vector2((float(uv[0]) + 0.5) / 256.0, (float(uv[1]) + 0.5) / 256.0))
                surface.add_vertex(Vector3(float(p[0]), -float(p[1]), float(p[2])) * MODEL_SCALE)
            var mesh := surface.commit()
            if mesh != null:
                var instance := MeshInstance3D.new()
                instance.mesh = mesh
                instance.material_override = material_cache[page_key]
                model_root.add_child(instance)
                triangles_total += records.size() / 3
    print("Experimental TMD preview triangles: ", triangles_total)
