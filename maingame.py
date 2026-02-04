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
acceleration=100
velocity+=acceleration
opponentscore=0
playerscore=0
velocity+=acceleration
position=+velocity
#trying to make simple figures for our tennis court
#A blank canvas which I guess you need to make the imahge on
sprite_surface = pygame.surface((100,100), pygame.SRCALPHA)
#how you draw a rectangle
player=pygame.draw.circle(sprite_surface, (50,0,0),(25),50)
opponent=pygame.draw.circle(sprite_surface, (-50,0,0),(25),50)
#how to draw a circle
circle=pygame.draw.circle(sprite_surface, (50,0,0), (25), 25)
circle.x=0
circle.y=0
circle.x+=velocity.x 
circle.y+=velocity.y
#physics
acceleration=100

position=+velocity

if player.position==circle.position:
    velocity.x=-velocity.x
    velocity.y=-velocity.y
circle.x+=velocity.x
circle.y+=velocity.y
if opponent.position==circle.position:
    velocity.x=-velocity.x
    velocity.y=-velocity.y
circle.x+=velocity.x
circle.y+=velocity.y
def point():
    if player.position<circle.position:
        opponentscore=opponentscore+1
        print("the opponent have",opponentscore)
        print("you have", playerscore)
    elif opponent.position>circle.position:
        playerscore=playerscore+1
        print("the opponent have",opponentscore)
        print("you have", playerscore)