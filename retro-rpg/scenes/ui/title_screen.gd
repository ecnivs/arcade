extends Control

func _on_new_game_button_pressed() -> void:
	GameManager.start_new_game()
	Loader.load_scene(self, "res://scenes/game.tscn")
