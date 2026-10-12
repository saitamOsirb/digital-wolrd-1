extends Node2D
# Authentic DW1 backdrop viewer. Only user-extracted images, no synthesized map.
# Drag the map with the mouse; wheel zooms around the cursor.
const ORIGINAL_MAP := "res://assets/demo/map.png"
const MIN_ZOOM := 0.25
const MAX_ZOOM := 6.0

var picture: Sprite2D
var hint: Label
var zoom_value := 1.0
var dragging := false

func _ready() -> void:
    get_viewport().size_changed.connect(_fit_viewport)
    picture = Sprite2D.new()
    picture.centered = true
    picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    add_child(picture)
    hint = Label.new()
    hint.text = "DIGITAL WORLD 1 — Visualizador de escenarios PS1"
    hint.position = Vector2(16, 12)
    hint.add_theme_color_override("font_color", Color.WHITE)
    hint.add_theme_color_override("font_shadow_color", Color.BLACK)
    hint.add_theme_constant_override("shadow_offset_x", 2)
    hint.add_theme_constant_override("shadow_offset_y", 2)
    add_child(hint)
    _load_original_map()

func _load_original_map() -> void:
    if not FileAccess.file_exists(ORIGINAL_MAP):
        hint.text = "MAPA ORIGINAL NO IMPORTADO\nEjecuta: python tools-python/import_original_map.py <BIN> --map TWNA01\nEl PNG se guarda en client-godot/assets/demo/map.png"
        return
    var image := Image.new()
    var err := image.load(ProjectSettings.globalize_path(ORIGINAL_MAP))
    if err != OK:
        hint.text = "Error al abrir el PNG de mapa: " + str(err)
        return
    picture.texture = ImageTexture.create_from_image(image)
    hint.text = "TWNA01 — Fondo PS1 importado | rueda: zoom | arrastrar: mover | R: centrar"
    _fit_viewport()

func _fit_viewport() -> void:
    if picture == null or picture.texture == null:
        return
    var view_size := get_viewport_rect().size
    var image_size := picture.texture.get_size()
    zoom_value = min(view_size.x / image_size.x, view_size.y / image_size.y)
    zoom_value = clampf(zoom_value, MIN_ZOOM, MAX_ZOOM)
    picture.scale = Vector2.ONE * zoom_value
    picture.position = view_size * 0.5

func _unhandled_input(event: InputEvent) -> void:
    if picture.texture == null:
        return
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT:
            dragging = event.pressed
        elif event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP, MOUSE_BUTTON_WHEEL_DOWN]:
            var factor := 1.15 if event.button_index == MOUSE_BUTTON_WHEEL_UP else 1.0 / 1.15
            var old_zoom := zoom_value
            zoom_value = clampf(zoom_value * factor, MIN_ZOOM, MAX_ZOOM)
            var mouse := get_global_mouse_position()
            picture.position = mouse + (picture.position - mouse) * (zoom_value / old_zoom)
            picture.scale = Vector2.ONE * zoom_value
    if event is InputEventMouseMotion and dragging:
        picture.position += event.relative
    if event is InputEventKey and event.pressed and event.keycode == KEY_R:
        _fit_viewport()
