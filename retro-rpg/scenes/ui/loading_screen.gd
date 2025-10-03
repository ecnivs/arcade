extends Control

@export var loading_bar:TextureProgressBar

func _ready() -> void:
	Loader.loading_progress_updated.connect(_on_progress_updated)

func _on_progress_updated(percentage):
	loading_bar.value = percentage
