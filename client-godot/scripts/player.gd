extends CharacterBody3D

@export var walk_speed: float = 4.5
@export var run_multiplier: float = 1.6
@export var gravity_force: float = 20.0
var _visual: MeshInstance3D

func _ready() -> void:
    name = "Player"
    var shape := CapsuleShape3D.new()
    shape.radius = 0.32
    shape.height = 1.7
    var collider := CollisionShape3D.new()
    collider.shape = shape
    add_child(collider)

    _visual = MeshInstance3D.new()
    var body := CapsuleMesh.new()
    body.radius = 0.32
    body.height = 1.7
    _visual.mesh = body
    var material := StandardMaterial3D.new()
    material.albedo_color = Color(0.99, 0.68, 0.28)
    _visual.material_override = material
    add_child(_visual)

func _physics_process(delta: float) -> void:
    var input_direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    var direction := Vector3(input_direction.x, 0.0, input_direction.y)
    var speed := walk_speed * (run_multiplier if Input.is_key_pressed(KEY_SHIFT) else 1.0)
    velocity.x = direction.x * speed
    velocity.z = direction.z * speed
    if not is_on_floor():
        velocity.y -= gravity_force * delta
    else:
        velocity.y = 0.0
    if direction.length_squared() > 0.01:
        _visual.rotation.y = atan2(direction.x, direction.z)
    move_and_slide()
