import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
GROUND_HEIGHT = 320  # Lowered ground height
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 130
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 60
GRAVITY = 0.7
JUMP_FORCE = -15
GAME_SPEED = 6
BACKGROUND_SCROLL_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
background_img = pygame.image.load("vecteezy_majestic-waterfall-cascading-down-mountainous-landscape-on_55652094.png")
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
player_sprite = pygame.image.load("pngwing.com (2).png")
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
obstacle_sprite = pygame.image.load("pngwing.com (1).png.png")
obstacle_sprite = pygame.transform.scale(obstacle_sprite, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Running Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_HEIGHT - PLAYER_HEIGHT
        self.vel_y = 0
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_FORCE
            self.is_jumping = True

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.y > GROUND_HEIGHT - PLAYER_HEIGHT:
            self.y = GROUND_HEIGHT - PLAYER_HEIGHT
            self.vel_y = 0
            self.is_jumping = False

        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(player_sprite, (self.x, self.y))

class Obstacle:
    def __init__(self):
        self.x = WINDOW_WIDTH
        self.y = GROUND_HEIGHT - OBSTACLE_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    def update(self):
        self.x -= GAME_SPEED
        self.rect.x = self.x

    def is_off_screen(self):
        return self.x < -OBSTACLE_WIDTH

    def draw(self, screen):
        screen.blit(obstacle_sprite, (self.x, self.y))


def main():
    player = Player()
    obstacles = []
    score = 0
    game_over = False
    last_obstacle = pygame.time.get_ticks()
    obstacle_interval = 1500
    bg_x = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    player = Player()
                    obstacles = []
                    score = 0
                    game_over = False
                    bg_x = 0

        if not game_over:
            player.update()
            bg_x -= BACKGROUND_SCROLL_SPEED
            if bg_x <= -WINDOW_WIDTH:
                bg_x = 0
            
            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle > obstacle_interval:
                obstacles.append(Obstacle())
                last_obstacle = current_time

            for obstacle in obstacles[:]:
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1
                if player.rect.colliderect(obstacle.rect):
                    game_over = True

        screen.blit(background_img, (bg_x, 0))
        screen.blit(background_img, (bg_x + WINDOW_WIDTH, 0))
        pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (WINDOW_WIDTH, GROUND_HEIGHT), 2)
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, RED)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, BLACK)
            screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
