extends Control

func _on_new_game_button_pressed() -> void:
	Loader.load_scene(self, "res://scenes/game.tscn")
