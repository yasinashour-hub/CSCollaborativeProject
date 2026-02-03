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
