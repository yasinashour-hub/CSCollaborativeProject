import pygame, sys

# Initialize and setup
pygame.init()
WIDTH, S_SIZE = 300, 100
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Simple Tic Tac Toe')
board = [[0]*3 for _ in range(3)]
player = "O"

# Colors and drawing helpers
COLOR_BG, COLOR_LINE, C_1, C_2 = (28, 170, 156), (23, 145, 135), (239, 231, 200), (66, 66, 66)
def draw_board():
    screen.fill(COLOR_BG)
    for i in range(1, 3):
        pygame.draw.line(screen, COLOR_LINE, (0, i*S_SIZE), (WIDTH, i*S_SIZE), 10)
        pygame.draw.line(screen, COLOR_LINE, (i*S_SIZE, 0), (i*S_SIZE, WIDTH), 10)
    for r in range(3):
        for c in range(3):
            if board[r][c] == "O": pygame.draw.circle(screen, C_1, (c*S_SIZE+50, r*S_SIZE+50), 30, 10)
            elif board[r][c] == "X":
                pygame.draw.line(screen, C_2, (c*S_SIZE+20, r*S_SIZE+80), (c*S_SIZE+80, r*S_SIZE+20), 10)
                pygame.draw.line(screen, C_2, (c*S_SIZE+20, r*S_SIZE+20), (c*S_SIZE+80, r*S_SIZE+80), 10)

# Main Loop
draw_board()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            r, c = event.pos[1]//S_SIZE, event.pos[0]//S_SIZE
            if board[r][c] == 0:
                board[r][c] = player
                player = "X" if player == "O" else "O"
                draw_board()
    pygame.display.update()
