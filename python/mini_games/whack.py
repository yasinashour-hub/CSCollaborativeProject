import pygame
import random

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Square properties
sq_size = 50
sq_color = (255, 0, 0)  # Red
sq_rect = pygame.Rect(300, 200, sq_size, sq_size)

# Game variables
score = 0
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 750)  # Move every 1000ms (1 second)

running = True
while running:
    # 2. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sq_rect.collidepoint(event.pos):
                score += 1
                # Move immediately when clicked
                sq_rect.x = random.randint(0, 600 - sq_size)
                sq_rect.y = random.randint(0, 400 - sq_size)
        
        # Move on timer tick
        if event.type == MOVE_EVENT:
            sq_rect.x = random.randint(0, 600 - sq_size)
            sq_rect.y = random.randint(0, 400 - sq_size)

    # 3. Drawing
    screen.fill((255, 255, 255))  # White background
    pygame.draw.rect(screen, sq_color, sq_rect)
    
    # Display score in window title
    pygame.display.set_caption(f"Whack-A-Square | Score: {score}")
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
