import pygame
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
promptFont = pygame.font.SysFont("Courier New", 30, bold=True, italic=True)
instructionFont  = pygame.font.SysFont("Courier New", 20, bold=False, italic=False)


# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640

textRows = 80
textColumns = 320
textHeight = SCREEN_HEIGHT / textRows
textWidth = SCREEN_WIDTH / textColumns

numLevels = 2

#import sounds
jump_sound = pygame.mixer.Sound("SoundEffects/jump.ogg")
attack_sound = pygame.mixer.Sound("SoundEffects/attack.ogg")
death_sound = pygame.mixer.Sound("SoundEffects/death.ogg")

# play background sounds
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load('SoundEffects/theme.ogg')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self):

        # Call the parent's constructor
        super(self.__class__, self).__init__()

        self.color = (0, 0, 0)
        self.dashColor = (0, 0, 0)

        # create score counter
        self.score = 0

        self.ded = False

        self.current_level_no  = 0

        # enable dashing
        self.canDash = True
        self.attacking = 0

        # set traps
        self.traps_left = 3

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
        self.platformBoost_y = 0
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
        self.platformBoost_y = 0

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if isinstance(block, Trap):
                if block.active:
                    self.ded = True
                    print "you ded"
            else:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y # + self.platformBoost_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if isinstance(block, Trap):
                if block.active:
                    self.ded = True
            else:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    if isinstance(block, MovingPlatform):
                        self.platformBoost_x = block.change_x
                        self.platformBoost_y = block.change_y
                        if self.platformBoost_y > 0:
                            self.change_y = self.platformBoost_y
                        else:
                            self.change_y = 0
                    else:
                        # Stop our vertical movement
                        self.change_y = 0

                    if not self.attacking:
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
        if len(platform_hit_list) > 0:
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

    def set_trap(self, player_a, player_b, current_level):
        if self.traps_left > 0:
            self.traps_left -= 1

            block = Trap(6, 8)
            block.rect.x = self.rect.x - textWidth
            block.rect.y = self.rect.y - textHeight
            block.player_a = player_a
            block.player_b = player_b
            current_level.platform_list.add(block)


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height, color):

        # super(self.__class__, self).__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width*textWidth, height*textHeight])
        self.image.fill(color)

        self.rect = self.image.get_rect()


class Trap(Platform):

    def __init__(self, height, width):
        # super(self.__class__, self).__init__(width, height)
        Platform.__init__(self, height, width, LGREY)
        self.active = False

    def update(self):
        if not pygame.sprite.collide_rect(self.player_a, self) and not pygame.sprite.collide_rect(self.player_b, self):
            self.active = True
            self.image.fill(DGREY)


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

    def __init__(self, width, height, color):
        # super(self.__class__, self).__init__(width, height)
        Platform.__init__(self, width, height, color)

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
            elif self.change_x > 0:
                # Otherwise if we are moving left, do the opposite.
                self.player_a.rect.left = self.rect.right

        # See if we hit playerB
        hit = pygame.sprite.collide_rect(self, self.player_b)
        if hit:

            if self.change_x < 0:
                self.player_b.rect.right = self.rect.left
            elif self.change_x > 0:
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

        print "new level"

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
            block = Platform(platform[0], platform[1], GREEN)
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player_a = self.player_a
            block.player_b = self.player_b
            self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(48, 2, GREEN)
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


# Create platforms for  level 2
class Level_02(Level):
    """ Definition for level 1. """

    def __init__(self, player_a, player_b):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player_a, player_b)

        # Array with width, height, x, and y of platform
        level = [[10, 80, 0, 0],  # left wall
                 [10, 80, 310, 0],  # right wall
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], GREEN)
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player_a = self.player_a
            block.player_b = self.player_b
            self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(50, 2, GREEN)
        block.rect.x = 30*textWidth
        block.rect.y = 34*textHeight
        block.boundary_bottom = 72*textHeight
        block.boundary_top = 10*textHeight
        block.change_y = textWidth
        block.player_a = self.player_a
        block.player_b = self.player_b
        block.level = self
        self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(50, 2, GREEN)
        block.rect.x = 100*textWidth
        block.rect.y = 52*textHeight
        block.boundary_bottom = 72*textHeight
        block.boundary_top = 10*textHeight
        block.change_y = textWidth
        block.player_a = self.player_a
        block.player_b = self.player_b
        block.level = self
        self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(50, 2, GREEN)
        block.rect.x = 170*textWidth
        block.rect.y = 70*textHeight
        block.boundary_bottom = 72*textHeight
        block.boundary_top = 10*textHeight
        block.change_y = -textWidth
        block.player_a = self.player_a
        block.player_b = self.player_b
        block.level = self
        self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(50, 2, GREEN)
        block.rect.x = 240*textWidth
        block.rect.y = 56*textHeight
        block.boundary_bottom = 72*textHeight
        block.boundary_top = 10*textHeight
        block.change_y = -textWidth
        block.player_a = self.player_a
        block.player_b = self.player_b
        block.level = self
        self.platform_list.add(block)

        self.a_start_x = 50*textWidth
        self.a_start_y = 26*textHeight
        self.b_start_x = 320*textWidth - 50*textWidth - player_b.rect.width
        self.b_start_y = 44*textHeight


# Create platforms for  level 3
class Level_03(Level):
    """ Definition for level 1. """

    def __init__(self, player_a, player_b):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player_a, player_b)

        # Array with width, height, x, and y of platform
        level = [[60, 4, 140, 62],  # bottom
                 [60, 4, 140, 14],  # top
                 [8, 4, 208, 54],
                 [8, 4, 208, 22],
                 [24, 4, 200, 50],
                 [8, 4, 216, 26],
                 [8, 8, 232, 38],  #nose
                 [8, 8, 124, 50],
                 [8, 4, 124, 26],
                 [8, 4, 116, 46],
                 [8, 4, 116, 30],
                 [8, 4, 108, 42],
                 # [8, 4, 108, 34],
                 [16, 4, 92, 46],
                 [16, 4, 92, 30],
                 [8, 4, 84, 50],
                 [8, 4, 84, 26],
                 [8, 4, 76, 54],
                 [8, 4, 76, 22],
                 [8, 4, 68, 58],
                 [8, 4, 68, 18],
                 [8, 12, 60, 46],
                 [8, 12, 60, 22],
                 [8, 4, 140, 42],  # side fin
                 [8, 4, 148, 38],  # side fin
                 [8, 4, 156, 34],  # side fin
                 [16, 4, 148, 46],  # side fin
                 [48, 4, 116, 70],  # bottom fin
                 [8, 4, 116, 66],  # bottom fin
                 [8, 4, 164, 66],  # bottom fin
                 [24, 4, 140, 6],  # top fin
                 [16, 4, 124, 10],  # top fin
                 [16, 4, 116, 14],  # top fin
                 [8, 4, 164, 10],  # top fin
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], GREEN)
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player_a = self.player_a
            block.player_b = self.player_b
            self.platform_list.add(block)

        eye = [[2, 4, 200, 32],
               [2, 6, 202, 31],
               [8, 8, 204, 30],
               [2, 6, 212, 31],
               [2, 4, 214, 32],
               ]

        for platform in eye:
            block = Trap(platform[0], platform[1])
            block.rect.x = platform[2]*textWidth
            block.rect.y = platform[3]*textHeight
            block.player_a = self.player_a
            block.player_b = self.player_b
            self.platform_list.add(block)

        self.a_start_x = 180*textWidth
        self.a_start_y = 4*textHeight
        self.b_start_x = 180*textWidth
        self.b_start_y = 52*textHeight


def win_check(player_a, player_b, level_list, current_level, screen):
    if pygame.sprite.collide_rect(player_a, player_b):
        if player_a.attacking and player_b.attacking:
            print "Tie"
            death_sound.play()
            pause(player_a, player_b, 5000, screen, 0, False)
            load_level(player_a, player_b, False, level_list, current_level)
        elif player_a.attacking or player_b.ded:
            print "A Wins"
            death_sound.play()
            player_a.score += 1
            pause(player_a, player_b, 5000, screen, 1, False)
            load_level(player_a, player_b, True, level_list, current_level)
        elif player_b.attacking or player_a.ded:
            print "B Wins"
            death_sound.play()
            player_b.score += 1
            pause(player_a, player_b, 5000, screen, 2, False)
            load_level(player_a, player_b, True, level_list, current_level)
        else:
            print "Nobody attacking"

    if player_a.ded and player_b.ded:
        print "Tie"
        death_sound.play()
        pause(player_a, player_b, 5000, screen, 0, True)
        load_level(player_a, player_b, False, level_list, current_level)
    elif player_b.ded:
        print "A Wins"
        death_sound.play()
        player_a.score += 1
        pause(player_a, player_b, 5000, screen, 1, True)
        load_level(player_a, player_b, True, level_list, current_level)
    elif player_a.ded:
        print "B Wins"
        death_sound.play()
        player_b.score += 1
        pause(player_a, player_b, 5000, screen, 2, True)
        load_level(player_a, player_b, True, level_list, current_level)

    player_a.ded = False
    player_b.ded = False


def pause(player_a, player_b, min_duration, screen, winner, trapped):

    pygame.mixer.music.pause()

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
    if trapped:
        if winner == 1:
            botRectTop = player_b.rect.y + 9 * textHeight
            topRectBot = player_b.rect.y - 3 * textHeight
        if winner == 2:
            botRectTop = player_a.rect.y + 9 * textHeight
            topRectBot = player_a.rect.y - 3 * textHeight
    elif player_a.rect.y <= player_b.rect.y:
        botRectTop = player_b.rect.y + 9 * textHeight
        topRectBot = player_a.rect.y - 3 * textHeight
    else:
        botRectTop = player_a.rect.y + 9 * textHeight
        topRectBot = player_b.rect.y - 3 * textHeight
    pygame.draw.rect(screen, BLACK, [0, 0, SCREEN_WIDTH, topRectBot])
    pygame.draw.rect(screen, BLACK, [0, botRectTop, SCREEN_WIDTH, SCREEN_HEIGHT - botRectTop])

    # draw text
    if winner == 0:
        title = titleFont.render("Tie", True, WHITE)
        title_width, title_height = titleFont.size("Tie")
    elif winner == 1:
        title = titleFont.render("Player A Wins", True, WHITE)
        title_width, title_height = titleFont.size("Player A Wins")
    elif winner == 2:
        title = titleFont.render("Player B Wins", True, WHITE)
        title_width, title_height = titleFont.size("Player B Wins")

    score_text = "Player A: " + str(player_a.score) + "                             Player B: " + str(player_b.score)
    text = scoreFont.render(score_text, True, WHITE)
    score_width, score_height = scoreFont.size(score_text)

    if topRectBot > 50 + title_height + 16 + score_height + 36:
        textY = 50
    else:
        textY = botRectTop + 36
    screen.blit(title, [(SCREEN_WIDTH-title_width)/2, textY])
    screen.blit(text, [(SCREEN_WIDTH-score_width)/2, textY + title_height + 16])


    prompt_text = "release all keys to proceed to round " + str(player_a.score + player_b.score + 1)
    text = promptFont.render(prompt_text, True, WHITE)
    prompt_width, prompt_height = promptFont.size(prompt_text)
    if botRectTop > SCREEN_HEIGHT - prompt_height - 72:
        screen.blit(text, [(SCREEN_WIDTH - prompt_width)/2, topRectBot - prompt_height - 36])
    else:
        screen.blit(text, [(SCREEN_WIDTH - prompt_width)/2, SCREEN_HEIGHT - prompt_height - 36])

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

    pygame.mixer.music.unpause()


def load_level(player_a, player_b, change_level, level_list, current_level):
    if change_level:
        new_rand = random.randint(0, 2)
        while new_rand == player_a.current_level_no:
            new_rand = random.randint(0, 2)
        player_a.current_level_no = new_rand

    current_level.platform_list.empty()
    current_level = level_list[player_a.current_level_no]
    current_level.__init__(player_a, player_b)
    # current_level.update()

    print player_a.current_level_no

    player_a.level = current_level
    player_b.level = current_level

    player_a.rect.x = current_level.a_start_x
    player_a.rect.y = current_level.a_start_y

    player_b.rect.x = current_level.b_start_x
    player_b.rect.y = current_level.b_start_y

    player_a.attacking = 0
    player_b.attacking = 0

    player_a.traps_left = 3
    player_b.traps_left = 3

    player_a.move_x = 0
    player_a.move_y = 0
    player_a.dash_x = 0
    player_a.dash_y = 0
    player_b.move_x = 0
    player_b.move_y = 0
    player_b.dash_x = 0
    player_b.dash_y = 0


def menu(screen):
    screen.fill(BLACK)

    title = titleFont.render("Decker Duels", True, WHITE)
    title_width, title_height = titleFont.size("Decker Duels")
    screen.blit(title, [(SCREEN_WIDTH-title_width)/2, 80])

    byline = scoreFont.render("by Ezra Robinson", True, WHITE)
    byline_width, byline_height = scoreFont.size("by Ezra Robinson")
    screen.blit(byline, [(SCREEN_WIDTH-byline_width)/2, 100 + title_height])

    a_controls = ['[w]','[a]','[s]','[d]','[f]','[g]','[c]']
    b_controls = ['[i]','[j]','[k]','[l]','[;]','[\']','[.]']
    control_names = ['CONTROLS:','up()','left()','down()','right()','jump()','attack()','corrupt()']
    control_width, control_height = instructionFont.size("[w]")
    i = 1
    for line in a_controls:
        i += 1
        text = instructionFont.render(line, True, WHITE)
        screen.blit(text, [SCREEN_WIDTH * 0.3, 140 + title_height + byline_height + control_height * i])
    i = 1
    for line in b_controls:
        i += 1
        text = instructionFont.render(line, True, WHITE)
        screen.blit(text, [0.7 * SCREEN_WIDTH - control_width, 140 + title_height + byline_height + control_height * i])
    i = 0
    for line in control_names:
        i += 1
        text = instructionFont.render(line, True, WHITE)
        control_width, control_height = instructionFont.size(line)
        screen.blit(text, [(SCREEN_WIDTH - control_width) / 2, 140 + title_height + byline_height + control_height * i])

    intrs = scoreFont.render("playerA:          press up() to jack in          playerB:", True, WHITE)
    intrs_width, intrs_height = scoreFont.size("playerA:          press up() to jack in          playerB:")
    screen.blit(intrs, [(SCREEN_WIDTH-intrs_width)/2, SCREEN_HEIGHT-150])

    pygame.display.update()

    ready_a = False
    ready_b = False

    while not ready_a or not ready_b:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ready_a, ready_b = True

            if event.type == pygame.KEYDOWN:
                # playerA Controls
                if event.key == pygame.K_w:
                    ready_a = True
                    jackedA = promptFont.render("ready                                                    ", True, RED)
                    jackedA_width, jackedA_height = promptFont.size("ready                                                    ")
                    screen.blit(jackedA, [(SCREEN_WIDTH-jackedA_width)/2, SCREEN_HEIGHT-140+intrs_height])
                    pygame.display.update()
                if event.key == pygame.K_i:
                    ready_b = True
                    jackedB = promptFont.render("                                                 ready   ", True, RED)
                    jackedB_width, jackedB_height = promptFont.size("                                                 ready   ")
                    screen.blit(jackedB, [(SCREEN_WIDTH-jackedB_width)/2, SCREEN_HEIGHT-140+intrs_height])
                    pygame.display.update()

    for i in range (0, 3):
        pygame.time.delay(1000)
        # attack_sound.play()
        screen.fill(BLACK)
        countdown = titleFont.render(str(3 - i), True, WHITE)
        countdown_width, countdown_height = titleFont.size(str(3 - i))
        screen.blit(countdown, [(SCREEN_WIDTH-countdown_width)/2, (SCREEN_HEIGHT-countdown_height)/2])
        pygame.display.update()

    pygame.time.delay(1000)
    # death_sound.play()


def main():
    """ Main Program """

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Decker Duels")

    # bring up the menu
    menu(screen)

    # Create the player
    playerA = Player()
    playerB = Player()

    # set player colors
    playerA.color = VIOLET
    playerB.color = GOLD

    playerA.dashColor = MAGENTA
    playerB.dashColor = RED

    # Create all the levels
    level_list = [Level_01(playerA, playerB), Level_02(playerA, playerB), Level_03(playerA, playerB)]

    # Set the current level
    playerA.current_level_no = 0
    current_level = level_list[playerA.current_level_no]

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

            # restart song when reaches end
            if event.type == pygame.constants.USEREVENT:
                pygame.mixer.music.play()

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
                if event.key == pygame.K_c:
                    playerA.set_trap(playerA, playerB, current_level)

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
                if event.key == pygame.K_PERIOD:
                    playerB.set_trap(playerA, playerB, current_level)

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

        # Update items in the level
        current_level.update()

        # Update the players
        active_sprite_list.update()

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
        current_level = level_list[playerA.current_level_no]
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(24)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()

        # check if somebody won
        win_check(playerA, playerB, level_list, current_level, screen)

        # fps = clock.get_fps()
        # print fps

    pygame.quit()

if __name__ == "__main__":
    main()
