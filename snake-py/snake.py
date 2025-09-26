from settings import *

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction =  Vector2(1, 0)
        self.new_block = False
        self.on_init()

    def on_init(self):
        self.head_up = pg.image.load(HEAD_UP).convert_alpha()
        self.head_down = pg.image.load(HEAD_DOWN).convert_alpha()
        self.head_right = pg.image.load(HEAD_RIGHT).convert_alpha()
        self.head_left = pg.image.load(HEAD_LEFT).convert_alpha()

        self.tail_up = pg.image.load(TAIL_UP).convert_alpha()
        self.tail_down = pg.image.load(TAIL_DOWN).convert_alpha()
        self.tail_right = pg.image.load(TAIL_RIGHT).convert_alpha()
        self.tail_left = pg.image.load(TAIL_LEFT).convert_alpha()  

        self.body_vertical = pg.image.load(BODY_VER).convert_alpha()
        self.body_horizontal = pg.image.load(BODY_HOR).convert_alpha()

        self.body_tr = pg.image.load(BODY_TR).convert_alpha()
        self.body_tl = pg.image.load(BODY_TL).convert_alpha()
        self.body_br = pg.image.load(BODY_BR).convert_alpha()
        self.body_bl = pg.image.load(BODY_BL).convert_alpha()
        self.crunch_sound = pg.mixer.Sound(CRUNCH_WAV)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pg.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            if index == 0:
                self.screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                self.screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        self.screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        self.screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        self.screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        self.screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
