import pygame
pygame.init()

import math
import random

#set basic color variables
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)

# open 700x500 window
windowSize = (700, 500)
screen = pygame.display.set_mode(windowSize)

# define game clock
clock = pygame.time.Clock()

# main loop runs until user clicks close button
done = False

# define character drawing function
def draw_stick_figure(screen, x, y, COLOR):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1+x,y,10,10], 0)

    # Legs
    pygame.draw.line(screen, BLACK ,[5+x,17+y], [10+x,27+y], 2)
    pygame.draw.line(screen, BLACK, [5+x,17+y], [x,27+y], 2)

    # Body
    pygame.draw.line(screen, COLOR, [5+x,17+y], [5+x,7+y], 2)

    # Arms
    pygame.draw.line(screen, COLOR, [5+x,7+y], [9+x,17+y], 2)
    pygame.draw.line(screen, COLOR, [5+x,7+y], [1+x,17+y], 2)

# Speed in pixels per frame
x_speed = 0
y_speed = 0

# Current position
x_coord = 10
y_coord = 10

screen.fill(WHITE)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0

    # Move the object according to the speed vector.
    x_coord += x_speed
    y_coord += y_speed

    # Draw the stick figure
    draw_stick_figure(screen, x_coord, y_coord, [random.randint(0,225),random.randint(0,225),random.randint(0,225)])

    pygame.display.flip()  # update screen with what we said to draw above

    clock.tick(60)  # limit to 60 fps

pygame.quit()  # close window when loop finishes
