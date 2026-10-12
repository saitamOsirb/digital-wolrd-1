extends Node3D
# Inspect a locally converted PNG on a plane in the Godot test scene.
# Never distributes proprietary textures.
const PREVIEW_PATH := "res://assets/diagnostic/texture.png"

func _ready() -> void:
    var image := Image.new()
    var file_path := ProjectSettings.globalize_path(PREVIEW_PATH)
    if not FileAccess.file_exists(PREVIEW_PATH):
        return
    var error := image.load(file_path)
    if error != OK:
        push_warning("Cannot load diagnostic texture: " + str(error))
        return
    var mesh_instance := MeshInstance3D.new()
    var plane := PlaneMesh.new()
    plane.size = Vector2(8.0, 8.0)
    mesh_instance.mesh = plane
    mesh_instance.position = Vector3(0.0, 0.025, -9.0)
    var material := StandardMaterial3D.new()
    material.albedo_texture = ImageTexture.create_from_image(image)
    material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.cull_mode = BaseMaterial3D.CULL_DISABLED
    mesh_instance.material_override = material
    add_child(mesh_instance)
    print("Diagnostic texture preview: ", image.get_width(), "x", image.get_height())
