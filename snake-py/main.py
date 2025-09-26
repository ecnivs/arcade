from settings import *
from snake import Snake
from fruit import Fruit

class Core:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.last_direction_change_time = 0
        self.direction_change_cooldown = 200

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.snake = Snake(self.screen)
        self.fruit = Fruit(self.screen)
        self.grass_color = (167, 209, 61)
        self.font = pg.font.Font(FONT, 25)

    def render(self):
        self.screen.fill((175,215,70))
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.check_fail()
        pg.display.flip()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= CELL_NUMBER or not 0 <= self.snake.body[0].y <= CELL_NUMBER:
            self.is_running = False
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block :
                self.is_running = False

    def draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pg.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pg.draw.rect(self.screen, self.grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pg.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pg.draw.rect(self.screen, self.grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.font.render(score_text, True,(56, 47, 12))
        score_rect = score_surface.get_rect(center = (50, 30))
        apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left, score_rect.centery))

        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.fruit.apple, apple_rect)

    def update(self):
        self.snake.move_snake()
        self.check_collision()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')

    def handle_events(self):
        current_time = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False

            if event.type == UPDATE:
                self.update()

        keys = pg.key.get_pressed()

        if current_time - self.last_direction_change_time > self.direction_change_cooldown:
            if keys[pg.K_UP] and self.snake.direction.y != 1:
                self.snake.direction = Vector2(0, -1)
                self.last_direction_change_time = current_time
            if keys[pg.K_DOWN] and self.snake.direction.y != -1:
                self.snake.direction = Vector2(0, 1)
                self.last_direction_change_time = current_time
            if keys[pg.K_LEFT] and self.snake.direction.x != 1:
                self.snake.direction = Vector2(-1, 0)
                self.last_direction_change_time = current_time
            if keys[pg.K_RIGHT] and self.snake.direction.x != -1:
                self.snake.direction = Vector2(1, 0)
                self.last_direction_change_time = current_time

        pg.display.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.render()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    core = Core()
    UPDATE = pg.USEREVENT # custom event to call update function
    pg.time.set_timer(UPDATE, 150) # every 150 ms
    core.run()
