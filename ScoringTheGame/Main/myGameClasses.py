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
GOLD = (255, 165, 0)
VIOLET = (148, 0, 211)
MAGENTA = (255, 0, 255)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)
LGREY = (225, 225, 225)
DGREY = (60, 60, 60)
LBLUE = (150, 160, 255)

# set font info
font = pygame.font.SysFont("Courier New", 10, bold=False, italic=False)
fontB = pygame.font.SysFont("Courier New", 10, bold=True, italic=False)
titleFont = pygame.font.SysFont("Courier New", 50, bold=True, italic=False)
scoreFont = pygame.font.SysFont("Courier New", 30, bold=True, italic=False)

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640

textRows = 80
textColumns = 320
textHeight = SCREEN_HEIGHT / textRows
textWidth = SCREEN_WIDTH / textColumns

current_level_no = 0
numLevels = 1

#import sounds
jump_sound = pygame.mixer.Sound("SoundEffects/jump.ogg")
attack_sound = pygame.mixer.Sound("SoundEffects/attack.ogg")
death_sound = pygame.mixer.Sound("SoundEffects/death.ogg")


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self):

        # Call the parent's constructor
        super(self.__class__, self).__init__()

        self.color = (0, 0, 0)
        self.dashColor = (0, 0, 0)

        # create score counter
        self.score = 0

        # enable dashing
        self.canDash = True
        self.attacking = 0

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

        # moving platform conditions
        self.platformBoost_x = 0
        self.onMovingPlatform = False

        # List of sprites we can bump against
        self.level = None

    def update(self):
        self.image.fill(self.color)

        # Gravity
        self.calc_grav()

        # calculate total movement
        self.change_x = self.move_x + self.dash_x + self.platformBoost_x

        self.platformBoost_x = 0

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
                if isinstance(block, MovingPlatform):
                    self.platformBoost_x = block.change_x
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

        # count down attack active
        if self.attacking > 0:
            self.attacking -= 1
            self.image.fill(self.dashColor)

    def calc_grav(self):
        """ Calculate effect of gravity. """
        self.change_y += 0.15 * textHeight

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT:
            self.rect.y = -self.rect.height

    def jump(self):

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -2.1 * textHeight
            jump_sound.play()

    # Player-controlled movement:
    def go_left(self):
        self.move_x -= 2 * textWidth

    def go_right(self):
        self.move_x += 2 * textWidth

    """def stop(self):
        # Called when the user lets off the keyboard.
        self.move_x = 0
        self.canDash = True"""

    def dash_success(self):
        self.canDash = False
        self.attacking = 10
        attack_sound.play()

    def dash(self):
        if self.canDash:
            if self.upPressed:
                self.change_y = -2.4 * textHeight
                self.dash_success()
            if self.downPressed:
                self.change_y = 2.4 * textHeight
                self.dash_success()
            if self.leftPressed:
                self.dash_x -= 5 * textWidth
                self.dash_success()
            if self.rightPressed:
                self.dash_x += 5 * textWidth
                self.dash_success()


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height):

        # super(self.__class__, self).__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width*textWidth, height*textHeight])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):

    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player_a = None
    player_b = None

    level = None

    def __init__(self, width, height):
        # super(self.__class__, self).__init__(width, height)
        Platform.__init__(self, width, height)

    def update(self):

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit playerA
        hit = pygame.sprite.collide_rect(self, self.player_a)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player_a.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player_a.rect.left = self.rect.right

        # See if we hit playerB
        hit = pygame.sprite.collide_rect(self, self.player_b)
        if hit:

            if self.change_x < 0:
                self.player_b.rect.right = self.rect.left
            else:
                self.player_b.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we playerA
        hit = pygame.sprite.collide_rect(self, self.player_a)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player_a.rect.bottom = self.rect.top
            else:
                self.player_a.rect.top = self.rect.bottom

        # Check and see if we playerB
        hit = pygame.sprite.collide_rect(self, self.player_b)
        if hit:

            if self.change_y < 0:
                self.player_b.rect.bottom = self.rect.top
            else:
                self.player_b.rect.top = self.rect.bottom

        # Check boundaries and reverse direction if necessary
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1


class Level(object):

    def __init__(self, player_a, player_b):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.player_a = player_a
        self.player_b = player_b

        # player staring positions
        self.a_start_x = 0
        self.a_start_y = 0
        self.b_start_x = 0
        self.b_start_y = 0

        # Background image
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()

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


# Create platforms for  level 1
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player_a, player_b):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player_a, player_b)

        # Array with width, height, x, and y of platform
        level = [[60, 2, 130, 32],  # middle platform
                 [34, 2, 86, 44],  # left middle platform
                 [34, 2, 200, 44],  # left middle platform
                 [208, 10, 56, 76],  # floor
                 [30, 8, 0, 74],  # floor left podium
                 [30, 8, 290, 74],  # floor right podium
                 [6, 83, 0, 0],  # left wall
                 [6, 83, 314, 0],  # left wall
                 [21, 6, 72, 63],  # tunnel ceiling 1
                 [17, 13, 93, 56],  # tunnel ceiling 2
                 [100, 9, 110, 57],  # tunnel ceiling 3
                 [17, 13, 210, 56],  # tunnel ceiling 4
                 [21, 6, 227, 63],  # tunnel ceiling 5
                 [12, 42, 20, 16],  # left column
                 [12, 42, 288, 16]  # right column
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player_a = self.player_a
            block.player_b = self.player_b
            self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(48, 2)
        block.rect.x = 136*textWidth
        block.rect.y = 20*textHeight
        block.boundary_left = 42*textWidth
        block.boundary_right = 278*textWidth-48*textWidth
        block.change_x = textWidth
        block.player_a = self.player_a
        block.player_b = self.player_b
        block.level = self
        self.platform_list.add(block)

        self.a_start_x = 15*textWidth
        self.a_start_y = 65*textHeight
        self.b_start_x = 320*textWidth - 15*textWidth - player_b.rect.width
        self.b_start_y = 65*textHeight


def win_check(player_a, player_b, level_list, current_level, current_level_no, screen):
    if pygame.sprite.collide_rect(player_a, player_b):
        if player_a.attacking and player_b.attacking:
            print "Tie"
            pause(player_a, player_b, 5000, screen, 0)
            load_level(player_a, player_b, False, level_list, current_level, current_level_no)
            death_sound.play()

        elif player_a.attacking:
            print "A Wins"
            player_a.score += 1
            pause(player_a, player_b, 5000, screen, 1)
            load_level(player_a, player_b, True, level_list, current_level, current_level_no)
            death_sound.play()
        elif player_b.attacking:
            print "B Wins"
            player_b.score += 1
            pause(player_a, player_b, 5000, screen, 2)
            load_level(player_a, player_b, True, level_list, current_level, current_level_no)
            death_sound.play()
        else:
            print "Nobody attacking"


def pause(player_a, player_b, min_duration, screen, winner):

    player_a.move_x = 0
    player_a.move_y = 0
    player_a.dash_x = 0
    player_a.dash_y = 0
    player_a.change_x = 0
    player_a.change_y = 0
    player_b.move_x = 0
    player_b.move_y = 0
    player_b.dash_x = 0
    player_b.dash_y = 0
    player_b.change_x = 0
    player_b.change_y = 0

    player_a.upPressed = False
    player_a.leftPressed = False
    player_a.rightPressed = False
    player_a.downPressed = False
    player_b.upPressed = False
    player_b.leftPressed = False
    player_b.rightPressed = False
    player_b.downPressed = False

    # draw bars
    if player_a.rect.y <= player_b.rect.y:
        botRectTop = player_b.rect.y + 9 * textHeight
        topRectBot = player_a.rect.y - 3 * textHeight
    else:
        botRectTop = player_a.rect.y + 9 * textHeight
        topRectBot = player_b.rect.y - 3 * textHeight
    pygame.draw.rect(screen, BLACK, [0, 0, SCREEN_WIDTH, topRectBot])
    pygame.draw.rect(screen, BLACK, [0, botRectTop, SCREEN_WIDTH, SCREEN_HEIGHT - botRectTop])

    # draw text
    textY = 50

    if winner == 0:
        title = titleFont.render("Tie", True, WHITE)
        title_width, title_height = titleFont.size("Tie")
        screen.blit(title, [(SCREEN_WIDTH-title_width)/2, textY])
    elif winner == 1:
        title = titleFont.render("Player A Wins", True, WHITE)
        title_width, title_height = titleFont.size("Player A Wins")
        screen.blit(title, [(SCREEN_WIDTH-title_width)/2, textY])
    elif winner == 2:
        title = titleFont.render("Player B Wins", True, WHITE)
        title_width, title_height = titleFont.size("Player B Wins")
        screen.blit(title, [(SCREEN_WIDTH-title_width)/2, textY])

    text = scoreFont.render("Player A: " + str(player_a.score), True, WHITE)
    score_width, score_height = scoreFont.size("Player A: " + str(player_a.score))
    screen.blit(text, [(SCREEN_WIDTH-score_width)/2, textY + title_height + 10])

    pygame.display.update()

    pygame.time.delay(min_duration)

    a_key_is_down = True

    while a_key_is_down:
        pygame.time.delay(1000)
        a_key_is_down = False
        press = pygame.key.get_pressed()
        if pygame.key.get_focused():
            for i in range(0, len(press)):
                if press[i]:
                    a_key_is_down = True
                    print "a key is pressed: "
                    print i
        pygame.event.pump()

    pygame.event.clear()


def load_level(player_a, player_b, change_level, level_list, current_level, current_level_no):
    if change_level:
        current_level_no = random.randint(0, len(level_list) - 1)

    player_a.rect.x = current_level.a_start_x
    player_a.rect.y = current_level.a_start_y

    player_b.rect.x = current_level.b_start_x
    player_b.rect.y = current_level.b_start_y

    player_a.attacking = 0
    player_b.attacking = 0

    player_a.move_x = 0
    player_a.move_y = 0
    player_a.dash_x = 0
    player_a.dash_y = 0
    player_b.move_x = 0
    player_b.move_y = 0
    player_b.dash_x = 0
    player_b.dash_y = 0


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

    # set player colors
    playerA.color = VIOLET
    playerB.color = GOLD

    playerA.dashColor = MAGENTA
    playerB.dashColor = RED

    # Create all the levels
    level_list = []
    level_list.append(Level_01(playerA, playerB))

    # Set the current level
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    playerA.level = current_level
    playerB.level = current_level

    playerA.rect.x = current_level.a_start_x
    playerA.rect.y = current_level.a_start_y
    active_sprite_list.add(playerA)

    playerB.rect.x = current_level.b_start_x
    playerB.rect.y = current_level.b_start_y
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
                if event.key == pygame.K_j:
                    playerB.go_left()
                    playerB.leftPressed = True
                if event.key == pygame.K_l:
                    playerB.go_right()
                    playerB.rightPressed = True
                if event.key == pygame.K_i:
                    playerB.upPressed = True
                if event.key == pygame.K_k:
                    playerB.downPressed = True
                if event.key == pygame.K_QUOTE:
                    playerB.jump()
                if event.key == pygame.K_SEMICOLON:
                    playerB.dash()

            if event.type == pygame.KEYUP:

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
                if event.key == pygame.K_j:
                    playerB.go_right()
                    playerB.leftPressed = False
                if event.key == pygame.K_l:
                    playerB.go_left()
                    playerB.rightPressed = False
                if event.key == pygame.K_i:
                    playerB.upPressed = False
                if event.key == pygame.K_k:
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

        # ALL CODE TO DRAW SHOULD 2GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()

        # check if somebody won
        win_check(playerA, playerB, level_list, current_level, current_level_no, screen)

        # fps = clock.get_fps()
        # print fps

    pygame.quit()

if __name__ == "__main__":
    main()
