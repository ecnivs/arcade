from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from settings import *

app = Ursina()

# Load assets
grass_texture = load_texture(grass_texture)
stone_texture = load_texture(stone_texture)
brick_texture = load_texture(brick_texture)
dirt_texture = load_texture(dirt_texture)
sky_texture = load_texture(sky_texture)
arm_texture = load_texture(arm_texture)
punch_sound = Audio(punch_sound, loop=False, autoplay=False)

# game variables
current_block = 1
tab = False

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                new_position = self.position + mouse.normal

                if (new_position - player.position).length() > 1:
                    if current_block == 1:
                        Voxel(position=new_position, texture=grass_texture)
                    elif current_block == 2:
                        Voxel(position=new_position, texture=dirt_texture)
                    elif current_block == 3:
                        Voxel(position=new_position, texture=stone_texture)
                    elif current_block == 4:
                        Voxel(position=new_position, texture=brick_texture)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

class Bedrock(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=stone_texture,
            color=color.color(0, 0, 0.4),
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                new_position = self.position + mouse.normal

                if (new_position - player.position).length() > 1:
                    if current_block == 1:
                        Voxel(position=new_position, texture=grass_texture)
                    elif current_block == 2:
                        Voxel(position=new_position, texture=dirt_texture)
                    elif current_block == 3:
                        Voxel(position=new_position, texture=stone_texture)
                    elif current_block == 4:
                        Voxel(position=new_position, texture=brick_texture)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)

class Hand(Entity):
    # Hand
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

class Chunk(Entity):
    def __init__(self, position=(0, 0, 0), size=render_distance):
        super().__init__(position=position)
        self.size = size
        self.voxels = []
        self.create_voxels()

    def create_voxels(self):
        for z in range(self.size):
            for x in range(self.size):
                voxel = Voxel(position=(self.x + x, 0, self.z + z), texture=grass_texture)
                self.voxels.append(voxel)
                Voxel(position=(self.x + x, -1, self.z + z), texture=dirt_texture)
                Voxel(position=(self.x + x, -2, self.z + z), texture=dirt_texture)
                Bedrock(position=(self.x + x, -3, self.z + z))

# main game loop
def update():
    global current_block
    global tab

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    
    # change block
    if held_keys['1']:
        current_block = 1
    elif held_keys['2']:
        current_block = 2
    elif held_keys['3']:
        current_block = 3
    elif held_keys['4']:
        current_block = 4

    # respawn location
    if player.y < -10:
        voxel = Voxel(position=(1, -1, 1))
        player.y = +3
        player.x = 0

    if held_keys['tab'] and not tab:
        tab = True
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible
    elif not held_keys['tab']:
        tab = False

if __name__ == "__main__":
    player = FirstPersonController()
    sky = Sky()
    hand = Hand()

    chunks = []
    for z in range(-1, 2):
        for x in range(-1, 2):
            chunk_position = (x * render_distance, 0, z * render_distance)
            chunk = Chunk(position=chunk_position, size=render_distance)
            chunks.append(chunk)

    app.run()
