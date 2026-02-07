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
pygame.display.set_caption("Table Tennis")
screen.fill((0,0,0))

opponentscore=0
playerscore=0
velocity = pygame.Vector2(0, 0)
acceleration = pygame.Vector2(0, 100)
velocity += acceleration
position=+velocity
#trying to make simple figures for our tennis court
#A blank canvas which I guess you need to make the imahge on
sprite_surface = pygame.surface((100,100), pygame.SRCALPHA)
#how you draw a rectangle
player_rect=pygame.draw.rect(sprite_surface, (50,0,0),(25),50)
opponent_rect=pygame.draw.rect(sprite_surface, (150,0,0),(25),50)
#how to draw a ball
ball_circle=pygame.draw.rect(sprite_surface, (50,0,0), (25), 25)
ball_circle.x=0
ball_circle.y=0
ball_circle.x+=velocity.x 
ball_circle.y+=velocity.y
#physics


position=+velocity



def point():
    if player_rect.colliderect(ball_rect):
        ball_circle.x-=velocity.x 
        ball_circle.y-=velocity.y

    if opponent_rect.colliderect(ball_rect):
        ball_circle.x-=velocity.x 
        ball_circle.y-=velocity.y
    if player.centerx<ball.centerx:
        global opponentscore, playerscore
        opponentscore=opponentscore+1
        print("the opponent has",opponentscore)
        print("you have", playerscore)
    elif opponent.centerx>ball.centerx:
        playerscore=playerscore+1
        print("the opponent has",opponentscore)
        print("you have", playerscore)
While True:
    point()
