extends Node2D
# Optional locally imported character animation sheet, not bundled game content.
# Layout: 4 columns of walking frames and 4 rows ordered down,left,right,up.
const SHEET := "res://assets/characters/tamer_walk.png"
const FRAMES := 4
const DIRECTIONS := 4

var loaded := false
var frame_size := Vector2i.ZERO
var direction_row := 0
var frame_index := 0
var walking := false
var phase := 0.0
var texture: Texture2D

func _ready() -> void:
    texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    _load_sheet()

func _load_sheet() -> void:
    if not FileAccess.file_exists(SHEET):
        return
    var image := Image.new()
    if image.load(ProjectSettings.globalize_path(SHEET)) != OK:
        push_warning("Invalid local character sheet")
        return
    if image.get_width() % FRAMES != 0 or image.get_height() % DIRECTIONS != 0:
        push_warning("Character sheet must have 4 columns and 4 rows")
        return
    frame_size = Vector2i(image.get_width() / FRAMES, image.get_height() / DIRECTIONS)
    texture = ImageTexture.create_from_image(image)
    loaded = true
    queue_redraw()

func update_motion(direction: Vector2, delta: float) -> void:
    walking = direction.length_squared() > 0.001
    if walking:
        if absf(direction.x) > absf(direction.y):
            direction_row = 2 if direction.x > 0 else 1
        else:
            direction_row = 0 if direction.y > 0 else 3
        phase += delta * 8.0
        frame_index = int(phase) % FRAMES
    else:
        phase = 0.0
        frame_index = 0
    queue_redraw()

func _draw() -> void:
    if not loaded:
        return
    var size := Vector2(frame_size)
    var source := Rect2(Vector2(frame_index * frame_size.x, direction_row * frame_size.y), size)
    # Anchor at feet, not character center.
    draw_texture_rect_region(texture, Rect2(-size.x * 0.5, -size.y, size.x, size.y), source)
