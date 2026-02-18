
#Importing necessary libraries
import pygame
import time
import random
import sys
pygame.init()
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP
pygame.font.init()
pygame.display.init()
velocity=0
#Setting up display
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Tennis Battle Royale")
screen.fill((0,255,0))
def court():
        pygame.draw.line(screen, (255,255,255), (500, 0) , (500, 800), 4)
        pygame.draw.line(screen, (255, 255, 255), (0, 50) , (1000, 50), 2)
        pygame.draw.line(screen, (255, 255, 255), (0, 750) , (1000, 750), 2)
        pygame.draw.line(screen, (255, 255, 255), (250, 50) , (250, 750), 2)
        pygame.draw.line(screen, (255, 255, 255), (750, 50) , (750, 750), 2)
        pygame.draw.line(screen, (255, 255, 255), (250, 400) , (750, 400), 2)
        pygame.display.update()
def minigame():
    choice1 = input("You notice someone with a troubled expression on their face. Do you want to help? Y/N")
    if choice1.lower() == "y":
           print("\nYou walk up to the person, who seems relieved that someone came to their aid.'What seems to be the matter?' you ask.")
           print("\nI need help with my math homework,' he replies. 'My name is Timmy, and I'm usually my parent's pride and joy, but today I'm hiding out at the tennis court until I finish all my homework.")
           print("\nOkay, I have one question left: Solve ln(e^6/e^-2).")
           homework = None
           while homework != 8:  
                  homework = int(input("Solve the expression."))
                  if homework != 8:
                        print("Try again, for Timmy's future depends on it.")
                  else:
                        print("You are correct! Timmy rejoices and immediately writes down the answer. 'Thank you,' he exclaims.'Here, take this reward. My parents will be so proud, and I will get to keep my #1 spot in SALSA High School.'")
                        coins = coins + 15
                        break
    elif choice1.lower() == "n":
        print("\nYou decide not to help, and leave them to their business.")
    else:
           print("\nYou feel conflicted, but ultimately decide not to help.")     

def music():
        pygame.mixer.music.load("cramusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        #i think there's another line to add to make the music play but im not sure what it is
opponentscore=0
playerscore=0
velocity = pygame.Vector2(0, 0)
acceleration = pygame.Vector2(0, 100)
velocity += acceleration
position=+velocity
clock=pygame.time.Clock()
fps_limit = 60
#trying to make simple figures for our tennis court
#how you draw a rectangle
player_rect=pygame.draw.rect(screen, (100,200,200), pygame.Rect(100, 100, 130, 130)) 
opponent_rect=pygame.draw.rect(screen, (0,0,0), pygame.Rect(30, 30, 60, 60)) 
#how to drawa ball
#see if this works:
ball_circle=pygame.draw.circle(screen, (0,0,0), [500,10], 25, 0)
position=+velocity
court()
# music()
def up():
        player_rect.y += 10
        return
def down():
        player_rect.y -= 10
        return
def left():
        player_rect.x -= 10
        return
def right():
        player_rect.x += 10
        return
def movement():
        if pygame.event == K_UP:
                up()
                pygame.display.update()
                return
        if pygame.event == KEYDOWN:
                down()
                pygame.display.update()
                return
        if pygame.event == K_LEFT:
                left()
                pygame.display.update()
                return
        if pygame.event == K_RIGHT:
                right()
                pygame.display.update()
                return

def point():
    global velocity
    global player_rect, opponent_rect
    global opponentscore, playerscore, ball_circle
    velocity = pygame.Vector2(0, 0)
    acceleration = pygame.Vector2(0, 100)
    velocity += acceleration
    position = +velocity
    clock = pygame.time.Clock()
    fps_limit = 60
    # trying to make simple figures for our tennis court
    # how you draw a rectangle

   # ball_circle += velocity.x
    #ball_circle += velocity.y
        

    movement()
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
while True:
         for event in pygame.event.get():
                              
                point()
                pygame.display.update()
