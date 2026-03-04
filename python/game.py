import pygame
import random
from pygame import mixer

global p1point, p2point
p1point=0
p2point=0
# Setup
pygame.init()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Constants
GREEN, WHITE, YELLOW = (34, 139, 34), (255, 255, 255), (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, up_key, down_key,right_key,left_key):
        super().__init__()
        self.image = pygame.Surface((15, 80))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, HEIGHT // 2))
        self.up_key, self.down_key,self.right_key,self.left_key = up_key, down_key, right_key, left_key

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]: self.rect.y -= 7
        if keys[self.down_key]: self.rect.y += 7
        if keys[self.right_key]: self.rect.x -= 7
        if keys[self.left_key]: self.rect.x += 7
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
p1 = Player(50, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
p2 = Player(WIDTH - 50, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
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
    if ball.rect.left <= 0:
        ball.reset()
        p1point=p1point+1
        print("player 1 has",p1point,"player 2 has",p2point)
    if ball.rect.right >= WIDTH:
        ball.reset()
        p2point=p2point+1
        print("player 1 has",p1point,"player 2 has",p2point)
    # Draw
    screen.fill(GREEN)
    pygame.draw.line(screen, (255,255,255), (500, 0) , (500, 800), 4)
    pygame.draw.line(screen, (255, 255, 255), (0, 50) , (1000, 50), 2)
    pygame.draw.line(screen, (255, 255, 255), (0, 750) , (1000, 750), 2)
    pygame.draw.line(screen, (255, 255, 255), (250, 50) , (250, 750), 2)
    pygame.draw.line(screen, (255, 255, 255), (750, 50) , (750, 750), 2)
    pygame.draw.line(screen, (255, 255, 255), (250, 400) , (750, 400), 2)
    # pygame.draw.rect(screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100), 3) # Court
    # pygame.draw.line(screen, WHITE, (WIDTH//2, 50), (WIDTH//2, HEIGHT-50), 2) # Net
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
