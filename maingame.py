#Importing necessary libraries
import pygame
import time
import random
pygame.init()
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
pygame.font.init()
pygame.display.init()

#Setting up display
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Table Tennis")
screen.fill((0,0,0))

#trying to make simple figures for our tennis court
#A blank canvas which I guess you need to make the imahge on
#TestSurface = pygame.surface((100,100), pygame.SRCALPHA)
#how you draw a rectangle
#pygame.draw.rect(sprite_surface, (50,0,0),(0,0,25,25))
#how to draw a circle
#pygame.draw.circle(sprite_surface, (50,0,0), (25), 25)
