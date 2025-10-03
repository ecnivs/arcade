extends TileMapLayer
class_name Map2d

enum terrain_data_types { TerrainType }

func _ready() -> void:
	print(get_terrain_data_for_tile(terrain_data_types.TerrainType, 0, 0))

func get_terrain_data_for_tile(data: int, x: int, y: int):
	var tile: TileData = get_cell_tile_data(Vector2i(x, y))
	
	if tile != null:
		return tile.get_custom_data(terrain_data_types.keys()[data])
	return null
