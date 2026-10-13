extends RefCounted
# User-provided transparent foregrounds. They do not claim to be decoded
# original PlayStation foreground masks: alpha PNGs are authored separately.
const BASE := "res://assets/maps/overlays/"

static func load_overlay(map_id: String) -> Texture2D:
    if map_id.is_empty() or "/" in map_id or "\\" in map_id or ".." in map_id:
        return null
    var path := BASE + map_id + ".png"
    if not FileAccess.file_exists(path):
        return null
    var img := Image.new()
    if img.load(ProjectSettings.globalize_path(path)) != OK:
        push_warning("Invalid foreground PNG: " + path)
        return null
    if img.get_width() <= 0 or img.get_height() <= 0:
        return null
    return ImageTexture.create_from_image(img)
