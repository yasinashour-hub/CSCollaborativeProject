import pygame
import sys
import random
import time
import subprocess

# FOR USERS: Make sure reop name is "CSCollaborativeProject" EXACTLY

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
pygame.display.set_caption("Tennis Battle Royale") # Set window caption
clock = pygame.time.Clock() # Program clock

title_font = pygame.font.SysFont("Arial", 60, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 24)
instruction_font = pygame.font.SysFont("Arial", 20)
font_bold = pygame.font.SysFont("Arial", 30, bold=True)
font = pygame.font.SysFont("Arial", 26, bold=True) # Universal font

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
    def __init__(self, x, y, width, height, text, default_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = default_color
        self.hover_color = hover_color
        self.color = default_color
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(text, True, (255, 255, 255)) # Black text
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        #Draws the button on the screen and updates its color based on mouse position.
        pygame.draw.rect(screen, self.color, self.rect, 0, 10)
        screen.blit(self.text_surface, self.text_rect)

# Screen Functions
def show_home_screen(): # Home screen function
    waiting = True # Waiting state
    while waiting: # While in ^
        screen.fill(COURT_COLOR) # Set background

        # Rendered text variables
        title = title_font.render("TENNIS BATTLE ROYALE", True, WHITE)
        start = font.render("Click The Buttons To Play", True, WHITE)
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
        
        shop_button.draw(screen)

        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] in range(shop_button.rect.left, shop_button.rect.right) and mouse_position[1] in range(shop_button.rect.top, shop_button.rect.bottom):
            shop_button.color = shop_button.hover_color
        else:
            shop_button.color = shop_button.default_color


        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] in range(shop_button.rect.left, shop_button.rect.right) and mouse_position[1] in range(shop_button.rect.top, shop_button.rect.bottom):
                    waiting = False

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
        
        start_button.draw(screen)

        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] in range(start_button.rect.left, start_button.rect.right) and mouse_position[1] in range(start_button.rect.top, start_button.rect.bottom):
            start_button.color = start_button.hover_color
        else:
            start_button.color = start_button.default_color

        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            # If the event is any key or mouse press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] in range(start_button.rect.left, start_button.rect.right) and mouse_position[1] in range(start_button.rect.top, start_button.rect.bottom):
                    shopping = False

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

        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] in range(ttt_button.rect.left, ttt_button.rect.right) and mouse_position[1] in range(ttt_button.rect.top, ttt_button.rect.bottom):
            ttt_button.color = ttt_button.hover_color
        else:
            ttt_button.color = ttt_button.default_color

        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] in range(ttt_button.rect.left, ttt_button.rect.right) and mouse_position[1] in range(ttt_button.rect.top, ttt_button.rect.bottom):
                    subprocess.run([sys.executable, 'CSCollaborativeProject/python/mini_games/ttt.py'])

# Object Initialization
player1 = Player(100, HEIGHT // 2, 'left')
player2 = Player(WIDTH - 100, HEIGHT // 2, 'right')
ball = Ball()
all_sprites = pygame.sprite.Group(player1, player2, ball)

# Button Initialization
shop_button = Button(
    x=857,
    y=3,
    width=140,
    height=40,
    text="ENTER SHOP",
    default_color=(80, 180, 80),
    hover_color=(100, 200, 100)
)

start_button = Button(
    x=912,
    y=3,
    width=85,
    height=40,
    text="START",
    default_color=(80, 180, 80),
    hover_color=(100, 200, 100)
)

finish_button = Button(
    x=912,
    y=457,
    width=85,
    height=40,
    text="FINISH",
    default_color=(80, 180, 80),
    hover_color=(100, 200, 100)
)

ttt_button = Button(
    x=150,
    y=150,
    width=140,
    height=40,
    text="Tic-Tac-Toe",
    default_color=(80, 180, 80),
    hover_color=(100, 200, 100)
)

def get_current_score(score1, score2):
    # Standard labels
    labels = ["Love", "15", "30", "40"]
    
    # Check for winner
    if score1 >= 4 and score1 - score2 >= 2:
        return "Player 1 Wins", "Player 2 Loses"
    if score2 >= 4 and score2 - score1 >= 2:
        return "Player 1 Loses", "Player 2 Wins"
    
    # Handle Deuce and Advantage
    if score1 >= 3 and score2 >= 3:
        if score1 == score2:
            return "Deuce", "Deuce"
        elif score1 > score2:
            return "Advantage Player 1", "Deuce"
        else:
            return "Deuce", "Advantage Player 2"
            
    # Standard score reporting
    return f"{labels[score1]}", f"{labels[score2]}"

score1 = 0
score2 = 0


# Music Set Up
pygame.mixer.music.load("CSCollaborativeProject/python/assets/strategy_twice.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] in range(finish_button.rect.left, finish_button.rect.right) and mouse_position[1] in range(finish_button.rect.top, finish_button.rect.bottom):
                    shopping = False

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
        
        s1_string, s2_string = get_current_score(score1, score2)
        s1_text = font.render(str(s1_string), True, WHITE) # Text for score 1
        s2_text = font.render(str(s2_string), True, WHITE) # Text for score 1
        screen.blit(s1_text, (s1_text.get_rect(midright=((WIDTH // 2)*7 // 13 - 10, 30)))) # Blit text1 on left
        screen.blit(s2_text, (s2_text.get_rect(midleft=(WIDTH - (WIDTH // 2)*7 // 13 + 10, 30)))) # Blit text2 on right
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] in range(finish_button.rect.left, finish_button.rect.right) and mouse_position[1] in range(finish_button.rect.top, finish_button.rect.bottom):
                    shopping = False

        # 1.1 Hover Effect Check
        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] in range(finish_button.rect.left, finish_button.rect.right) and mouse_position[1] in range(finish_button.rect.top, finish_button.rect.bottom):
            finish_button.color = finish_button.hover_color
        else:
            finish_button.color = finish_button.default_color

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
        
        if score1 >= 11 or score2 >= 11:
            show_finish_screen()

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
        s1_string, s2_string = get_current_score(score1, score2)
        s1_text = font.render(str(s1_string), True, WHITE) # Text for score 1
        s2_text = font.render(str(s2_string), True, WHITE) # Text for score 1
        screen.blit(s1_text, (s1_text.get_rect(midright=((WIDTH // 2)*7 // 13 - 10, 30)))) # Blit text1 on left
        screen.blit(s2_text, (s2_text.get_rect(midleft=(WIDTH - (WIDTH // 2)*7 // 13 + 10, 30)))) # Blit text2 on right

        pygame.display.flip() # Update pygame
        clock.tick(FPS) # Constrain game's frame rate to fixed value for consistancy

pygame.quit()
# When game isn't running quit pygame and exit system
sys.exit()
