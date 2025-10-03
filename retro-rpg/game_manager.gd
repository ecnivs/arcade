extends Node

var default_map_path: String = "res://scenes/tile_map.tscn"
var current_map_path: String

func start_new_game():
	current_map_path = default_map_path
