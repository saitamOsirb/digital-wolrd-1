extends Node2D
# Inspección del fondo original de DW1. Marcador y navegación son DIAGNÓSTICOS,
# no representan al protagonista ni la cámara/calibración auténticos.
const ORIGINAL_MAP := "res://assets/demo/map.png"
const MIN_ZOOM := 0.25
const MAX_ZOOM := 6.0
const MARKER_SPEED := 145.0

var picture: Sprite2D
var hint: Label
var marker: Node2D
var marker_position := Vector2.ZERO
var zoom_value := 1.0
var dragging := false
var follow_marker := false

func _ready() -> void:
    get_viewport().size_changed.connect(_fit_viewport)
    picture = Sprite2D.new()
    picture.centered = true
    picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    add_child(picture)
    marker = Node2D.new()
    marker.z_index = 10
    picture.add_child(marker)
    marker.draw.connect(_draw_marker)
    hint = Label.new()
    hint.position = Vector2(16, 12)
    hint.z_index = 20
    hint.add_theme_color_override("font_color", Color.WHITE)
    hint.add_theme_color_override("font_shadow_color", Color.BLACK)
    hint.add_theme_constant_override("shadow_offset_x", 2)
    hint.add_theme_constant_override("shadow_offset_y", 2)
    add_child(hint)
    _load_original_map()

func _draw_marker() -> void:
    marker.draw_circle(Vector2(0, 9), 7, Color(0, 0, 0, 0.5))
    marker.draw_circle(Vector2.ZERO, 7, Color(1, 0.8, 0.18))
    marker.draw_arc(Vector2.ZERO, 9, 0, TAU, 24, Color.BLACK, 2)
    marker.draw_line(Vector2(0, -12), Vector2(0, -22), Color(1, 0.8, 0.18), 2)

func _load_original_map() -> void:
    if not FileAccess.file_exists(ORIGINAL_MAP):
        hint.text = "MAPA ORIGINAL NO IMPORTADO\nEjecuta: python tools-python/import_original_map.py <BIN> --map TWNA01"
        marker.visible = false
        return
    var image := Image.new()
    var error := image.load(ProjectSettings.globalize_path(ORIGINAL_MAP))
    if error != OK:
        hint.text = "Error de mapa: " + str(error)
        marker.visible = false
        return
    picture.texture = ImageTexture.create_from_image(image)
    marker_position = image.get_size() * 0.5
    _update_marker()
    _fit_viewport()
    _update_hint()

func _map_size() -> Vector2:
    return picture.texture.get_size() if picture.texture != null else Vector2.ZERO

func _update_marker() -> void:
    marker.position = marker_position - _map_size() * 0.5

func _update_hint() -> void:
    if picture.texture == null:
        return
    hint.text = "TWNA01 | Fondo original PS1 | marcador de prueba (NO jugador real)\n" + "X: %.0f Y: %.0f | WASD/flechas: mover | Shift+clic: ubicar\n" % [marker_position.x, marker_position.y] + "R: encuadrar | F: seguimiento %s | rueda: zoom | arrastrar: mapa" % ("SI" if follow_marker else "NO")

func _process(delta: float) -> void:
    if picture.texture == null:
        return
    var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    if Input.is_key_pressed(KEY_A):
        direction.x = -1
    if Input.is_key_pressed(KEY_D):
        direction.x = 1
    if Input.is_key_pressed(KEY_W):
        direction.y = -1
    if Input.is_key_pressed(KEY_S):
        direction.y = 1
    if direction.length_squared() > 1:
        direction = direction.normalized()
    if direction.length_squared() > 0:
        marker_position += direction * MARKER_SPEED * delta
        marker_position = marker_position.clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
        _update_marker()
        if follow_marker:
            picture.position = get_viewport_rect().size * 0.5 - marker.position * zoom_value
        _update_hint()

func _fit_viewport() -> void:
    if picture == null or picture.texture == null:
        return
    var screen_size := get_viewport_rect().size
    var size := _map_size()
    zoom_value = clampf(min(screen_size.x / size.x, screen_size.y / size.y), MIN_ZOOM, MAX_ZOOM)
    picture.scale = Vector2.ONE * zoom_value
    picture.position = screen_size * 0.5

func _unhandled_input(event: InputEvent) -> void:
    if picture.texture == null:
        return
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT:
            if event.pressed and event.shift_pressed:
                var local := picture.to_local(event.position) + _map_size() * 0.5
                marker_position = local.clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
                _update_marker()
                _update_hint()
                dragging = false
            else:
                dragging = event.pressed
        elif event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP, MOUSE_BUTTON_WHEEL_DOWN]:
            var factor := 1.15 if event.button_index == MOUSE_BUTTON_WHEEL_UP else 1.0 / 1.15
            var old_zoom := zoom_value
            zoom_value = clampf(zoom_value * factor, MIN_ZOOM, MAX_ZOOM)
            picture.position = event.position + (picture.position - event.position) * (zoom_value / old_zoom)
            picture.scale = Vector2.ONE * zoom_value
    elif event is InputEventMouseMotion and dragging:
        picture.position += event.relative
    elif event is InputEventKey and event.pressed:
        if event.keycode == KEY_R:
            _fit_viewport()
        elif event.keycode == KEY_F:
            follow_marker = not follow_marker
            _update_hint()
