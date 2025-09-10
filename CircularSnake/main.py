import pygame
import sys
import random
import math

class CircularSnake:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 1000
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.RINGS = 8
        self.SEGMENTS = 24
        self.FPS_BASE = 6

        self.COLORS = {
            'snake': (0, 100, 0),
            'snake_head': (200, 0, 0),
            'food': (255, 0, 0),
            'bg': (0, 100, 0),
            'grid': (40, 40, 40),
            'text': (255, 255, 255)
        }
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Circular Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        start_ring = self.RINGS // 2
        start_segment = 0
        self.snake = [
            (start_ring, start_segment),
            (start_ring, (start_segment - 1) % self.SEGMENTS)
        ]
        self.direction = (0, 1)
        self.food = None
        self.score = 0
        self.game_over = False
        self.spawn_food()

    def to_xy(self, ring, segment):
        radius_step = (self.WIDTH // 2 - 50) / self.RINGS
        radius = radius_step * (ring + 0.5)
        theta = 2 * math.pi * segment / self.SEGMENTS
        x = self.CENTER[0] + radius * math.cos(theta)
        y = self.CENTER[1] + radius * math.sin(theta)
        return int(x), int(y)

    def get_segment_size(self, ring):
        radius_step = (self.WIDTH // 2 - 50) / self.RINGS
        inner_radius = radius_step * ring
        outer_radius = radius_step * (ring + 1)
        radius = (inner_radius + outer_radius) / 2
        circumference = 2 * math.pi * radius
        segment_size = max(6, int(circumference / self.SEGMENTS * 0.4))
        return segment_size

    def spawn_food(self):
        while True:
            ring = random.randint(0, self.RINGS - 1)
            segment = random.randint(0, self.SEGMENTS - 1)
            if (ring, segment) not in self.snake:
                self.food = (ring, segment)
                break

    def move_snake(self):
        if self.game_over:
            return

        head_ring, head_segment = self.snake[0]
        d_ring, d_segment = self.direction
        new_ring = (head_ring + d_ring) % self.RINGS
        new_segment = (head_segment + d_segment) % self.SEGMENTS

        new_head = (new_ring, new_segment)
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_over and event.key == pygame.K_SPACE:
                self.reset_game()
                return

            new_direction = None
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                new_direction = (0, -1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                new_direction = (0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                new_direction = (-1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                new_direction = (1, 0)
            elif event.key == pygame.K_r:
                self.reset_game()
                return

            if new_direction and new_direction != (-self.direction[0], -self.direction[1]):
                self.direction = new_direction

    def draw_grid(self):
        radius_step = (self.WIDTH // 2 - 50) / self.RINGS
        for ring in range(self.RINGS + 1):
            radius = int(radius_step * ring)
            if radius > 5:
                pygame.draw.circle(self.screen, self.COLORS['grid'], 
                                 self.CENTER, radius, 1)

        for segment in range(self.SEGMENTS):
            angle = 2 * math.pi * segment / self.SEGMENTS - math.pi / self.SEGMENTS
            start_radius = radius_step * 0.1
            end_radius = radius_step * self.RINGS

            start_x = self.CENTER[0] + start_radius * math.cos(angle)
            start_y = self.CENTER[1] + start_radius * math.sin(angle)
            end_x = self.CENTER[0] + end_radius * math.cos(angle)
            end_y = self.CENTER[1] + end_radius * math.sin(angle)
            pygame.draw.line(self.screen, self.COLORS['grid'], 
                           (int(start_x), int(start_y)), (int(end_x), int(end_y)), 1)

    def draw_snake(self):
        for i, (ring, segment) in enumerate(self.snake):
            pos = self.to_xy(ring, segment)
            size = self.get_segment_size(ring)
            color = self.COLORS['snake_head'] if i == 0 else self.COLORS['snake']
            pygame.draw.circle(self.screen, color, pos, size // 2)
            pygame.draw.circle(self.screen, (255, 255, 255), pos, size // 2, 1)

    def draw_food(self):
        if self.food:
            pos = self.to_xy(*self.food)
            size = self.get_segment_size(self.food[0])
            pygame.draw.circle(self.screen, self.COLORS['food'], pos, size // 2)
            pulse = int(5 * math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.circle(self.screen, (255, 100, 100), pos, size // 2 + pulse, 2)

    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.COLORS['text'])
        self.screen.blit(score_text, (10, 10))
        controls = [
            "Arrow Keys / WASD: Move",
            "R: Restart",
            "Wraps: Center↔Outer, All directions!"
        ]

        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 24).render(control, True, (150, 150, 150))
            self.screen.blit(text, (10, 50 + i * 25))

        if self.game_over:
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, (255, 0, 0))
            score_text = pygame.font.Font(None, 48).render(f"Final Score: {self.score}", True, self.COLORS['text'])
            restart_text = self.font.render("Press SPACE to restart", True, self.COLORS['text'])

            self.screen.blit(game_over_text, 
                           (self.WIDTH//2 - game_over_text.get_width()//2, self.HEIGHT//2 - 100))
            self.screen.blit(score_text,
                           (self.WIDTH//2 - score_text.get_width()//2, self.HEIGHT//2 - 30))
            self.screen.blit(restart_text,
                           (self.WIDTH//2 - restart_text.get_width()//2, self.HEIGHT//2 + 20))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)

            self.move_snake()
            self.screen.fill(self.COLORS['bg'])
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_ui()
            pygame.display.flip()

            fps = self.FPS_BASE + len(self.snake) // 3
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CircularSnake()
    game.run()
