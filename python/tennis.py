import pygame
import sys
import random
import time
import subprocess

"""
Note: This file's version name is tennis3com++

ToDo:
- Add "Next" Buttons to all screen and remove click for next screen
- Enhance button appearence
- Compact/Optimize/Tidy button class and all associated functions, variables, etc.
- Finish Shop/Integration
"""

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 500
COURT_COLOR = (50, 150, 50)
NET_COLOR = (255, 255, 255)
BALL_COLOR = (200, 255, 50)
PLAYER_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
FPS = 60

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Create display with defined dimentions and assign to variable
pygame.display.set_caption("PvP Tennis") # Set window caption
clock = pygame.time.Clock() # Program clock

title_font = pygame.font.SysFont("Arial", 60, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 24)
instruction_font = pygame.font.SysFont("Arial", 20)
font_bold = pygame.font.SysFont("Arial", 30, bold=True)
font = pygame.font.SysFont("Arial", 30) # Universal font

# Classes
class Player(pygame.sprite.Sprite): # Player Class
    def __init__(self, x, y, side): # Object initialization function taking in object, x+y, and side
        super().__init__() # Activate parent class's contents
        self.image = pygame.Surface((20, 80)) # Create player image
        self.image.fill(PLAYER_COLOR) # Add color to image
        self.rect = self.image.get_rect() # Record object's frame
        self.rect.center = (x, y) # Set object's rect's center to given coordinates
        self.side = side # 'left' or 'right'
        self.speed = 7 # Player speed

        self.vel_x = 0 # Track current frame movement
        self.vel_y = 0

    def update(self, keys): # Update function taking in object and keys
        old_x, old_y = self.rect.x, self.rect.y # Record start of frame's position
        
        if self.side == 'left': # If player is on the left,
            if keys[pygame.K_w] and self.rect.top > 0: self.rect.y -= self.speed
            # AND the key is 'w' and the player's top is not crossing the top edge, move the player up by the speed
            if keys[pygame.K_s] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
            # AND the key is 's' and the player's top is not crossing the bottom edge, move the player down by the speed
            if keys[pygame.K_d] and self.rect.right < WIDTH // 2 - 10: self.rect.x += self.speed
            # AND the key is 'd' and the player's top is not crossing the net (little left of half of width), move the player right by the speed
            if keys[pygame.K_a] and self.rect.left > 0: self.rect.x -= self.speed
            # AND the key is 'a' and the player's top is not crossing the left edge, move the player left by the speed
        
        else: # Otherwise, player is on right so do the same as left with horzonal concepts edited
            if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
            if keys[pygame.K_LEFT] and self.rect.left > WIDTH // 2 + 10: self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed
        
        # Calculate velocity for this frame
        # (Difference of start vs end position in one frame)
        self.vel_x = self.rect.x - old_x
        self.vel_y = self.rect.y - old_y

class Ball(pygame.sprite.Sprite): # Ball Class
    def __init__(self): # Object initialization (same reasoning as player)
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.reset_ball() # Call ball reset function

    def reset_ball(self): # Ball reset function
        self.rect.center = (WIDTH // 2, HEIGHT // 2) # Center object to middle of width & height
        self.speed_x = random.choice([-5, -5]) # Randomly move ball either to left or right with speed 7
        self.speed_y = random.choice([-3, 3]) # Randomly move ball either up or down with speed 4

    def update(self): # Update ball
        self.rect.x += self.speed_x # Move ball's X by said speed
        self.rect.y += self.speed_y # Move ball's Y by said speed

        # Bounce off top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT: # If ball has hit vertial limits,
            self.speed_y *= -1 # Invert ball movement/speed

    def hit(self, player): # Hit instructions
        # 1. Reverse horizontal direction
        self.speed_x *= -1
        
        # 2. Add player's X-momentum (Chill Physics)
        # Moving toward the ball speeds it up & moving away slows it down
        self.speed_x += player.vel_x * 0.6
        
        # 3. Add vertical "spin" based on player's Y-movement + hit position
        paddle_influence = (self.rect.centery - player.rect.centery) * 0.1
        self.speed_y = (player.vel_y * 0.4) + paddle_influence

        # 4. Speed Lower Limit: Ensure ball never stops or moves too slow to finish a point
        if abs(self.speed_x) < 5:
            self.speed_x = 5 if self.speed_x > 0 else -5

class Button:
    def __init__(self, x, y, width, height, text, default_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = default_color
        self.hover_color = hover_color
        self.color = default_color
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(text, True, (255, 255, 255)) # Black text
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        #Draws the button on the screen and updates its color based on mouse position.
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def check_hover(self, mouse_pos):
        #Changes button color on hover.
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = self.default_color

    def handle_event(self, event):
        # Handles mouse click events.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

# Screen Functions
def show_home_screen(): # Home screen function
    waiting = True # Waiting state
    while waiting: # While in ^
        screen.fill(COURT_COLOR) # Set background

        # Rendered text variables
        title = title_font.render("CHILL PHYSICS TENNIS", True, WHITE)
        start = font.render("Press any key to Play", True, WHITE)
        instruction1 = instruction_font.render(
            "This is a 2D, Top-View, PvP, Pong-Inspired Tennis Sim", True, WHITE)
        instruction2 = instruction_font.render(
            "It has built basic realistic tennis physics including dynamic speed, spin, etc.",
            True, WHITE)
        
        # Text display
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 1.6))
        screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 1.45))
        
        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            # If the event is any key or mouse press
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False # Exit this loop to start the game

def show_shop_screen(): # Home screen function
    shopping = True # Waiting state
    while shopping: # While in ^
        screen.fill(COURT_COLOR) # Set background
        
        # Rendered text variables
        title = title_font.render("TENNIS SHOP", True, WHITE)
        title_rect = title.get_rect()
        subtitle = subtitle_font.render("View/Toggle your earned upgrades here | Increase your wealth through in-game merit", True, WHITE)
        
        # Text display
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_rect.bottom + 30))
        
        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            # If the event is any key or mouse press
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                shopping = False # Exit this loop to start the game

def show_finish_screen(): # Home screen function
    finishing = True # Waiting state
    while finishing: # While in ^
        screen.fill(COURT_COLOR) # Set background
        
        # Rendered text variables
        title = title_font.render("FINISH SCREEN", True, WHITE)
        title_rect = title.get_rect()
        subtitle = subtitle_font.render("Play around with our minigames here", True, WHITE)
        
        # Text display
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_rect.bottom + 30))
        
        ttt_button.draw(screen)

        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            # Pass events to the button handler
            ttt_button.handle_event(event)

def ttt(): # Tic-Tac_toe minigame function
    subprocess.run([sys.executable, 'CSCollaborativeProject/python/mini_games/ttt.py'])

# Object Initialization
player1 = Player(100, HEIGHT // 2, 'left')
player2 = Player(WIDTH - 100, HEIGHT // 2, 'right')
ball = Ball()
all_sprites = pygame.sprite.Group(player1, player2, ball)

finish_button = Button(
    x=905,
    y=3,
    width=100,
    height=50,
    text="FINISH",
    default_color=COURT_COLOR,
    hover_color=WHITE,
    action=show_finish_screen
)

ttt_button = Button(
    x=150,
    y=125,
    width=200,
    height=100,
    text="Tic-Tac-Toe",
    default_color=COURT_COLOR,
    hover_color=WHITE,
    action=ttt
)

score1 = 0
score2 = 0

# Music Set Up
pygame.mixer.music.load("python/assets/strategy_twice.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1.0)

# Pre-Main Game Screens
show_home_screen() # Call wait screen function before main game untill quitted
show_shop_screen() # Call wait screen function before main game untill quitted

# Game Loop
running = True
first_run = True
while running:
    if first_run:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the button handler
            finish_button.handle_event(event)

        # 1.1 Hover Effect Check
        mouse_pos = pygame.mouse.get_pos()
        finish_button.check_hover(mouse_pos)

        # 2. Contant Updates
        keys = pygame.key.get_pressed() # Get any key presses
        player1.update(keys) # Update players based on key press
        player2.update(keys)
        ball.update() # Update ball

        # 3. Collision Detection
        if pygame.sprite.collide_rect(ball, player1) and ball.speed_x < 0: # If collision with left player and ball is going left
            ball.hit(player1) # Apply realistic hit protocols based to hitter (not thier rect)
        if pygame.sprite.collide_rect(ball, player2) and ball.speed_x > 0: # If collision with right player and ball is going right
            ball.hit(player2) # Apply realistic hit protocols based to hitter (not thier rect)

        # 4. Scoring
        if ball.rect.left <= 0: # If ball's left side is past left side of screen
            score2 += 1 # Add to player2's (right side player) score
            ball.reset_ball() # Reset ball because point is over
        elif ball.rect.right >= WIDTH:
            score1 += 1
            ball.reset_ball()

        # 5. Draw
        screen.fill(COURT_COLOR) # Color the screen to court color
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)
        pygame.draw.line(screen, NET_COLOR, (0, HEIGHT // 8), (WIDTH, HEIGHT // 8), 2) # Top Alley
        pygame.draw.line(screen, NET_COLOR, (0, HEIGHT*7 // 8), (WIDTH, HEIGHT*7 // 8), 2) # Bottom Alley
        pygame.draw.line(screen, NET_COLOR, ((WIDTH // 2)*7 // 13, 0), ((WIDTH // 2)*7 // 13, HEIGHT), 2) # Left Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH - (WIDTH // 2)*7 // 13, 0), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT), 2) # Right Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), ((WIDTH // 2)*7 // 13, HEIGHT // 2), 2) # Left Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT // 2), 2) # Right Service Line
        # Draw court lines on screen in white with accurately calculated proportions
        all_sprites.draw(screen) # Draw all sprites on screen
        finish_button.draw(screen)

        # UI
        wait_text = font_bold.render("Game Start In ~3 Seconds", True, WHITE) # Text for score 1
        s1_text = font.render(str(score1), True, WHITE) # Text for score 1
        s2_text = font.render(str(score2), True, WHITE) # Text for score 1
        screen.blit(s1_text, (WIDTH // 4, 20)) # Blit text1 on left
        screen.blit(s2_text, (3 * WIDTH // 4, 20)) # Blit text2 on right
        screen.blit(wait_text, (WIDTH // 2 - wait_text.get_width() // 2 - 10, HEIGHT // 2 - wait_text.get_height() // 2 - 50)) # Blit text2 on right

        pygame.display.flip() # Update pygame
        clock.tick(FPS) # Constrain game's frame rate to fixed value for consistancy

        time.sleep(3)
        first_run = False
    else:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the button handler
            finish_button.handle_event(event)

        # 2. Contant Updates
        keys = pygame.key.get_pressed() # Get any key presses
        player1.update(keys) # Update players based on key press
        player2.update(keys)
        ball.update() # Update ball

        # 3. Collision Detection
        if pygame.sprite.collide_rect(ball, player1) and ball.speed_x < 0: # If collision with left player and ball is going left
            ball.hit(player1) # Apply realistic hit protocols based to hitter (not thier rect)
        if pygame.sprite.collide_rect(ball, player2) and ball.speed_x > 0: # If collision with right player and ball is going right
            ball.hit(player2) # Apply realistic hit protocols based to hitter (not thier rect)

        # 4. Scoring
        if ball.rect.left <= 0: # If ball's left side is past left side of screen
            score2 += 1 # Add to player2's (right side player) score
            ball.reset_ball() # Reset ball because point is over
        elif ball.rect.right >= WIDTH:
            score1 += 1
            ball.reset_ball()

        # 5. Draw
        screen.fill(COURT_COLOR) # Color the screen to court color
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)
        pygame.draw.line(screen, NET_COLOR, (0, HEIGHT // 8), (WIDTH, HEIGHT // 8), 2) # Top Alley
        pygame.draw.line(screen, NET_COLOR, (0, HEIGHT*7 // 8), (WIDTH, HEIGHT*7 // 8), 2) # Bottom Alley
        pygame.draw.line(screen, NET_COLOR, ((WIDTH // 2)*7 // 13, 0), ((WIDTH // 2)*7 // 13, HEIGHT), 2) # Left Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH - (WIDTH // 2)*7 // 13, 0), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT), 2) # Right Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), ((WIDTH // 2)*7 // 13, HEIGHT // 2), 2) # Left Service Line
        pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT // 2), 2) # Right Service Line
        # Draw court lines on screen in white with accurately calculated proportions
        all_sprites.draw(screen) # Draw all sprites on screen
        finish_button.draw(screen)

        # UI
        s1_text = font.render(str(score1), True, WHITE) # Text for score 1
        s2_text = font.render(str(score2), True, WHITE) # Text for score 1
        screen.blit(s1_text, (WIDTH // 4, 20)) # Blit text1 on left
        screen.blit(s2_text, (3 * WIDTH // 4, 20)) # Blit text2 on right

        pygame.display.flip() # Update pygame
        clock.tick(FPS) # Constrain game's frame rate to fixed value for consistancy

pygame.quit()
# When game isn't running quit pygame and exit system
sys.exit()
