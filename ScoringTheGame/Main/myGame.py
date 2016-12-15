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
LBLUE   = ( 150, 160, 255)

# set font info
font = pygame.font.SysFont("Courier New", 12, bold=False, italic=False)
fontB = pygame.font.SysFont("Courier New", 12, bold=True, italic=False)

textHeight = 15  # pygame.font.Font.get_linesize()
textWidth = 7
textRows = 72  # int(math.ceil(1080/fontLineHeight))
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
pygame.display.set_caption("Decker Duels")

# define game clock
clock = pygame.time.Clock()

# main loop runs until user clicks close button
done = False

# set starting positions of stuff
platformA_startX = 10
platformA_startY = 30
platformA_end = 10
platformA_width = 60
platformA_height = 3
platformA_dir = 1

#reset positions of stuff
platformA_x = platformA_startX

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

    # draw background
    for i in range(0, textRows):
        currentLine = ""

        for j in range(0, textColumns):
            currentLine += str(random.randint(0,1))

        text = font.render(currentLine, True, LBLUE)
        screen.blit(text, [1, i*textHeight])

    #draw moving platform
    if platformA_x >=  textColumns-platformA_end-platformA_width:
        platformA_dir = -1
    elif platformA_x <= platformA_startX:
        platformA_dir = 1
    platformA_x += textWidth * platformA_dir

    pygame.draw.rect(screen, WHITE, [platformA_x*textWidth, platformA_startY*textHeight, platformA_width*textWidth, platformA_height*textHeight])

    for i in range(platformA_height):
        currentLine = ""

        for j in range(platformA_width):
            currentLine += str(random.randint(0,1))

        text = fontB.render(currentLine, True, BLUE)
        screen.blit(text, [1+platformA_x*textWidth, (i+platformA_startY)*textHeight])




    pygame.display.flip()  # update screen with what we said to draw above

    clock.tick(10)  # limit to 30 fps

pygame.quit()  # close window when loop finishes
