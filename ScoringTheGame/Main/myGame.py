import pygame
pygame.init()

import math
import random

#set basic color variables
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
LGREY   = ( 225, 225, 225)
DGREY   = (  60,  60,  60)
BLUE    = (   0,   0, 255)

# set font info
font = pygame.font.SysFont("Courier New", 12, bold=False, italic=False)

fontLineHeight = 15  #pygame.font.Font.get_linesize()
textRows = 72  #int(math.ceil(1080/fontLineHeight))
textColumns = 274
'''
# make background
for i in range(0, textRows):
    tooShort = True
    currentLine = ""

    while tooShort:
        currentLine += str(round(random.randint(0,1)))
        lineSize = pygame.font.Font.size(currentLine)
        tooShort = lineSize[0] >= 1920

    text = font.render(currentLine, True, BLACK)
'''
# open 1920x1080 window
windowSize = (1920, 1080)
screen = pygame.display.set_mode(windowSize)

# set window title
pygame.display.set_caption("Ezra's Decker Game")


# define game clock
clock = pygame.time.Clock()

# main loop runs until user clicks close button
done = False

while not done:

    for event in pygame.event.get():  # user did something

        if event.type == pygame.QUIT:  # user hit close
            done = True
            print("User asked to quit.")
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")

    # ---- game logic goes here ----
    playerPosition = pygame.mouse.get_pos()
    x = playerPosition[0]
    y = playerPosition[1]




    # ---- drawing code goes here ----

    screen.fill(WHITE)

    for i in range(0, textRows):
        tooShort = True
        currentLine = ""

        for j in range(0, textColumns):
            currentLine += str(random.randint(0,1))

        text = font.render(currentLine, True, BLACK)
        screen.blit(text, [1, i*fontLineHeight])



    pygame.display.flip()  # update screen with what we said to draw above

    clock.tick(60)  # limit to 60 fps

pygame.quit()  # close window when loop finishes
