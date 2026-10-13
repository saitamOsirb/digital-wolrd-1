extends Node2D
# Inspección del fondo original de DW1. Marcador y navegación son DIAGNÓSTICOS,
# no representan al protagonista ni la cámara/calibración auténticos.
const ORIGINAL_MAP := "res://assets/demo/map.png"
const CATALOG_PATH := "res://assets/maps/catalog.json"
const MAP_BASE := "res://assets/maps/"
const ORIGINAL_METADATA := "res://assets/demo/map.json"
const MIN_ZOOM := 0.25
const MAX_ZOOM := 6.0
const MARKER_SPEED := 145.0
const WalkZones = preload("res://scripts/map_walk_zones.gd")
const ZONES_PATH := "res://assets/maps/walk_zones.json"
const MapTransitions = preload("res://scripts/map_transitions.gd")
const LINKS_PATH := "res://assets/maps/transitions.json"
const ZoneEditor = preload("res://scripts/map_zone_editor.gd")
const MapPathfinding = preload("res://scripts/map_pathfinding.gd")
const ExplorationSave = preload("res://scripts/exploration_save.gd")
const MapForegrounds = preload("res://scripts/map_foregrounds.gd")
const TamerSprite = preload("res://scripts/tamer_sprite_preview.gd")

var picture: Sprite2D
var hint: Label
var marker: Node2D
var zone_overlay: Node2D
var foreground: Sprite2D
var tamer_sprite: Node2D
var marker_position := Vector2.ZERO
var zoom_value := 1.0
var dragging := false
var follow_marker := false
var map_label := "Mapa original"
var catalog_maps: Array[Dictionary] = []
var catalog_index := 0
var blocked_zones: Array[PackedVector2Array] = []
var collisions_enabled := true
var transition_zones: Array[Dictionary] = []
var transition_cooldown := 0.0
var show_debug_zones := false
var editing_zones := false
var draft_vertices := PackedVector2Array()
var walking_path := PackedVector2Array()
var path_step := 0

func _ready() -> void:
    get_viewport().size_changed.connect(_fit_viewport)
    picture = Sprite2D.new()
    picture.centered = true
    picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    add_child(picture)
    zone_overlay = Node2D.new()
    zone_overlay.z_index = 5
    picture.add_child(zone_overlay)
    zone_overlay.draw.connect(_draw_zones)
    zone_overlay.visible = false
    marker = Node2D.new()
    marker.z_index = 10
    picture.add_child(marker)
    marker.draw.connect(_draw_marker)
    tamer_sprite = TamerSprite.new()
    marker.add_child(tamer_sprite)
    foreground = Sprite2D.new()
    foreground.centered = true
    foreground.z_index = 15
    foreground.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
    picture.add_child(foreground)
    hint = Label.new()
    hint.position = Vector2(16, 12)
    hint.z_index = 20
    hint.add_theme_color_override("font_color", Color.WHITE)
    hint.add_theme_color_override("font_shadow_color", Color.BLACK)
    hint.add_theme_constant_override("shadow_offset_x", 2)
    hint.add_theme_constant_override("shadow_offset_y", 2)
    add_child(hint)
    _load_catalog()
    _load_original_map()
    _restore_session()

func _save_session() -> void:
    if picture.texture == null:
        return
    if ExplorationSave.write_state(map_label, marker_position, follow_marker, zoom_value):
        print("Exploration position saved: ", map_label)

func _restore_session() -> void:
    var state: Dictionary = ExplorationSave.read_state()
    if state.is_empty():
        return
    var destination_id: String = state["mapId"]
    if not catalog_maps.is_empty():
        var found := -1
        for i in range(catalog_maps.size()):
            if str(catalog_maps[i]["name"]) == destination_id:
                found = i
                break
        if found < 0:
            return
        catalog_index = found
        _load_original_map()
    elif map_label != destination_id:
        return
    if picture.texture == null:
        return
    marker_position = (state["position"] as Vector2).clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
    follow_marker = state["follow"]
    zoom_value = state["zoom"]
    picture.scale = Vector2.ONE * zoom_value
    _update_marker()
    if follow_marker:
        picture.position = get_viewport_rect().size * 0.5 - marker.position * zoom_value
    _update_hint()

func _draw_zones() -> void:
    if picture.texture == null:
        return
    var displacement := -_map_size() * 0.5
    for polygon in blocked_zones:
        var shifted := PackedVector2Array()
        for point in polygon:
            shifted.append(point + displacement)
        if shifted.size() >= 3:
            zone_overlay.draw_colored_polygon(shifted, Color(0.95, 0.12, 0.12, 0.22))
            for i in range(shifted.size()):
                zone_overlay.draw_line(shifted[i], shifted[(i + 1) % shifted.size()], Color(1.0, 0.18, 0.18), 2.0)
    if draft_vertices.size() > 0:
        for i in range(draft_vertices.size()):
            var point := draft_vertices[i] + displacement
            zone_overlay.draw_circle(point, 3.0, Color.YELLOW)
            if i > 0:
                zone_overlay.draw_line(draft_vertices[i - 1] + displacement, point, Color.YELLOW, 2.0)
    if walking_path.size() > 0:
        for i in range(1, walking_path.size()):
            zone_overlay.draw_line(walking_path[i - 1] + displacement, walking_path[i] + displacement, Color(0.2, 0.55, 1.0, 0.9), 2.0)
    for link in transition_zones:
        var box: Rect2 = link["rect"]
        zone_overlay.draw_rect(Rect2(box.position + displacement, box.size), Color(0.1, 0.95, 0.7, 0.3), true)
        zone_overlay.draw_rect(Rect2(box.position + displacement, box.size), Color(0.12, 1.0, 0.7), false, 2.0)

func _draw_marker() -> void:
    if tamer_sprite != null and tamer_sprite.loaded:
        return
    marker.draw_circle(Vector2(0, 9), 7, Color(0, 0, 0, 0.5))
    marker.draw_circle(Vector2.ZERO, 7, Color(1, 0.8, 0.18))
    marker.draw_arc(Vector2.ZERO, 9, 0, TAU, 24, Color.BLACK, 2)
    marker.draw_line(Vector2(0, -12), Vector2(0, -22), Color(1, 0.8, 0.18), 2)

func _load_catalog() -> void:
    if not FileAccess.file_exists(CATALOG_PATH):
        return
    var file := FileAccess.open(CATALOG_PATH, FileAccess.READ)
    if file == null:
        return
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    if not parsed is Dictionary:
        return
    var items: Variant = parsed.get("maps")
    if not items is Array or items.size() > 2000:
        return
    for entry in items:
        if not entry is Dictionary:
            continue
        var image_path: Variant = entry.get("image", "")
        var label: Variant = entry.get("name", "")
        if image_path is String and label is String and image_path.length() > 0 and label.length() > 0:
            if ".." not in image_path and not image_path.begins_with("/"):
                catalog_maps.append({"image": image_path, "name": label})

func _selected_path() -> String:
    if catalog_maps.is_empty():
        return ORIGINAL_MAP
    return MAP_BASE + str(catalog_maps[catalog_index]["image"])

func _change_map(direction: int) -> void:
    if catalog_maps.is_empty():
        return
    catalog_index = posmod(catalog_index + direction, catalog_maps.size())
    _load_original_map()

func _load_original_map() -> void:
    var selected_path := _selected_path()
    if not FileAccess.file_exists(selected_path):
        hint.text = "MAPA ORIGINAL NO IMPORTADO\nEjecuta: python tools-python/import_original_map.py <BIN> --map TWNA01"
        marker.visible = false
        return
    var image := Image.new()
    var error := image.load(ProjectSettings.globalize_path(selected_path))
    if error != OK:
        hint.text = "Error de mapa: " + str(error)
        marker.visible = false
        return
    picture.texture = ImageTexture.create_from_image(image)
    map_label = str(catalog_maps[catalog_index]["name"]) if not catalog_maps.is_empty() else "Mapa original"
    if catalog_maps.is_empty() and FileAccess.file_exists(ORIGINAL_METADATA):
        var metadata_file := FileAccess.open(ORIGINAL_METADATA, FileAccess.READ)
        if metadata_file != null:
            var parsed: Variant = JSON.parse_string(metadata_file.get_as_text())
            if parsed is Dictionary:
                var value: Variant = parsed.get("mapId", "")
                if value is String and not value.is_empty():
                    map_label = value
    marker.visible = true
    foreground.texture = MapForegrounds.load_overlay(map_label)
    if foreground.texture != null and foreground.texture.get_size() != picture.texture.get_size():
        push_warning("Foreground dimensions do not match background: " + map_label)
        foreground.texture = null
    blocked_zones = WalkZones.load_polygons(ZONES_PATH, map_label)
    transition_zones = MapTransitions.load_links(LINKS_PATH, map_label)
    draft_vertices.clear()
    walking_path.clear()
    path_step = 0
    zone_overlay.queue_redraw()
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
    hint.text = map_label + " | Fondo original PS1 | marcador de prueba (NO jugador real)\n" + "X: %.0f Y: %.0f | WASD/flechas: mover | Shift+clic: ubicar\n" % [marker_position.x, marker_position.y] + "PgUp/PgDown: mapa | F: seguir %s | C: colisión %s | V: ver zonas" % [("SI" if follow_marker else "NO"), ("ON" if collisions_enabled else "OFF")]

func _process(delta: float) -> void:
    if picture.texture == null:
        return
    transition_cooldown = maxf(0.0, transition_cooldown - delta)
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
        walking_path.clear()
        path_step = 0
        zone_overlay.queue_redraw()
    elif path_step < walking_path.size():
        var target: Vector2 = walking_path[path_step]
        tamer_sprite.update_motion(target - marker_position, delta)
        if marker_position.distance_to(target) <= MARKER_SPEED * delta:
            marker_position = target
            path_step += 1
            if path_step >= walking_path.size():
                walking_path.clear()
                path_step = 0
                zone_overlay.queue_redraw()
        else:
            marker_position = marker_position.move_toward(target, MARKER_SPEED * delta)
        _update_marker()
        if transition_cooldown <= 0.0:
            _try_transition()
        if follow_marker:
            picture.position = get_viewport_rect().size * 0.5 - marker.position * zoom_value
        _update_hint()
    if direction.length_squared() > 0:
        tamer_sprite.update_motion(direction, delta)
        var offset := direction * MARKER_SPEED * delta
        var goal := (marker_position + offset).clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
        if not collisions_enabled or not WalkZones.is_blocked(goal, blocked_zones):
            marker_position = goal
        else:
            var horizontal := Vector2(goal.x, marker_position.y)
            var vertical := Vector2(marker_position.x, goal.y)
            if not WalkZones.is_blocked(horizontal, blocked_zones):
                marker_position = horizontal
            elif not WalkZones.is_blocked(vertical, blocked_zones):
                marker_position = vertical
        if transition_cooldown <= 0.0:
            _try_transition()
        _update_marker()
        if follow_marker:
            picture.position = get_viewport_rect().size * 0.5 - marker.position * zoom_value
        _update_hint()
    elif path_step >= walking_path.size():
        tamer_sprite.update_motion(Vector2.ZERO, delta)

func _try_transition() -> void:
    var link := MapTransitions.destination(marker_position, transition_zones)
    if link.is_empty():
        return
    var requested: String = link["to"]
    var index := -1
    for i in range(catalog_maps.size()):
        if str(catalog_maps[i]["name"]) == requested:
            index = i
            break
    if index < 0:
        push_warning("Destination map not imported: " + requested)
        transition_cooldown = 1.0
        return
    var spawn: Vector2 = link["spawn"]
    catalog_index = index
    _load_original_map()
    marker_position = spawn.clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
    walking_path.clear()
    path_step = 0
    _update_marker()
    transition_cooldown = 1.0
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
        if event.button_index == MOUSE_BUTTON_RIGHT and event.pressed and not editing_zones:
            var target := (picture.to_local(event.position) + _map_size() * 0.5).clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
            var obstacles: Array[PackedVector2Array] = blocked_zones if collisions_enabled else []
            walking_path = MapPathfinding.find_path(marker_position, target, _map_size(), obstacles)
            path_step = 1 if walking_path.size() > 1 else 0
            if walking_path.size() == 1:
                walking_path.clear()
            zone_overlay.queue_redraw()
            return
        if editing_zones and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            draft_vertices.append(picture.to_local(event.position) + _map_size() * 0.5)
            zone_overlay.queue_redraw()
            return
        if event.button_index == MOUSE_BUTTON_LEFT:
            if event.pressed and event.shift_pressed:
                var local := picture.to_local(event.position) + _map_size() * 0.5
                var goal := local.clamp(Vector2.ZERO, _map_size() - Vector2.ONE)
                if not collisions_enabled or not WalkZones.is_blocked(goal, blocked_zones):
                    marker_position = goal
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
        elif event.keycode == KEY_PAGEUP:
            _change_map(-1)
        elif event.keycode == KEY_PAGEDOWN:
            _change_map(1)
        elif event.keycode == KEY_C:
            collisions_enabled = not collisions_enabled
            _update_hint()
        elif event.keycode == KEY_F5:
            _save_session()
        elif event.keycode == KEY_F9:
            _restore_session()
        elif event.keycode == KEY_V:
            show_debug_zones = not show_debug_zones
            zone_overlay.visible = show_debug_zones or editing_zones
            zone_overlay.queue_redraw()
        elif event.keycode == KEY_E:
            editing_zones = not editing_zones
            draft_vertices.clear()
            dragging = false
            zone_overlay.visible = show_debug_zones or editing_zones
            zone_overlay.queue_redraw()
            print("Polygon editing: ", editing_zones)
        elif editing_zones and event.keycode == KEY_ENTER:
            if draft_vertices.size() >= 3:
                blocked_zones.append(draft_vertices.duplicate())
                if ZoneEditor.save_polygons(ZONES_PATH, map_label, blocked_zones):
                    print("Saved blocked polygon for ", map_label)
                else:
                    push_error("Could not save walk zones")
            draft_vertices.clear()
            zone_overlay.queue_redraw()
        elif editing_zones and event.keycode == KEY_BACKSPACE:
            if draft_vertices.size() > 0:
                draft_vertices.remove_at(draft_vertices.size() - 1)
            zone_overlay.queue_redraw()
        elif editing_zones and event.keycode == KEY_ESCAPE:
            draft_vertices.clear()
            zone_overlay.queue_redraw()
