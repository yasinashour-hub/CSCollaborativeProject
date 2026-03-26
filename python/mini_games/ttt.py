import pygame
import sys

# --- Configuration ---
SIZE = 300
LINE_WIDTH = 10
GRID_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Tic Tac Toe')

# --- Game State ---
board = [[None for _ in range(3)] for _ in range(3)]
player = 'X'
game_over = False

def draw_grid():
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        # Vertical lines
        pygame.draw.line(screen, GRID_COLOR, (i * SIZE // 3, 0), (i * SIZE // 3, SIZE), LINE_WIDTH)
        # Horizontal lines
        pygame.draw.line(screen, GRID_COLOR, (0, i * SIZE // 3), (SIZE, i * SIZE // 3), LINE_WIDTH)

def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                center_x = col * SIZE // 3 + SIZE // 6
                center_y = row * SIZE // 3 + SIZE // 6
                pygame.draw.line(screen, X_COLOR, (center_x - 30, center_y - 30), (center_x + 30, center_y + 30), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (center_x + 30, center_y - 30), (center_x - 30, center_y + 30), LINE_WIDTH)
            elif board[row][col] == 'O':
                center_x = col * SIZE // 3 + SIZE // 6
                center_y = row * SIZE // 3 + SIZE // 6
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 40, LINE_WIDTH)

def check_win():
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] is not None: return True
        if board[0][i] == board[1][i] == board[2][i] is not None: return True
    if board[0][0] == board[1][1] == board[2][2] is not None: return True
    if board[0][2] == board[1][1] == board[2][0] is not None: return True
    return False

def check_draw():
    for row in board:
        if None in row:
            return False
    return True

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row = y // (SIZE // 3)
            col = x // (SIZE // 3)
            if board[row][col] is None:
                board[row][col] = player
                if check_win():
                    game_over = True
                    print(f"Player {player} wins!")
                elif check_draw():
                    game_over = True
                    print("Game Draw!")
                else:
                    player = 'O' if player == 'X' else 'X'

    draw_grid()
    draw_marks()
    pygame.display.update()
