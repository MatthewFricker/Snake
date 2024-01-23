import pygame
from collections import deque
from random import choice

class Snake:
    def __init__(self, height=15, length=15):
        pygame.init()
        self.load_images()
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.snake_length = 2

        self.height = height
        self.length = length
        self.scale = self.images[0].get_width()
        self.window_height = self.scale * self.height
        self.window_width = self.scale * self.length

        self.new_game()

        self.window = pygame.display.set_mode((self.window_width, self.window_height+self.scale))
        self.clock = pygame.time.Clock()

        self.main_loop()

    def new_game(self):
        self.grid = [[0]*self.length for _ in range(self.height)]
        self.snake = deque()
        self.snake_direction = (0, 1)
        self.game_over = False
        for i in range(2):
            self.grid[self.height//2][3+i] = 1
            self.snake.append((3+i, self.height//2))
        self.grid[self.height//2][self.length-3] = 2
    
    def load_images(self):
        self.images = []
        for name in ["floor", "box", "target"]:
            self.images.append(pygame.image.load(name + ".png"))

    def main_loop(self):
        while not self.game_over:
            self.check_events()
            self.draw_window()
            self.move_snake(self.snake_direction[0], self.snake_direction[1])
            self.clock.tick_busy_loop(5)
        else:
            self.snake_direction = (0,0)
            game_over_text = self.game_font.render("Game Over!", True, (255, 0, 0))
            self.window.blit(game_over_text, (self.window_width//2-30, self.window_height//2-30))
            pygame.display.flip()
            pygame.time.wait(1000)
            exit()

        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake_direction[0] != 0:
                    self.snake_direction = (0, -1)
                if event.key == pygame.K_UP and self.snake_direction[1] != 0:
                    self.snake_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and self.snake_direction[0] != 0:
                    self.snake_direction = (0, 1)
                if event.key == pygame.K_DOWN and self.snake_direction[1] != 0:
                    self.snake_direction = (1, 0)
            if event.type == pygame.QUIT:
                exit()

    def move_snake(self, x, y):
        snake_head_y, snake_head_x = self.snake[-1]
        self.snake.append((snake_head_y + y, snake_head_x + x))
        if snake_head_x + x >= self.height or snake_head_x + x < 0 or snake_head_y + y >= self.length or snake_head_y + y < 0:
            self.game_over = True
            return
        new_head = self.grid[snake_head_x + x][snake_head_y + y]
        if new_head == 0:
            snake_tail_y, snake_tail_x = self.snake.popleft()
            self.grid[snake_tail_x][snake_tail_y] = 0
        elif new_head == 1:
            self.game_over = True
            return
        else:
            self.new_target()
            self.snake_length += 1
        self.grid[snake_head_x + x][snake_head_y + y] = 1
        

    def new_target(self):
        options = []
        for i in range(self.height):
            for j in range(self.length):
                if self.grid[i][j] == 0:
                    options.append((i,j))
        x, y = choice(options)
        self.grid[x][y] = 2

    def draw_window(self):
        self.window.fill((0, 0, 0))
        game_text = self.game_font.render("Snake Length: " + str(self.snake_length), True, (255, 255, 255))
        self.window.blit(game_text, (25, self.height*self.scale + 10))

        for x in range(self.height):
            for y in range(self.length):
                square = self.grid[x][y]
                self.window.blit(self.images[square], (y * self.scale, x * self.scale))

        pygame.display.flip()
    
if __name__ == "__main__":
    Snake()