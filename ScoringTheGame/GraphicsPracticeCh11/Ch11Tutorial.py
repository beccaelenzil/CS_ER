import pygame
pygame.init()

#set basic color variables
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)

backgroundImage = pygame.image.load("background.jpg")
playerImage = pygame.image.load("maggot.png")
playerImage.set_colorkey(BLACK)

# open 700x500 window
windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

# set window title
pygame.display.set_caption("Ezra's Practice Graphics")

# define game clock
clock = pygame.time.Clock()

# play background sounds
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load('maggotSounds.ogg')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()

# main loop runs until user clicks close button
done = False

while not done:

    for event in pygame.event.get():  # user did something

        if event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.play()

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
    screen.blit(backgroundImage, [0, 0])

    screen.blit(playerImage, [x, y])


    # clear screen before doing anything else

    pygame.display.flip()  # update screen with what we said to draw above

    clock.tick(60)  # limit to 60 fps

pygame.quit()  # close window when loop finishes
