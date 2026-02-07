#Importing necessary libraries
import pygame
import time
import random

pygame.init()
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
pygame.font.init()
pygame.display.init()
velocity=0
#Setting up display
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Tennis Battle Royale")
screen.fill((0,255,0))
pygame.draw.line(screen, (255,255,255), (500, 0) , (500, 800), 4)
pygame.draw.line(screen, (255, 255, 255), (0, 50) , (1000, 50), 2)
pygame.draw.line(screen, (255, 255, 255), (0, 750) , (1000, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (250, 50) , (250, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (750, 50) , (750, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (250, 400) , (750, 400), 2)
pygame.display.update()
opponentscore=0
playerscore=0
velocity = pygame.Vector2(0, 0)
acceleration = pygame.Vector2(0, 100)
velocity += acceleration
position=+velocity
#trying to make simple figures for our tennis court
#how you draw a rectangle
player_rect=pygame.draw.rect(sprite_surface, (50,0,0),(25),50)
opponent_rect=pygame.draw.rect(sprite_surface, (150,0,0),(25),50)
#how to draw a ball
#see if this works:
ball_circle=pygame.draw.circle(screen, (0,0,0), [0,0], 25, 0)
position=+velocity
def point():
    global opponentscore, playerscore
    ball_circle.x += velocity.x
    ball_circle.y += velocity.y
    if player_rect.colliderect(ball_circle) or opponent_rect.colliderect(ball_circle):
        velocity.x *= -1
    if ball_circle.top <= 0 or ball_circle.bottom >= 800:
        velocity.y *= -1
    if ball_circle.left <= 0:
        opponentscore += 1
        print("the opponent has", opponentscore)
        print("you have", playerscore)
        return
    if ball_circle.right >= 1000:
        playerscore += 1
        print("the opponent has", opponentscore)
        print("you have", playerscore)
        return
    if playerscore >= opponentscore + 2 and playerscore >= 7:
        print("you win")
        return
    if opponentscore >= playerscore + 2 and opponentscore >= 7:
        print("you lose")
        return
While True:
    point()
