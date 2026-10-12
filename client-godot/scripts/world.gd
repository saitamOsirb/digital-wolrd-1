extends Node3D

const CollisionMap = preload("res://scripts/collision_loader.gd")
const DIAGNOSTIC_FILE = "res://assets/diagnostic/collision.json"
const MapRenderer = preload("res://scripts/map_renderer.gd")

# Synthetic 3D test map. Does NOT reproduce an original DW1 stage.
func _ready() -> void:
    _add_floor()
    add_child(MapRenderer.new())
    var imported: Array[Dictionary] = CollisionMap.load_map(DIAGNOSTIC_FILE)
    if imported.is_empty():
        _add_block(Vector3(6, 1.0, 2), Vector3(3, 2, 3), Color(0.36, 0.51, 0.41))
        _add_block(Vector3(-5, 1.0, -4), Vector3(4, 2, 2), Color(0.45, 0.47, 0.66))
    else:
        CollisionMap.add_colliders(self, imported)
        print("Loaded diagnostic obstacles: ", imported.size())
    var sunlight := DirectionalLight3D.new()
    sunlight.rotation_degrees = Vector3(-45, -20, 0)
    add_child(sunlight)
    var environment := WorldEnvironment.new()
    var settings := Environment.new()
    settings.background_mode = Environment.BG_COLOR
    settings.background_color = Color(0.55, 0.76, 0.92)
    settings.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    settings.ambient_light_color = Color(0.85, 0.89, 0.91)
    environment.environment = settings
    add_child(environment)

func _add_floor() -> void:
    _add_block(Vector3(0, -0.5, 0), Vector3(100, 1, 100), Color(0.53, 0.71, 0.42))

func _add_block(origin: Vector3, size: Vector3, color: Color) -> void:
    var node := StaticBody3D.new()
    node.position = origin
    var collision := CollisionShape3D.new()
    var box := BoxShape3D.new()
    box.size = size
    collision.shape = box
    node.add_child(collision)
    var visual := MeshInstance3D.new()
    var mesh := BoxMesh.new()
    mesh.size = size
    visual.mesh = mesh
    var material := StandardMaterial3D.new()
    material.albedo_color = color
    visual.material_override = material
    node.add_child(visual)
    add_child(node)
