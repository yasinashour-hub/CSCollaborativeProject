import pygame
import sys
import random
import time
import subprocess

'''
TO DO:
- Integration
- Angular Hitting
- Doubles
- More Bots, Mini-Games, Etc.
'''

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 500
COURT_COLOR = (50, 150, 50)
NET_COLOR = (255, 255, 255)
BALL_COLOR = (200, 255, 50)
PLAYER_COLOR = (255, 255, 255)
BOT_COLOR = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
FPS = 60

# Game State
game_mode = "START PvP" # Will update to bot mode if that is selected

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
    def __init__(self, x, y, side, bot_difficulty): # Object initialization function taking in object, x+y, and side
        super().__init__() # Activate parent class's contents
        self.original_image = pygame.Surface((20, 80), pygame.SRCALPHA) # Create player image
        self.original_image.fill(PLAYER_COLOR) # Add color to image
        self.image = self.original_image
        self.rect = self.image.get_rect() # Record object's frame
        self.angle = 0
        self.rect.center = (x, y) # Set object's rect's center to given coordinates
        self.OGcenter = (x, y)
        self.side = side # 'left' or 'right'
        self.speed = 7 # Player speed
        self.is_bot = False # Determines if this paddle is Bot-controlled
        self.bot_difficulty = bot_difficulty

        self.vel_x = 0 # Track current frame movement
        self.vel_y = 0

    def update(self, keys, ball=None): # Update function taking in object, keys, and ball
        old_x, old_y = self.rect.x, self.rect.y # Record start of frame's position
        
        if self.is_bot and ball is not None:
            self.image.fill(BOT_COLOR)

            # BOT LOGIC (Tracking the ball's Y-coordinate)
            # The bot is slightly slower to make it beatable
            bot_speed = self.speed - self.bot_difficulty
            
            # Only track if the ball is moving towards the bot's side to look more realistic
            if ball.speed_x < 0:
                if self.rect.centery < ball.rect.centery and self.rect.bottom < HEIGHT:
                    self.rect.y += bot_speed
                elif self.rect.centery > ball.rect.centery and self.rect.top > 0:
                    self.rect.y -= bot_speed
            else:
                # Return slowly to center when ball is moving away
                if self.rect.centery < HEIGHT // 2 - 10:
                    self.rect.y += 2
                elif self.rect.centery > HEIGHT // 2 + 10:
                    self.rect.y -= 2

        elif self.side == 'left': # If player is on the left,
            if keys[pygame.K_w] and self.rect.top > 0: self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
            if keys[pygame.K_d] and self.rect.right < WIDTH // 2 - 10: self.rect.x += self.speed
            if keys[pygame.K_a] and self.rect.left > 0: self.rect.x -= self.speed

            if keys[pygame.K_q]: self.angle += 2
            if keys[pygame.K_e]: self.angle -= 2
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.new_rect = self.image.get_rect(center=old_center)
        
        else: # Otherwise, manual player is on right
            if keys[pygame.K_UP] and self.rect.top > 0: self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT: self.rect.y += self.speed
            if keys[pygame.K_LEFT] and self.rect.left > WIDTH // 2 + 10: self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed

            if keys[pygame.K_PERIOD]: self.angle += 2
            if keys[pygame.K_SLASH]: self.angle -= 2
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.new_rect = self.image.get_rect(center=old_center)
        
        # Calculate velocity for this frame
        # (Difference of start vs end position in one frame)
        self.vel_x = self.rect.x - old_x
        self.vel_y = self.rect.y - old_y
    
    def reset_position(self):
        self.rect.center = self.OGcenter

class Ball(pygame.sprite.Sprite): # Ball Class
    def __init__(self): # Object initialization (same reasoning as player)
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.reset_ball() # Call ball reset function

    def reset_ball(self): # Ball reset function
        self.rect.center = (WIDTH // 2, HEIGHT // 2) # Center object to middle of width & height
        self.speed_x = random.choice([-5, 5]) # Randomly move ball either to left or right
        self.speed_y = random.choice([-3, 3]) # Randomly move ball either up or down

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
        self.speed_x += player.vel_x * 0.6
        
        # 3. Add vertical "spin" based on player's Y-movement + hit position
        if player.side == 'left':
            angle_influence = player.angle * -0.2
        else:
            angle_influence = player.angle * 0.2
        paddle_influence = ((self.rect.centery - player.rect.centery) * 0.1) + (angle_influence)
        self.speed_y = (player.vel_y * 0.4) + paddle_influence

        # 4. Speed Lower Limit: Ensure ball never stops or moves too slow
        if abs(self.speed_x) < 5:
            self.speed_x = 5 if self.speed_x > 0 else -5

class Button:
    def __init__(self, x, y, width, height, text, default_color, hover_color, big=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = default_color
        self.hover_color = hover_color
        self.color = default_color

        if big == True:
            self.font = pygame.font.Font(None, 40)
        else:
            self.font = pygame.font.Font(None, 30)

        self.text_surface = self.font.render(text, True, (255, 255, 255)) # White text
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        #Draws the button on the screen and updates its color
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
        if shop_button.rect.collidepoint(mouse_position):
            shop_button.color = shop_button.hover_color
        else:
            shop_button.color = shop_button.default_color


        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.rect.collidepoint(mouse_position):
                    waiting = False

def show_shop_screen(): # Shop screen function
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
        if start_button.rect.collidepoint(mouse_position):
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
                if start_button.rect.collidepoint(mouse_position):
                    shopping = False

def show_start_screen():
    global game_mode
    starting = True
    while starting:
        screen.fill(COURT_COLOR) # Set background
        
        # Rendered text variables
        title = title_font.render("GAME MODES", True, WHITE)
        title_rect = title.get_rect()
        subtitle = subtitle_font.render("Select which game mode you would like to play", True, WHITE)
        
        # Text display
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_rect.bottom + 30))
        
        pvp_button.draw(screen)
        for button in bot_buttons:
            button.draw(screen)

        mouse_position = pygame.mouse.get_pos()
        if pvp_button.rect.collidepoint(mouse_position):
            pvp_button.color = pvp_button.hover_color
        else:
            pvp_button.color = pvp_button.default_color
        
        for button in bot_buttons:
            if button.rect.collidepoint(mouse_position):
                button.color = button.hover_color
            else:
                button.color = button.default_color

        pygame.display.flip() # Update pygame
            
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            # If the event is any key or mouse press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.rect.collidepoint(mouse_position):
                    game_mode = "START PvP"
                    starting = False
                for button in bot_buttons:
                    if button.rect.collidepoint(mouse_position):
                        game_mode = button.text
                        starting = False

def show_finish_screen(): # Finish screen function
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
        whack_button.draw(screen)

        mouse_position = pygame.mouse.get_pos()
        if ttt_button.rect.collidepoint(mouse_position):
            ttt_button.color = ttt_button.hover_color
        elif whack_button.rect.collidepoint(mouse_position):
            whack_button.color = whack_button.hover_color
        else:
            ttt_button.color = ttt_button.default_color
            whack_button.color = whack_button.default_color

        pygame.display.flip() # Update pygame
        
        for event in pygame.event.get(): # For any event that pygame picks up
            if event.type == pygame.QUIT: # If the event is to quit the program, quit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ttt_button.rect.collidepoint(mouse_position):
                    subprocess.run([sys.executable, 'OLDSAFETY_CSCollaborativeProject/python/mini_games/ttt.py'])
                elif whack_button.rect.collidepoint(mouse_position):
                    subprocess.run([sys.executable, 'OLDSAFETY_CSCollaborativeProject/python/mini_games/whack.py'])

# Object Initialization
player1 = Player(100, HEIGHT // 2, 'left', 0)
player2 = Player(WIDTH - 100, HEIGHT // 2, 'right', 0)
ball = Ball()
all_sprites = pygame.sprite.Group(player1, player2, ball)

# Button Initialization
shop_button = Button(
    x=857, y=3, width=140, height=40,
    text="ENTER SHOP", default_color=(80, 180, 80), hover_color=(100, 200, 100))

start_button = Button(
    x=912, y=3, width=85, height=40,
    text="START", default_color=(80, 180, 80), hover_color=(100, 200, 100))

pvp_button = Button(
    x=225, y=215, width=250, height=168,
    text="START PvP", default_color=(80, 180, 80), hover_color=(100, 200, 100), big=True)

easy_bot_button = Button(
    x=500, y=215, width=300, height=35,
    text="START EASY BOT", default_color=(80, 180, 80), hover_color=(100, 200, 100), big=True)

mid_bot_button = Button(
    x=500, y=257, width=300, height=35,
    text="START MID BOT", default_color=(80, 180, 80), hover_color=(100, 200, 100), big=True)

hard_bot_button = Button(
    x=500, y=299, width=300, height=35,
    text="START HARD BOT", default_color=(80, 180, 80), hover_color=(100, 200, 100), big=True)

boss_bot_button = Button(
    x=500, y=341, width=300, height=35,
    text="START BOSS BOT", default_color=(80, 180, 80), hover_color=(100, 200, 100), big=True)

new_button = Button(
    x=3, y=457, width=140, height=40,
    text="NEW GAME", default_color=(80, 180, 80), hover_color=(100, 200, 100))

finish_button = Button(
    x=912, y=457, width=85, height=40,
    text="FINISH", default_color=(80, 180, 80), hover_color=(100, 200, 100))

ttt_button = Button(
    x=310, y=175, width=140, height=40,
    text="Tic-Tac-Toe", default_color=(80, 180, 80), hover_color=(100, 200, 100))

whack_button = Button(
    x=510, y=175, width=180, height=40,
    text="Whack-A-Sqaure", default_color=(80, 180, 80), hover_color=(100, 200, 100))

bot_buttons = [easy_bot_button, mid_bot_button, hard_bot_button, boss_bot_button]

# Scoring
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
            return "Ad Player 1", "Deuce"
        else:
            return "Deuce", "Ad Player 2"
            
    # Standard score reporting
    return f"{labels[score1]}", f"{labels[score2]}"

score1 = 0
score2 = 0

# Music Set Up (Wrapped in a try block in case the audio file path is missing on a local machine)
try:
    songs = ["OLDSAFETY_CSCollaborativeProject/python/assets/the_girls.mp3", "OLDSAFETY_CSCollaborativeProject/python/assets/strategy_twice.mp3"]
    pygame.mixer.music.load(random.choice(songs))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1.0)
except FileNotFoundError:
    pass

# Pre-Main Game Screens
show_home_screen() # Call wait screen function before main game untill quitted
show_shop_screen() # Call wait screen function before main game untill quitted
show_start_screen() # Call wait screen function before main game untill quitted

if game_mode == "START EASY BOT":
    player1.is_bot = True
    player1.bot_difficulty = 2
elif game_mode == "START MID BOT":
    player1.is_bot = True
    player1.bot_difficulty = 1
elif game_mode == "START HARD BOT":
    player1.is_bot = True
    player1.bot_difficulty = 0
elif game_mode == "START BOSS BOT":
    player1.is_bot = True
    player1.bot_difficulty = -93
else:
    player1.is_bot = False

# Game Loop
playing = True
while playing:
    running = True
    first_run = True
    while running:
        if first_run:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False

            # 2. Constant Updates (Pass ball into updates for bot tracking)
            keys = pygame.key.get_pressed() # Get any key presses
            player1.update(keys, ball) # Update players based on key press
            player2.update(keys, ball)
            ball.update() # Update ball

            # 3. Collision Detection
            if pygame.sprite.collide_rect(ball, player1) and ball.speed_x < 0:
                ball.hit(player1)
            if pygame.sprite.collide_rect(ball, player2) and ball.speed_x > 0: 
                ball.hit(player2)

            # 4. Scoring
            if ball.rect.left <= 0: 
                score2 += 1 
                ball.reset_ball() 
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
            all_sprites.draw(screen) # Draw all sprites on screen

            # UI
            wait_text = font_bold.render("Game Start In ~3 Seconds", True, WHITE)
            angle_instructions = instruction_font.render("Paddle Angle: For WASD use q & e | For Arrow use . & /", True, WHITE)
            screen.blit(wait_text, (WIDTH // 2 - wait_text.get_width() // 2 - 10, HEIGHT // 2 - wait_text.get_height() // 2 - 50)) 
            if game_mode == "START PvP":
                screen.blit(angle_instructions, (WIDTH // 2 - angle_instructions.get_width() // 2, HEIGHT // 2 - 60)) 
            
            s1_string, s2_string = get_current_score(score1, score2)
            s1_text = font.render(str(s1_string), True, WHITE) # Text for score 1
            s2_text = font.render(str(s2_string), True, WHITE) # Text for score 1
            screen.blit(s1_text, (s1_text.get_rect(midright=((WIDTH // 2)*7 // 13 - 10, 30)))) 
            screen.blit(s2_text, (s2_text.get_rect(midleft=(WIDTH - (WIDTH // 2)*7 // 13 + 10, 30)))) 

            pygame.display.flip() # Update pygame
            clock.tick(FPS) 

            time.sleep(3)
            first_run = False
        else:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if finish_button.rect.collidepoint(mouse_position):
                        show_finish_screen()
                    elif new_button.rect.collidepoint(mouse_position):
                        ball.reset_ball()
                        player1.reset_position()
                        player2.reset_position()
                        running = False
                        show_start_screen()

            # 1.1 Hover Effect Check
            mouse_position = pygame.mouse.get_pos()
            if finish_button.rect.collidepoint(mouse_position):
                finish_button.color = finish_button.hover_color
            elif new_button.rect.collidepoint(mouse_position):
                new_button.color = new_button.hover_color
            else:
                finish_button.color = finish_button.default_color
                new_button.color = new_button.default_color

            # 2. Constant Updates (Pass ball into updates for bot tracking)
            keys = pygame.key.get_pressed() 
            player1.update(keys, ball) 
            player2.update(keys, ball)
            ball.update() 

            # 3. Collision Detection
            if pygame.sprite.collide_rect(ball, player1) and ball.speed_x < 0: 
                ball.hit(player1) 
            if pygame.sprite.collide_rect(ball, player2) and ball.speed_x > 0: 
                ball.hit(player2) 

            # 4. Scoring
            if ball.rect.left <= 0: 
                score2 += 1 
                ball.reset_ball() 
            elif ball.rect.right >= WIDTH:
                score1 += 1
                ball.reset_ball()

            # 5. Draw
            screen.fill(COURT_COLOR) 
            pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 4)
            pygame.draw.line(screen, NET_COLOR, (0, HEIGHT // 8), (WIDTH, HEIGHT // 8), 2) 
            pygame.draw.line(screen, NET_COLOR, (0, HEIGHT*7 // 8), (WIDTH, HEIGHT*7 // 8), 2) 
            pygame.draw.line(screen, NET_COLOR, ((WIDTH // 2)*7 // 13, 0), ((WIDTH // 2)*7 // 13, HEIGHT), 2) 
            pygame.draw.line(screen, NET_COLOR, (WIDTH - (WIDTH // 2)*7 // 13, 0), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT), 2)
            pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), ((WIDTH // 2)*7 // 13, HEIGHT // 2), 2) 
            pygame.draw.line(screen, NET_COLOR, (WIDTH // 2, HEIGHT // 2), (WIDTH - (WIDTH // 2)*7 // 13, HEIGHT // 2), 2) 
            
            all_sprites.draw(screen) 
            finish_button.draw(screen)
            new_button.draw(screen)

            # UI
            s1_string, s2_string = get_current_score(score1, score2)
            s1_text = font.render(str(s1_string), True, WHITE) 
            s2_text = font.render(str(s2_string), True, WHITE) 
            screen.blit(s1_text, (s1_text.get_rect(midright=((WIDTH // 2)*7 // 13 - 10, 30)))) 
            screen.blit(s2_text, (s2_text.get_rect(midleft=(WIDTH - (WIDTH // 2)*7 // 13 + 10, 30)))) 

            pygame.display.flip() 
            clock.tick(FPS) 

pygame.quit()
sys.exit()
