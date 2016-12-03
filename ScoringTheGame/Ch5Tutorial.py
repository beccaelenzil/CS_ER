import pygame
pygame.init()

import math

#set basic color variables
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)

PI = math.pi

#open 1920x1080 window
windowSize = (700, 500)
screen = pygame.display.set_mode(windowSize)

#set window title
pygame.display.set_caption("Ezra's First Graphics")

#define game clock
clock = pygame.time.Clock()

#main loop runs until user clicks close button
done = False

while not done:

    for event in pygame.event.get(): #user did something

        if event.type == pygame.QUIT:  #user hit close
            done = True
            print("User asked to quit.")
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")

    # ---- game logic goes here ----

    # ---- drawing code goes here ----

    screen.fill(WHITE) #clear screen before doing anything else

    pygame.display.flip() #update screen with what we said to draw above

    clock.tick(60) #limit to 60 fps

pygame.quit() #close window when loop finishes
