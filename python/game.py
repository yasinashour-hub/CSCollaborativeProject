import pygame
import random

# Setup
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define font size
font = pygame.font.Font(None, 74) 

score_a = 0
score_b = 0

# Constants
GREEN, WHITE, YELLOW, BLACK = (34, 139, 34), (255, 255, 255), (255, 255, 0), (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, up_key, down_key):
        super().__init__()
        self.image = pygame.Surface((15, 80))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, HEIGHT // 2))
        self.up_key, self.down_key = up_key, down_key

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]: self.rect.y -= 7
        if keys[self.down_key]: self.rect.y += 7
        self.rect.clamp_ip(screen.get_rect())

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = random.choice([-6, 6])
        self.dy = random.choice([-4, 4])

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Bounce off top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

# Objects
p1 = Player(50, pygame.K_w, pygame.K_s)
p2 = Player(WIDTH - 50, pygame.K_UP, pygame.K_DOWN)
ball = Ball()
all_sprites = pygame.sprite.Group(p1, p2, ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    all_sprites.update()

    # Collision logic
    if pygame.sprite.collide_rect(ball, p1) or pygame.sprite.collide_rect(ball, p2):
        ball.dx *= -1.1  # Speed up slightly on hit

    # Score reset
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.reset()
    
    # Assuming 'ball' is a Pygame Rect object and 'ball_speed_x'/'ball_speed_y' track its movement
    if ball.right >= WIDTH:
        score_a += 1
        # Reset ball position and reverse direction (implement a function for this)
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    if ball.left <= 0:
        score_b += 1
        # Reset ball position and reverse direction
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= -1

    # Draw
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100), 3) # Court
    pygame.draw.line(screen, WHITE, (WIDTH//2, 50), (WIDTH//2, HEIGHT-50), 2) # Net
    all_sprites.draw(screen)
    
    # Clear the screen first (e.g., fill with black)
    screen.fill(BLACK) 

    # Render score text
    text_a = font.render(str(score_a), True, WHITE)
    text_b = font.render(str(score_b), True, WHITE)

    # Position the text (adjust coordinates as needed for your screen size)
    # This places scores near the center top of the screen
    screen.blit(text_a, (WIDTH//4, 10))
    screen.blit(text_b, (WIDTH//4 * 3 - text_b.get_width(), 10))

    # Update the display
    pygame.display.flip() 

    clock.tick(60)

pygame.quit()
