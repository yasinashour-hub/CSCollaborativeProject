#Importing necessary libraries
import pygame
import time
import random
pygame.init()
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
pygame.font.init()
pygame.display.init()
#how to add music (this is a stretch goal but the code is rlly easy)
# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
# pygame.init()
# pygame.mixer.init(44100, -16, 2, 512)
# from pygame import mixer
#how to play file
# pygame.mixer.music.load(random.choice(mp3 file))
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(1.0)


#Setting up display
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Tennis Battle Royale")
screen.fill((0,255, 0))

# trying to make simple figures for our tennis court
# A blank canvas which I guess you need to make the imahge on
# TestSurface = pygame.surface((100,100), pygame.SRCALPHA)
#how to draw a rectangle
# pygame.draw.rect(screen, (0, 255, 0), [0, 0, 100, 400], 0)
pygame.draw.line(screen, (255,255,255), (500, 0) , (500, 800), 4)
pygame.draw.line(screen, (255, 255, 255), (0, 50) , (1000, 50), 2)
pygame.draw.line(screen, (255, 255, 255), (0, 750) , (1000, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (250, 50) , (250, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (750, 50) , (750, 750), 2)
pygame.draw.line(screen, (255, 255, 255), (250, 400) , (750, 400), 2)
pygame.display.update()
time.sleep(10)