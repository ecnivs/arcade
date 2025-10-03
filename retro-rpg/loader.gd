extends Node

signal loading_progress_updated(percentage)
@export var loading_scene = preload("res://scenes/ui/loading_screen.tscn").instantiate()

var scene_path

func load_scene(caller, path):
	scene_path = path
	
	get_tree().root.add_child(loading_scene)
	ResourceLoader.load_threaded_request(scene_path)
	
	caller.queue_free()

func _process(_delta):
	if scene_path != null:
		var progress = []
		var loader_status = ResourceLoader.load_threaded_get_status(scene_path, progress)
	
		if loader_status == ResourceLoader.THREAD_LOAD_LOADED:
			var loaded_scene = ResourceLoader.load_threaded_get(scene_path).instantiate()
			get_tree().root.remove_child(loading_scene)
			get_tree().root.add_child(loaded_scene)
			scene_path = null
		
		elif loader_status == ResourceLoader.THREAD_LOAD_IN_PROGRESS:
			loading_progress_updated.emit(progress[0])
