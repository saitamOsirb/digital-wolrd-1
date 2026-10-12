extends Node3D
# 2D map background rendered as a textured ground plane beneath 3D actors.
# A synthetic fallback renders immediately without requiring Python execution.
const MAP_FILE := "res://assets/demo/map.png"
const WORLD_SIZE := 32.0
const PIXELS := 512

func _ready() -> void:
    var image := Image.new()
    if FileAccess.file_exists(MAP_FILE):
        if image.load(ProjectSettings.globalize_path(MAP_FILE)) != OK:
            push_warning("Map PNG invalid, using procedural diagnostic map")
            image = _create_synthetic_map()
    else:
        image = _create_synthetic_map()
    var plane := MeshInstance3D.new()
    var mesh := PlaneMesh.new()
    mesh.size = Vector2(WORLD_SIZE, WORLD_SIZE * float(image.get_height()) / float(image.get_width()))
    plane.mesh = mesh
    plane.position.y = 0.015
    var material := StandardMaterial3D.new()
    material.albedo_texture = ImageTexture.create_from_image(image)
    material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.cull_mode = BaseMaterial3D.CULL_DISABLED
    plane.material_override = material
    add_child(plane)
    print("Map demo rendered: %dx%d" % [image.get_width(), image.get_height()])

func _create_synthetic_map() -> Image:
    var image := Image.create(PIXELS, PIXELS, false, Image.FORMAT_RGBA8)
    for y in range(PIXELS):
        for x in range(PIXELS):
            var variation := sin(float(x) / 39.0) * 0.03 + cos(float(y) / 33.0) * 0.02
            var color := Color(0.23, 0.47 + variation, 0.26)
            var road := abs(float(x) - 256.0 + 29.0 * sin(float(y) / 73.0)) < 47.0
            var pond := pow((float(x) - 135.0) / 110.0, 2) + pow((float(y) - 135.0) / 73.0, 2) < 1.0
            if road:
                color = Color(0.64, 0.55, 0.36)
            elif pond:
                color = Color(0.18, 0.46, 0.61)
            elif (x * 17 + y * 31) % 97 < 3:
                color = Color(0.42, 0.6, 0.28)
            image.set_pixel(x, y, color)
    return image
