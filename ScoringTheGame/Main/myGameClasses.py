import pygame
import math
import random

pygame.init()

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LGREY = (225, 225, 225)
DGREY = (60, 60, 60)
LBLUE = (150, 160, 255)

# set font info
font = pygame.font.SysFont("Courier New", 10, bold=False, italic=False)
fontB = pygame.font.SysFont("Courier New", 10, bold=True, italic=False)

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

textHeight = 13
textWidth = 6
textRows = SCREEN_HEIGHT/textHeight  # 83
textColumns = SCREEN_WIDTH/textWidth  # 320


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self):

        # Call the parent's constructor
        super(self.__class__, self).__init__()

        self.color = (0, 0, 0)

        # enable dashing
        self.canDash = True

        self.upPressed = False
        self.leftPressed = False
        self.rightPressed = False
        self.downPressed = False

        # Create an image of the block, and fill it with a color.
        width = 4
        height = 6
        self.image = pygame.Surface([width*textWidth, height*textHeight])

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vectors of player
        self.change_x = 0
        self.change_y = 0

        self.move_x = 0
        self.move_y = 0
        self.dash_x = 0
        self.dash_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        self.image.fill(self.color)

        # Gravity
        self.calc_grav()

        # calculate total movement
        self.change_x = self.move_x + self.dash_x

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.canDash = True
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # add deceleration to horizontal dash
        if self.dash_x > 0:
            self.dash_x -= 2
        elif self.dash_x < 0:
            self.dash_x += 2

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1.4

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -24

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.move_x -= 10

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.move_x += 10

    """def stop(self):
        # Called when the user lets off the keyboard.
        self.move_x = 0
        self.canDash = True"""

    def dash(self):
        if self.canDash:
            if self.upPressed:
                self.change_y -= 20
            if self.downPressed:
                self.change_y += 20
            if self.leftPressed:
                self.dash_x -= 20
            if self.rightPressed:
                self.dash_x += 20

            self.canDash = False


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super(self.__class__, self).__init__()

        self.image = pygame.Surface([width*textWidth, height*textHeight])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level(object):

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(WHITE)

        '''for i in range(0, textRows):
            currentLine = ""

            for j in range(0, textColumns):
                currentLine += str(random.randint(0,1))

            text = font.render(currentLine, True, LBLUE)
            screen.blit(text, [0, i*textHeight])'''

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[60, 2, 130, 32],  # middle platform
                 [34, 2, 86, 44],  # left middle platform
                 [34, 2, 200, 44],  # left middle platform
                 [320, 5, 0, 78],  # floor
                 [30, 3, 0, 75],  # floor left podium
                 [30, 3, 290, 75],  # floor right podium
                 [6, 83, 0, 0],  # left wall
                 [6, 83, 314, 0],  # left wall
                 [100, 9, 110, 58],  # tunnel ceiling 3
                 [21, 6, 72, 64],  # tunnel ceiling 1
                 [17, 13, 93, 57],  # tunnel ceiling 2
                 [17, 13, 210, 57],  # tunnel ceiling 4
                 [21, 6, 227, 64],  # tunnel ceiling 5
                 [12, 42, 20, 16],  # left column
                 [12, 42, 288, 16]  # right column
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player = self.player
            self.platform_list.add(block)


def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Decker Duels")

    # Create the player
    playerA = Player()
    playerB = Player()

    #set player colors
    playerA.color = RED
    playerB.color = YELLOW

    # Create all the levels
    level_list = []
    level_list.append( Level_01(playerA) )

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    playerA.level = current_level
    playerB.level = current_level

    playerA.rect.x = 15*textWidth
    playerA.rect.y = 65*textHeight
    active_sprite_list.add(playerA)

    playerB.rect.x = 320*textWidth - 15*textWidth - playerB.rect.width
    playerB.rect.y = 65*textHeight
    active_sprite_list.add(playerB)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                # playerA Controls
                if event.key == pygame.K_a:
                    playerA.go_left()
                    playerA.leftPressed = True
                if event.key == pygame.K_d:
                    playerA.go_right()
                    playerA.rightPressed = True
                if event.key == pygame.K_w:
                    playerA.upPressed = True
                if event.key == pygame.K_s:
                    playerA.downPressed = True
                if event.key == pygame.K_g:
                    playerA.jump()
                if event.key == pygame.K_f:
                    playerA.dash()

                # playerB controls
                if event.key == pygame.K_h:
                    playerB.go_left()
                    playerB.leftPressed = True
                if event.key == pygame.K_k:
                    playerB.go_right()
                    playerB.rightPressed = True
                if event.key == pygame.K_u:
                    playerB.upPressed = True
                if event.key == pygame.K_j:
                    playerB.downPressed = True
                if event.key == pygame.K_SEMICOLON:
                    playerB.jump()
                if event.key == pygame.K_l:
                    playerB.dash()

            if event.type == pygame.KEYUP:
                '''
                if event.key == pygame.K_a and playerA.change_x < 0:
                    playerA.stop()
                if event.key == pygame.K_d and playerA.change_x > 0:
                    playerA.stop()

                if event.key == pygame.K_h and playerB.change_x < 0:
                    playerB.stop()
                if event.key == pygame.K_k and playerB.change_x > 0:
                    playerB.stop()'''

                # playerA Controls
                if event.key == pygame.K_a:
                    playerA.go_right()
                    playerA.leftPressed = False
                if event.key == pygame.K_d:
                    playerA.go_left()
                    playerA.rightPressed = False
                if event.key == pygame.K_w:
                    playerA.upPressed = False
                if event.key == pygame.K_s:
                    playerA.downPressed = False

                # playerB controls
                if event.key == pygame.K_h:
                    playerB.go_right()
                    playerB.leftPressed = False
                if event.key == pygame.K_k:
                    playerB.go_left()
                    playerB.rightPressed = False
                if event.key == pygame.K_u:
                    playerB.upPressed = False
                if event.key == pygame.K_j:
                    playerB.downPressed = False

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if playerA.rect.right > SCREEN_WIDTH:
            playerA.rect.right = SCREEN_WIDTH
        if playerB.rect.right > SCREEN_WIDTH:
            playerB.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if playerA.rect.left < 0:
            playerA.rect.left = 0
        if playerB.rect.left < 0:
            playerB.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        print playerA.canDash


        # Limit to 30 frames per second
        clock.tick(30)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
