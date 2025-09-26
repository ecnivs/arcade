from settings import *

class Fruit:
    def __init__(self, screen):
        self.screen = screen
        self.apple = pg.image.load(APPLE).convert_alpha()
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pg.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        self.screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,CELL_NUMBER-1)
        self.y = random.randint(0,CELL_NUMBER-1)
        self.pos = Vector2(self.x,self.y)
