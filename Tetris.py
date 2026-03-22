import pygame
import random

# Run the game 
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]]
]

# Shape Colors
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris by @DjentyDude")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.get_new_shape()
        self.current_color = random.choice(SHAPE_COLORS)
        self.shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        self.game_over = False

    def get_new_shape(self):
        return random.choice(SHAPES)

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_color, ((self.shape_x + x) * BLOCK_SIZE, (self.shape_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def move_shape(self, dx, dy):
        self.shape_x += dx
        self.shape_y += dy
        if self.check_collision():
            self.shape_x -= dx
            self.shape_y -= dy
            return False
        return True

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if self.check_collision():
            self.current_shape = [list(row) for row in zip(*self.current_shape)][::-1]

    def check_collision(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + self.shape_x < 0 or x + self.shape_x >= SCREEN_WIDTH // BLOCK_SIZE or y + self.shape_y >= SCREEN_HEIGHT // BLOCK_SIZE or self.grid[y + self.shape_y][x + self.shape_x] != BLACK:
                        return True
        return False

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.shape_y][x + self.shape_x] = self.current_color
        self.clear_lines()
        self.current_shape = self.get_new_shape()
        self.current_color = random.choice(SHAPE_COLORS)
        self.shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(lines_cleared)] + new_grid

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_shape()
            pygame.display.flip()

            for event in pygame.event.get(): #Controls
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_shape(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()

            if not self.move_shape(0, 1):
                self.lock_shape()

            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    Tetris().run()