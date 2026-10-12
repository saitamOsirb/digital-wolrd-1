extends Node3D
# Display a composited 2D map on the ground; characters remain 3D.
const MAP_FILE := "res://assets/demo/map.png"
const WORLD_SIZE := 32.0

func _ready() -> void:
    if not FileAccess.file_exists(MAP_FILE):
        print("No map PNG: run python tools-python/render_map_demo.py")
        return
    var image := Image.new()
    if image.load(ProjectSettings.globalize_path(MAP_FILE)) != OK:
        push_error("Could not load map image")
        return
    var plane := MeshInstance3D.new()
    var mesh := PlaneMesh.new()
    mesh.size = Vector2(WORLD_SIZE, WORLD_SIZE)
    plane.mesh = mesh
    plane.position.y = 0.015
    var material := StandardMaterial3D.new()
    material.albedo_texture = ImageTexture.create_from_image(image)
    material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.cull_mode = BaseMaterial3D.CULL_DISABLED
    plane.material_override = material
    add_child(plane)
    print("Map rendered: %dx%d PNG" % [image.get_width(), image.get_height()])
