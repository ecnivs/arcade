extends PathFollow3D

@export var reward := 25
@export var speed: float = 5
@export var max_health: int = 5

@onready var bank = get_tree().get_first_node_in_group("bank")
@onready var base = get_tree().get_first_node_in_group("base")
@onready var animation_player: AnimationPlayer = $AnimationPlayer

var current_health: int:
	set(health_in):
		if health_in < current_health:
			animation_player.play("TakeDamage")
		current_health = health_in
		if current_health < 1:
			bank.gold += reward
			queue_free()

func _ready() -> void:
	current_health = max_health

func _process(delta: float) -> void:
	progress += delta * speed
	if progress_ratio == 1:
		base.take_damage()
		set_process(false)
