import pygame
import random
import math
import json
from spritesheet import Spritesheet
from pygame import mixer

# -- Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (46, 204, 113)
ORANGE = (211, 84, 0)
PURPLE = (125, 60, 152)
AQUA = (22, 160, 133)
PINK = (255, 89, 222)
BROWN = (165, 42, 42)
CHOCOLATE = (210, 105, 30)
GREY = (128, 128, 128)
LIGHTBLUE = (173,216,230)
COLOUR = [WHITE, BLUE, YELLOW, RED, GREEN, ORANGE, PURPLE,
          AQUA, PINK, BROWN, CHOCOLATE, GREY, LIGHTBLUE]

# -- Initialise PyGame
pygame.init()

# -- Font
PLAYfont = pygame.font.SysFont('comicsans', 60)
font = pygame.font.Font('freesansbold.ttf', 20)
bigfont = pygame.font.Font('freesansbold.ttf', 32)

# -- Manages how fast screen refreshes

clock = pygame.time.Clock()

# -- Blank Screen

size = (1280, 720)
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

# -- Title of new window/screen
pygame.display.set_caption("GAME")

### -------------------------------------------------------------------Graphics----------------------------------------------------------------------###
Cone = pygame.image.load('graphics/VisionCone/viscone.png')
ConeU = pygame.image.load('graphics/VisionCone/viscone up.png')
ConeD = pygame.image.load('graphics/VisionCone/viscone down.png')
ConeR = pygame.image.load('graphics/VisionCone/viscone right.png')
ConeL = pygame.image.load('graphics/VisionCone/viscone left.png')
ConeGraphics = [ConeU, ConeD, ConeR, ConeL]

KeyImage = pygame.image.load('graphics/KEY.png')

spritesheet = Spritesheet('graphics/BIGspritesheet.png')
# ---Player object textures are loaded
CharUp = [spritesheet.parse_sprite('charup1.png'), spritesheet.parse_sprite('charup2.png'),
          spritesheet.parse_sprite('charup3.png'), spritesheet.parse_sprite('charup4.png')]
CharDown = [spritesheet.parse_sprite('chardown1.png'), spritesheet.parse_sprite('chardown2.png'),
            spritesheet.parse_sprite('chardown3.png'), spritesheet.parse_sprite('chardown4.png')]
CharRight = [spritesheet.parse_sprite('charright1.png'), spritesheet.parse_sprite('charright2.png'),
             spritesheet.parse_sprite('charright3.png'), spritesheet.parse_sprite('charright4.png')]
CharLeft = [spritesheet.parse_sprite('charleft1.png'), spritesheet.parse_sprite('charleft2.png'),
            spritesheet.parse_sprite('charleft3.png'), spritesheet.parse_sprite('charleft4.png')]

CharUpRight = [spritesheet.parse_sprite('charupright1.png'), spritesheet.parse_sprite('charupright2.png'),
               spritesheet.parse_sprite('charupright3.png'), spritesheet.parse_sprite('charupright4.png')]
CharUpLeft = [spritesheet.parse_sprite('charupleft1.png'), spritesheet.parse_sprite('charupleft2.png'),
              spritesheet.parse_sprite('charupleft3.png'), spritesheet.parse_sprite('charupleft4.png')]
CharDownRight = [spritesheet.parse_sprite('chardownright1.png'), spritesheet.parse_sprite('chardownright2.png'),
                 spritesheet.parse_sprite('chardownright3.png'), spritesheet.parse_sprite('chardownright4.png')]
CharDownLeft = [spritesheet.parse_sprite('charupleft1.png'), spritesheet.parse_sprite('charupleft2.png'),
                spritesheet.parse_sprite('charupleft3.png'), spritesheet.parse_sprite('charupleft4.png')]
#----Moving Enemy textures are loaded
Enemy3Up = [spritesheet.parse_sprite('enemy3up1.png'), spritesheet.parse_sprite('enemy3up2.png'),
            spritesheet.parse_sprite('enemy3up3.png'), spritesheet.parse_sprite('enemy3up4.png')]
Enemy3Down = [spritesheet.parse_sprite('enemy3down1.png'), spritesheet.parse_sprite('enemy3down2.png'),
              spritesheet.parse_sprite('enemy3down3.png'), spritesheet.parse_sprite('enemy3down4.png')]
Enemy3Right = [spritesheet.parse_sprite('enemy3right1.png'), spritesheet.parse_sprite('enemy3right2.png'),
               spritesheet.parse_sprite('enemy3right3.png'), spritesheet.parse_sprite('enemy3right4.png')]
Enemy3Left = [spritesheet.parse_sprite('enemy3left1.png'), spritesheet.parse_sprite('enemy3left2.png'),
              spritesheet.parse_sprite('enemy3left3.png'), spritesheet.parse_sprite('enemy3left4.png')]


## ---------------------------------------------------------------------Classes-----------------------------------------------------------------------##
class Player(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, name):
        super().__init__()
        self.filename = name
        self.keycollected = False
        self.colenemy = False  # Boolean variable to hold whether the player has collided with any enemies
        self.speed = 5
        self.direction_x = 0
        self.direction_y = 0
        self.colour = colour
        self.counter = 0

        self.width = spritesheet.get_width(self.filename) #width and height are calculated using the texture that gets loaded
        self.height = spritesheet.get_height(self.filename)
        self.image = spritesheet.parse_sprite(self.filename)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.index = 0
        # add all textures

    def get_centre(self):   #fucntion that returns the centre coordinates of the player object
        centre_x = self.rect.x + (self.width/2)
        centre_y = self.rect.y + (self.height/2)
        return [centre_x, centre_y]

    def get_key_state(self):    #getter fucntion that indicates whether the key is collected.
        return self.keycollected

    def set_key_state(self):    #setter function for setting the state of the key colletion
        self.keycollected = True

    def get_colenemy_state(self): # getter and setter fucntions that get and alter the state of a variable that determines level failure
        return self.colenemy

    def set_colenemy_state(self, state):
        self.colenemy = state

    # player movement methods
    def go_up(self):
        self.direction_y = self.speed * -1

    def go_down(self):
        self.direction_y = self.speed

    def go_right(self):
        self.direction_x = self.speed

    def go_left(self):
        self.direction_x = self.speed * -1

    def stop_x(self):
        self.direction_x = 0

    def stop_y(self):
        self.direction_y = 0

    def update(self):
        # ------Level border collision logic and movement
        if (self.rect.x >= 0 and self.rect.x <= (1000 - self.width)) and (
                self.rect.y >= 0 and self.rect.y <= (720 - self.height)):
            self.rect.x += self.direction_x
            self.rect.y += self.direction_y
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > (1000 - self.width):
            self.rect.x = (1000 - self.width)
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > (720 - self.height):
            self.rect.y = (720 - self.height)

        # -------Obstacle collision Logic

        obstacle_hit_group = pygame.sprite.groupcollide(player_group, obstacle_group, False, False)
        for player in obstacle_hit_group:
            self.rect.x -= self.direction_x
            self.rect.y -= self.direction_y

        # ------ Exit closed check
        exit_hit_group = pygame.sprite.groupcollide(player_group, exit_group, False, False)

        for elem in exit_hit_group:
            if not self.get_key_state():
                no_key_text()

        # ------- Enemy    collision
            #---Collision with the enemy detection area
        enemyarea_hit_group = pygame.sprite.spritecollide(self, enemy_vision_group, False)
        for elem in enemyarea_hit_group:
            obstacle_enemyarea_hit_group = pygame.sprite.spritecollide(elem, obstacle_group, False) #to make sure the corrrect detarea was being checked
            if len(obstacle_enemyarea_hit_group) == 0:       #to make sure no detections through the wall happen
                print('collided with enemy detection area')
                self.colenemy = True

            #---Proximity Detection
        for elem in enemy_group:
            enemy_loc =elem.get_centre()
            player_loc = self.get_centre()
            distance = round(math.sqrt((enemy_loc[0]-player_loc[0])**2+(enemy_loc[1]-player_loc[1])**2))
            if distance<60:
                print('level failure due to proximity detection')
                self.colenemy = True

            # --- Vision Detection





        # ------Key Collection Logic (opens the gate)
        key_hit_group = pygame.sprite.groupcollide(player_group, key_group, False, True)
        for elem in key_hit_group:
            for item in exit_group:
                print('key collected')
                item.state_change(1)
                self.key_collected = True

        # -> additional logic of collection indicator in the info menu can be added
        # ---Wirtten later in the code where the text displaying logic is

        # -> Logic for finishing a level after the key is collected
        # --- Also added later on in the code, using a text function.

        # --------------- Texture FLipping          There are 8 outcomes of this massive selective case, each one chooses the texture and animation depending on which of the 8 directions the player i facing
        self.counter = (self.counter + 1) % 5
        if self.counter == 0:           #depeding on the direction being moved, negative or positive in the vertical or horizontal axis determinde the textrue that gets displayed for this object durign a running level
            if self.direction_y < 0:
                if self.direction_x > 0:

                    self.image = CharUpRight[self.index]
                    self.index = (self.index + 1) % len(CharUpRight)    #list of elements that are being repeated circularly to give the effect of a complete flip book.
                elif self.direction_x < 0:

                    self.image = CharUpLeft[self.index]
                    self.index = (self.index + 1) % len(CharUpLeft)

                self.image = CharUp[self.index]
                self.index = (self.index + 1) % len(CharUp)
            elif self.direction_y > 0:

                if self.direction_x < 0:

                    self.image = CharDownRight[self.index]
                    self.index = (self.index + 1) % len(CharDownRight)
                elif self.direction_x < 0:

                    self.image = CharDownLeft[self.index]
                    self.index = (self.index + 1) % len(CharDownLeft)

                self.image = CharDown[self.index]
                self.index = (self.index + 1) % len(CharDown)

            elif self.direction_y == 0:

                if self.direction_x > 0:

                    self.image = CharRight[self.index]
                    self.index = (self.index + 1) % len(CharRight)
                elif self.direction_x < 0:

                    self.image = CharLeft[self.index]
                    self.index = (self.index + 1) % len(CharLeft)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, speed):
        super().__init__()
        self.colour = BLUE
        self.facing = facing
        self.direction_x = 0
        self.direction_y = 0  # -1 in y is UP!
        self.speed = speed

        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # all instances of enemies face different sides at the start, this initialises their direction
        if self.facing == 61:  # Facing up
            self.direction_y = -1
        elif self.facing == 62:  # Facing Down
            self.direction_y = 1
        elif self.facing == 63:  # facing right
            self.direction_x = 1
        elif self.facing == 64:  # facing left
            self.direction_x = -1


    def get_centre(self):   #funtion returning the centre coordinates of the object
        centre_x = self.rect.x + (self.width/2)
        centre_y = self.rect.y + (self.height/2)
        return [centre_x, centre_y]

class Enemy1(Enemy):        #first type of enemy -static, so no update method
    def __init__(self, x, y, facing, speed):

        self.colour = RED
        super().__init__(x, y, facing, speed)

        if facing == 61:
            self.image = spritesheet.parse_sprite('enemy1up.png')
        elif facing == 62:
            self.image = spritesheet.parse_sprite('enemy1down.png')
        elif facing == 63:
            self.image = spritesheet.parse_sprite('enemy1right.png')
        elif self.facing == 64:
            self.image = spritesheet.parse_sprite('enemy1left.png')


class Enemy2(Enemy):    #second type of enemy
    def __init__(self, x, y, facing, speed):
        self.speed = 0
        self.colour = PINK
        self.facing = facing
        self.orientation_list = [61, 63, 62, 64]  # in order: up, right, down, left
        self.index = 1
        super().__init__(x, y, facing, speed)
        self.orientation_selector()

    def orientation_selector(self): #returns the correct texture depending on which was the object is facing
        if self.facing == 61:
            self.image = spritesheet.parse_sprite('enemy2up.png')
            self.o_list_pointer = 0
        elif self.facing == 62:  # down
            self.image = spritesheet.parse_sprite('enemy2down.png')
            self.o_list_pointer = 2
        elif self.facing == 63:  # right
            self.image = spritesheet.parse_sprite('enemy2right.png')
            self.o_list_pointer = 1
        elif self.facing == 64:
            self.image = spritesheet.parse_sprite('enemy2left.png')
            self.o_list_pointer = 3

    def update(self):       #enemy is stationary but rotates hence the update function is used


        self.index = (self.index + 1) % self.speed  
        if self.index == 0:
            self.o_list_pointer = (self.o_list_pointer + 1) % len(self.orientation_list)
            self.facing = self.orientation_list[self.o_list_pointer]
            self.orientation_selector()


class Enemy3(Enemy):
    def __init__(self, x, y, facing, speed):

        self.colour = ORANGE

        self.counter = 0
        super().__init__(x, y, facing, speed)
        self.speed = 1 # speed is now provided as an argument  0 speed means no movement                    #!!!!!!!!!!!!! speed = 1 when movement is needed
        self.speedcounter = 0
        self.index = 0
        if facing == 61:
            self.image = spritesheet.parse_sprite('enemy3up1.png')
        elif facing == 62:
            self.image = spritesheet.parse_sprite('enemy3down1.png')
        elif facing == 63:
            self.image = spritesheet.parse_sprite('enemy3right1.png')
        elif self.facing == 64:
            self.image = spritesheet.parse_sprite('enemy3left1.png')

    def update(self):
        #self.speedcounter = (self.speedcounter +1) %2      #unhashign the code halves te speed of the enemies
        #movement behaviour, moves in the direction it faces until it faces an enemy obstalce
        if self.direction_x != 0 and self.speedcounter ==0:
            self.rect.x += self.direction_x * self.speed
        if self.direction_y != 0 and self.speedcounter ==0:
            self.rect.y += self.direction_y * self.speed
        #upoin colluision with an enemy obstacle...
        enemyobs_hit_group = pygame.sprite.spritecollide(self, enemyobs_group, False)
        #... it moves back to a state before the collision then changes direction depending on which way the enemy obstacle points towards
        #elem is the enemy obstacle that the collision is detected with
        for elem in enemyobs_hit_group:
            self.rect.x -= self.speed * self.direction_x
            self.rect.y -= self.speed * self.direction_y
            self.direction_x = elem.get_direction_x()
            self.direction_y = elem.get_direction_y()
        #driection faced is changed hence the variable is updated
        if self.direction_y<0:  #up
            self.facing =61
        elif self.direction_y>0:    #down
            self.facing =62
        if self.direction_x>0:  #right
            self.facing = 63
        elif self.direction_x<0:    #left
            self.facing = 64
        #this is the speed of the animation of the movement of the enemies
        self.counter = (self.counter + 1) % 5
        if self.counter == 0:
            if self.direction_y < 0:
                self.image = Enemy3Up[self.index]
                self.index = (self.index + 1) % len(Enemy3Up)   #same circular mechanism implemented for the player class
            if self.direction_y > 0:
                self.image = Enemy3Down[self.index]
                self.index = (self.index + 1) % len(Enemy3Down)
            if self.direction_x < 0:
                self.image = Enemy3Left[self.index]
                self.index = (self.index + 1) % len(Enemy3Left)
            if self.direction_x > 0:
                self.image = Enemy3Right[self.index]
                self.index = (self.index + 1) % len(Enemy3Right)

class EnemyVision(Enemy):           #inheritor of enemy group, creates the detection area for enemies
    def __init__(self, x, y,width, height, centre_pos, facing):
        speed = 0
        super().__init__(x, y, facing, speed)
        self.centre_pos = centre_pos
        self.colour = LIGHTBLUE
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_pos_change(self, newcentre_pos):  #method that recognises the enemy the vision area belongs to has changed direction.
        if self.centre_pos[0] == newcentre_pos[0] and self.centre_pos[1] == newcentre_pos[1]:
            return False
        return True


    def re_shaper(self, facing, centre_pos): #the dimensions, coordinates and the vision sprite changes, this is reshaped depending on which way the enemy object is
        self.facing = filter                #for every orientation of the detection area the dimensions are decribed slightly differently, 
        if self.facing == 61:  # Facing up
            width = 50
            height = 100
            self.rect.x = centre_pos[0] - (width / 2)
            self.rect.y = centre_pos[1] - height
        elif self.facing == 62:  # Facing Down
            width = 50
            height = 100
            self.rect.x = centre_pos[0] - (width / 2)
            self.rect.y = centre_pos[1]
        elif self.facing == 63:  # facing right
            width = 100
            height = 50
            self.rect. x = centre_pos[0]
            self.rect.y = centre_pos[1] - (height / 2)
        elif self.facing == 64:  # facing left
            width = 100
            height = 50
            self.rect.x = centre_pos[0] - width
            self.rect.y = centre_pos[1] - (height / 2)


        self.image = pygame.transform.scale(self.image,(width, height))
        temp_x = self.rect.x
        temp_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = temp_x
        self.rect.y = temp_y

    def update(self):
        enemy_hit_group = pygame.sprite.spritecollide(self, enemy_group, False) #update method is for detecting whent he area needs ot be reshaped

        for elem in enemy_hit_group:
            #print("live collision")
            if self.facing != elem.facing:      #if enemy changes direction, then the area must be recalculated
                #print(elem.facing)
                self.re_shaper(elem.facing, elem.get_centre())
            elif  self.check_pos_change(elem.get_centre()):  #checks the centre of the vision with the enemy it corresponds to, if different it recalculates the area.
                self.re_shaper(elem.facing,elem.get_centre())

#default purple enemybostacles are redundant as they have no funsitonality.
class EnemyObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, facing):
        super().__init__()
        self.facing = facing
        self.direction_y = 0
        self.direction_x = 0
        self.colour = PURPLE  # purple is the original colour
        # the blocks with rotation have white colour
        if self.facing == 91:  # UP
            self.direction_y = -1
            self.colour = WHITE
        elif self.facing == 92:  # DOWN
            self.direction_y = 1
            self.colour = WHITE
        elif self.facing == 93:  # RIGHT
            self.direction_x = 1
            self.colour = WHITE
        elif self.facing == 94:  # LEFT
            self.direction_x = -1
            self.colour = WHITE

        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_direction_x(self): #getter setter methods for the direction attribute of the enemyobstacles, these are for shaping the movement of enemy type 3
        return self.direction_x

    def get_direction_y(self):
        return self.direction_y


class Obstacle(pygame.sprite.Sprite): #the next 3 classes are elementary objects with not much functionality
    def __init__(self, x, y, w, h):
        super().__init__()
        self.colour = AQUA
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.graphic = KeyImage
        # self.colour = YELLOW
        self.width = 24
        self.height = 12
        self.image = pygame.transform.scale(self.graphic, (self.width, self.height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.colour = RED
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0  # exit closed by default

    def get_state(self):    #has state updates as the look and the functionality of a exit differs 
        return self.state

    def change_colour(self, colour):
        self.colour = colour
        self.image.fill(self.colour)

    def state_change(self, state):
        self.state = int(state)
        # state = 0 -> exit is closed   hence level cannot be completed
        # state = 1 -> exit is open


class Button():
    def __init__(self, colour, x, y, width, height, font, text=''):
        self.colour = colour
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.x = x
        self.y = y

    def set_text(self, value):
        self.text = value

    def draw(self, screen, outline=None):
        # Method to draw the button and its text onto the screen, creates a text box on top of a sprite object 
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = self.font.render(self.text, 1, BLACK)
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):  #decision method that checks whether the cursor is hovering over a button
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

class Background(pygame.sprite.Sprite): #elementary class that loads the backgroud image.
    def __init__(self, name):
        super().__init__()

        self.image = pygame.image.load(name).convert()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update_image(self, name):
        self.image = pygame.image.load(name)



##---------------------------------------------------------------------Functions/Procedures---------------------------------------------------------------------##


def set_level_colour(num, colour):      #used to chagne level colour depending on completion
    level_buttons[num].colour = colour


def reset_level_colour(num, colour):
    level_buttons[num].colour = colour


def level_selector(num):    #selecting case statement that runs he correct procedure to create the level on the screen
    num = int(num)
    if num == 1:
        level_1(num)
    if num == 2:
        level_2(num)
    if num == 3:
        level_3(num)
    if num == 4:
        level_4(num)
    if num == 5:
        level_5(num)
    if num == 6:
        level_6(num)
    if num == 7:
        level_7(num)
    if num == 8:
        level_8(num)
    if num == 9:
        level_9(num)
    if num == 10:
        level_10(num)


def level_clear():  # clears all the objects in all sprite groups
    all_sprites_group.empty()
    obstacle_group.empty()
    player_group.empty()
    enemy_group.empty()
    enemyobs_group.empty()
    key_group.empty()
    exit_group.empty()
    enemy_vision_group.empty()


#using the 2d list that is fed in, generates the bostacles by treating every index of the list as a placeholder for an area of 10x10px
def map_creator(layout):
    for y in range(len(layout)):
        for x in range(len(layout[y])):

            if layout[y][x] == 1:
                # places obstacle (followed +2 with width and height)
                create_obstacle(x * 10, y * 10, int(layout[y][x + 1]), int(layout[y][x + 2]))

            elif layout[y][x] == 2:
                # player spawn
                create_player(x * 10, y * 10, layout[y][x + 1])

            elif layout[y][x] == 3:
                # places exit (+2 for w and h)
                create_exit(x * 10, y * 10, int(layout[y][x + 1]), int(layout[y][x + 2]))

            elif layout[y][x] == 4:
                # places key
                create_key(x * 10, y * 10)

            ##            if layout[y][x] == 5:
            ##                # 5 IS NOT DEFINED IN THE MAP CREATION KEY

            elif layout[y][x] == 6:  # --- *1 = up, *2 = down, *3= right, *4 = left ---#
                # enemy type 1 (followed by +1 orientation)

                create_enemy(x * 10, y * 10, 1, int(layout[y][x + 1]), 0)  # enemy1 doesn't move, hence speed = 0

            elif layout[y][x] == 7:
                # enemy type 2 (followed by +1 orientation and speed)
                create_enemy(x * 10, y * 10, 2, int(layout[y][x + 1]), layout[y][x + 2])

            elif layout[y][x] == 8:
                # enemy type 3 (+2 orientation and speed)
                create_enemy(x * 10, y * 10, 3, int(layout[y][x + 1]), layout[y][x + 2])

            elif layout[y][x] == 9:
                # enemy obstacle (+1 rotation)
                if int(layout[y][x + 1]) != 0:  # <---- REMOVE this line to get back the default enemy obstacles.
                    create_enemyobstacle(x * 10, y * 10, int(layout[y][x + 1]))


def level_complete(level): #chagnes the level button colour information upon completion
    level = int(level) - 1
    level_colour_data[level] = [GREEN, AQUA]


###------------------------------------Level Creation Functions---------------------------------###
def level_1(num):
    Background.update_image('graphics/Backgrounds/Level1.png')
    print('level 1 - Tutorial Level')
    leveltext_creator(num)
    create_player(300, 500, 21)
    create_obstacle(380, 0, 60, 180)
    create_obstacle(380, 435, 60, 285)
    create_key(300, 300)
    create_exit(500, 0, 200, 50)
    create_enemy(400, 400, 1, 61, 0)
    create_enemy(500, 500, 2, 61, 150)
    create_enemy(600, 600, 3, 61, 1)
    create_enemyobstacle(600, 300, 92)  # has direction direction
    create_enemyobstacle(700, 300, 0)  # normal enemyobstacle object // redundant no longer needed in the game


def level_2(num):
    Background.update_image('graphics/Backgrounds/Level2.png')
    leveltext_creator(num)
    print('level 2 - Test Level')
    create_player(300, 500, 21)
    create_obstacle(100, 100, 100, 200)
    create_key(550, 50)
    create_exit(500, 0, 200, 50)
    create_enemy(400, 400, 1, 61, 0)
    create_enemy(500, 500, 2, 61, 150)
    create_enemy(600, 600, 3, 61, 1)
    create_enemyobstacle(600, 300, 92)  # has direction direction
    create_enemyobstacle(700, 300, 0)  # normal enemyobstacle object

def level_3(num):
    Background.update_image('graphics/Backgrounds/Level3.png')
    leveltext_creator(num)
    print('level 3')
    level_file = open('levels/level3.json', 'rt')
    layout = json.load(level_file)
    level_file.close()
    map_creator(layout)


def level_4(num):
    Background.update_image('graphics/Backgrounds/Level4.png')
    leveltext_creator(num)
    print('level 4')


def level_5(num):
    Background.update_image('graphics/Backgrounds/Level5.png')
    leveltext_creator(num)
    print('level 5')


def level_6(num):
    Background.update_image('graphics/Backgrounds/Level6.png')
    leveltext_creator(num)
    print('level 6')


def level_7(num):
    Background.update_image('graphics/Backgrounds/Level7.png')
    leveltext_creator(num)
    print('level 7')


def level_8(num):
    Background.update_image('graphics/Backgrounds/Level8.png')
    leveltext_creator(num)
    print('level 8')


def level_9(num):
    Background.update_image('graphics/Backgrounds/Level9.png')
    leveltext_creator(num)
    print('level 9')


def level_10(num):
    Background.update_image('graphics/Backgrounds/Level10.png')
    leveltext_creator(num)
    print("level 10")


###----------------------- Sprite Creation -----------------------------### procedures that create the sprites with correct attributes in the given locations, interacts with map_creator function
def create_player(x, y, orientation):
    global player
    if orientation == 21:
        name = 'charup1.png'
    elif orientation == 22:
        name = 'chardown1.png'
    elif orientation == 23:
        name = 'charright1.png'
    elif orientation == 24:
        name = 'charleft1.png'

    player_group.empty()  # -- there can only be 1 player at one time!
    player = Player(BLUE, x, y, name)
    player_group.add(player)
    all_sprites_group.add(player)


def create_obstacle(x, y, w, h):
    global obstacle
    obstacle = Obstacle(x, y, w, h)
    obstacle_group.add(obstacle)
    #all_sprites_group.add(obstacle)    #Obstacles get drawn on screen when this line is not hashed


def create_exit(x, y, w, h):
    global exit_
    exitblock = Exit(x, y, w, h)
    exit_group.add(exitblock)
    all_sprites_group.add(exitblock)


def create_key(x, y):
    global key
    key = Key(x, y)
    key_group.add(key)
    all_sprites_group.add(key)


def create_enemy(x, y, e_type, facing, speed):
    global enemy

    if e_type == 1:
        enemy = Enemy1(x, y, facing, speed)
    elif e_type == 2:
        enemy = Enemy2(x, y, facing, speed)
    elif e_type == 3:
        enemy = Enemy3(x, y, facing, speed)

    enemy_group.add(enemy)
    all_sprites_group.add(enemy)
    #if e_type == 2 and len(enemy_vision_group)<1:  //was used for a test, might be redundant code
    create_enemy_detection_area(enemy)

def create_enemyobstacle(x, y, facing):
    global enemy_obs
    enemy_obs = EnemyObstacle(x, y, facing)
    enemyobs_group.add(enemy_obs)
    #all_sprites_group.add(enemy_obs)  # ----!!!!!line should be hashed so that the enemyobs are not visible to the user


def create_enemy_detection_area(elem):   #elem is the enemy that the area is being created for, every enemy object gets another object that inherits form the enemy class to become its vision area.
    centre_pos = elem.get_centre()
    direction = elem.facing
    if  direction== 61:  # Facing up
        width = 50
        height = 100
        x = centre_pos[0] - (width / 2)
        y = centre_pos[1] - height
    elif direction == 62:  # Facing Down
        width = 50
        height = 100
        x = centre_pos[0] - (width / 2)
        y = centre_pos[1]
    elif direction == 63:  # facing right
        width = 100
        height = 50
        x = centre_pos[0]
        y = centre_pos[1] - (height / 2)
    elif direction == 64:  # facing left
        width = 100
        height = 50
        x = centre_pos[0] - width
        y = centre_pos[1] - (height / 2)

    detarea = EnemyVision(x, y, width, height,centre_pos,direction)
    enemy_vision_group.add(detarea)
    #all_sprites_group.add(detarea)     #to draw it behind the enemy


###--------------------------------------------Text Boxes/Text Creator Functions----------------------------------###       //global variables are not needed I kept them in as I didn't want to change them in case it affected some other aspect
    
def leveltext_creator(num): #creates the title of the level given the index of the level, and displays on the level screen
    global leveltext
    global leveltextRect
    leveltext = bigfont.render('LEVEL ' + str(num), True, PURPLE)
    leveltextRect = leveltext.get_rect()
    leveltextRect.center = (1140, 60)


def pause_menu_title():     #creates and displays on the window the title of the pause menu when the pause menu is active
    pausetext = bigfont.render('Pause Menu', True, BLUE)
    pausetextRect = pausetext.get_rect()
    pausetextRect.center = (640, 200)
    return screen.blit(pausetext, pausetextRect)


def level_menu_title(): #diplays title of level menu
    leveltitle = bigfont.render('Level Menu', True, BLUE)
    leveltitleRect = leveltitle.get_rect()
    leveltitleRect.center = (640, 200)
    return screen.blit(leveltitle, leveltitleRect)


def key_col_text():  # text to display when key is collected
    # global keytext
    # global keytextRect
    keytext = font.render('Key Collected', True, YELLOW)
    keytextRect = keytext.get_rect()
    keytextRect.center = (1140, 550)
    return screen.blit(keytext, keytextRect)


def no_key_text():  # text to display when the key is not
    # collected but the user tries to leave through the door
    global nokeytext
    global nokeytextRect
    nokeytext = font.render('Key was not collected', True, RED)
    nokeytextRect = nokeytext.get_rect()
    nokeytextRect.center = (1140, 550)
    return screen.blit(nokeytext, nokeytextRect)


def level_complete_text():  #prompts the user when a level is completed
    global comptext
    global comptextRect
    comptext = bigfont.render('Level Completed!', True, GREEN)
    comptextRect = comptext.get_rect()
    comptextRect.center = (640, 300)
    return screen.blit(comptext, comptextRect)


def level_failed_text():#prompts the user when a level is failed
    global failedtext
    global failedtextRect
    failedtext = bigfont.render('Level Failed!', True, RED)
    failedtextRect = failedtext.get_rect()
    failedtextRect.center = (640, 300)
    return screen.blit(failedtext, failedtextRect)

def boolean_check():        #testign fucntion used to print all screen variables to see what screen is actually running.
    print("game_over = ",game_over)
    print("play_game = ",play_game)
    print("end_level = ",end_level)
    print("pause_menu = ",pause_menu)
    print("level_failed = ",level_failed)
    print("level_running = ",level_running)



##---------------------------------------------------------------------Sprite groups and Sprite Initiation---------------------------------------------------------------------##
all_sprites_group = pygame.sprite.Group()

player_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

enemy_vision_group = pygame.sprite.Group()

enemyobs_group = pygame.sprite.Group()

obstacle_group = pygame.sprite.Group()

key_group = pygame.sprite.Group()

exit_group = pygame.sprite.Group()

background_group = pygame.sprite.Group()

##  --  Button/Cursor Sprites and Groups --  ##         /button class is removed form the game
##cursor_group = pygame.sprite.Group()
##cursor = Cursor(WHITE, 500, 500)
##cursor_group.add(cursor)


##button_group = pygame.sprite.Group()
##button_group.add(playbutton)

##cursorbutton_hit_group = pygame.sprite.Group()

##---------------------------------------------------------------------Variables---------------------------------------------------------------------##
###--------screen Boolean variables-------##
game_over = False
play_game = False
end_level = False
pause_menu = False
level_failed = False
level_running = False

### ----------data relating to the level menu and the level buttons===========#
level_buttons = []
level_x_places = [190, 390, 590, 790, 990, 190, 390, 590, 790, 990]
level_y_places = [250, 250, 250, 250, 250, 460, 460, 460, 460, 460]
level_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
level_colour_data = [[ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW],
                     [ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW], [ORANGE, YELLOW]]

### -----------------------------------------------------------------Constant Buttons-------------------------------------------------------------------------------### //button locations are predetermines but theyh are only active/clickable when certain screen boolean variables are active.
playbutton = Button(RED, 540, 150, 200, 100, PLAYfont, 'PLAY')
for counter in range(0, 10):
    level_button = Button(level_colour_data[counter][0], level_x_places[counter], level_y_places[counter], 100, 100,
                          PLAYfont, level_numbers[counter])
    level_buttons.append(level_button)

pause_button = Button(BLUE, 1040, 580, 200, 100, bigfont, 'PAUSE')
pmenu_button = Button(ORANGE, 540, 250, 200, 50, font, 'MENU')
plevel_button = Button(ORANGE, 540, 350, 200, 50, font, 'LEVELS')
pquit_button = Button(RED, 540, 450, 200, 50, bigfont, 'QUIT')

endlevel_button = Button(ORANGE, 440, 350, 400, 50, bigfont, 'Return to Menu')

level_failed_button = Button(RED, 440, 350, 400, 50, bigfont, 'Restart')

#--------backgrounds are initiated with the menu background, willl change later depending ont he level that is running.
Background = Background('graphics/Backgrounds/MenuBackground.png')
background_group.add(Background)

# -- current_level //used later to determine which level is running

##                                                                                       _________
##______________________________________________________________________________________/GAME LOOP\_____________________________________________________________________________________________________##
while not game_over:

    for event in pygame.event.get():        #gets the posiiton of the mouse what will be later used to check with button objects
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            game_over = True
        elif level_running and len(player_group) > 0:   #only checked when there are active players in the game or when a level is runnin as it will cause an error otherwise, because player object wouldnt exist.
            ####=======================================key press logic to determine how the player object should move======================####
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.go_up()
                elif event.key == pygame.K_s:
                    player.go_down()
                elif event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_a:
                    player.go_left()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.stop_y()
                elif event.key == pygame.K_s:
                    player.stop_y()
                elif event.key == pygame.K_d:
                    player.stop_x()
                elif event.key == pygame.K_a:
                    player.stop_x()

        # If the mouse is clicked over a button the actions are done.
        if event.type == pygame.MOUSEBUTTONDOWN:                    #if the mouse is clicked and it is over a certain button, various functions will be run to display other menus or switch screens etc.
            if pause_button.isOver(mouse_pos):      #isOver funtion is checked with every available button.
                print("pause button clicked")

                # This alternates the use of the pause menu, (if in the pause menu clicking the pause button takes you out of the pause menu)
                if pause_menu:
                    pause_menu = False
                    pause_button.set_text("PAUSE")
                else:
                    pause_menu = True
                    pause_button.set_text("RESUME")

            if pause_menu and pmenu_button.isOver(mouse_pos):   #there are additional boolean conditions here so that buttons are not always clickable.
                print("pmenu is clicked")
                level_running = False
                level_clear()
                play_game = False
                pause_menu = False
                pause_button.set_text("PAUSE")

            if pause_menu and plevel_button.isOver(mouse_pos):  # checks if we are in pause menu and if the levels button is clicked
                print("plevel is clicked")
                level_clear()
                level_running = False

                play_game = True
                pause_menu = False
                pause_button.set_text("PAUSE")

            if pause_menu and pquit_button.isOver(mouse_pos):  # checks if we are in pause menu and if 'QUIT' is pressed
                print("pquit is clicked")
                game_over = True

            if end_level and endlevel_button.isOver(mouse_pos):  # checks if return to menu has been clicked
                print('return to menu is clicked')

                level_running = False
                play_game = True
                end_level = False
            if level_failed and level_failed_button.isOver(mouse_pos):
                print('restart level is clicked, after level failure')

                level_failed = False
                level_selector(current_level)

        # checks if the PLAY button is clicked and creates the level buttons

        if not (pause_menu) and not (play_game) and not level_running and event.type == pygame.MOUSEBUTTONDOWN:
            if playbutton.isOver(mouse_pos):
                print("play button clicked")
                play_game = True

        # All the colour changes for any button done here
        if event.type == pygame.MOUSEMOTION:    #this is the logic sequence that changes the colour of the buttons that indicate clickability, this is not done under MOUSECLICK, becuase clicking causes the button to execute its fucntion
                                                #hovering causes user-friendly interactions to popup
            # Play
            if not play_game and playbutton.isOver(mouse_pos):
                playbutton.colour = GREEN
            else:
                playbutton.colour = RED
            # Pause
            if pause_button.isOver(mouse_pos):
                pause_button.colour = GREEN
            else:
                pause_button.colour = BLUE
            # Pause menu
            if pause_menu and pmenu_button.isOver(mouse_pos):
                pmenu_button.colour = YELLOW
            else:
                pmenu_button.colour = ORANGE
            # End of level menu button
            if end_level and endlevel_button.isOver(mouse_pos):
                endlevel_button.colour = YELLOW
            else:
                endlevel_button.colour = ORANGE
            # Pause Level
            if pause_menu and plevel_button.isOver(mouse_pos):
                plevel_button.colour = YELLOW
            else:
                plevel_button.colour = ORANGE
            # Pause Quit
            if pause_menu and pquit_button.isOver(mouse_pos):
                pquit_button.colour = PINK
            else:
                pquit_button.colour = RED
            if level_failed and level_failed_button.isOver(mouse_pos):
                level_failed_button.colour = GREEN
            else:
                level_failed_button.colour = RED

            #The level Buttons withinthe Level Menu exist as a list of objects, hence all their displaying and colour chagning logic is done in a for loop
                #previous functions regarding colour change are useful here.
            for counter in range(0, 10):
                if play_game and level_buttons[counter].isOver(mouse_pos):

                    set_level_colour(counter,level_colour_data[counter][1])  # -calls procedure to change button hover colour

                elif play_game:
                    set_level_colour(counter,level_colour_data[counter][0])  # -calls procedure that can revert the colour

        #this is the level initiator, gets the index of the clicked level button and launches the correct level using the level_selector procedure
        if play_game and not (pause_menu) and not end_level and event.type == pygame.MOUSEBUTTONDOWN:  # checks if a level is clicked
            for counter in range(0, 10):
                if level_buttons[counter].isOver(mouse_pos):
                    current_level = level_numbers[counter]
                    print(current_level, 'clicked')
                    level_running = True
                    level_selector(current_level)

    screen.fill(BLACK)
    ##    cursor_group.update()
    ##    cursor_group.draw(screen)

#----------------------menu displays ----------------------------------####
    #// this is all the logic that determines what needs to be present on the screen.
    # Pause Menu
    pause_button.draw(screen)       #pause butotn is always ont he screen, so no condition
    if pause_menu:              #ther buttons and level object require certain conditions such as the pause menu button need the pause menu to be running
        background_group.draw(screen)   #menu background is loaded into pause menu to give the illusion of overlay
        if level_running:
            enemy_vision_group.draw(screen)
            all_sprites_group.draw(screen)
            pause_button.draw(screen)               
            try:
                screen.blit(leveltext, leveltextRect)
            except:
                NameError
        
        pause_menu_title()
        pmenu_button.draw(screen)
        plevel_button.draw(screen)
        pquit_button.draw(screen)



    if not level_running and not pause_menu:  # -whether a level is running
        if not play_game and not end_level:  # -nothing runnnig displays title screen
            Background.update_image('graphics/Backgrounds/MenuBackground.png')  #menu background is loaded as no level is running
            background_group.draw(screen)
            playbutton.draw(screen)     #correct buttons are drawn onto depending on the current menu
            pause_button.draw(screen)
        if play_game:  # -play pressed into level screen
            Background.update_image('graphics/Backgrounds/MenuBackground.png')
            background_group.draw(screen)
            pause_button.draw(screen)
            level_menu_title()
            for counter in range(0, 10):
                level_buttons[counter].draw(screen)


    elif level_running and not pause_menu:          #level is active and not paused
        play_game = False
        # writes the level on the screen
        background_group.draw(screen)
        pause_button.draw(screen)
        try:
            screen.blit(leveltext, leveltextRect)
            # checks whether the key has been collected to finish the level         #this is the level completion logic where it constantly checks properties of the player object for seeing key collection and exit collision
            if player.get_colenemy_state() == True:
                level_failed = True
            for item in exit_group:
                if item.get_state() == 1:
                    player.set_key_state()          #player properties are updated to show that it has collected the key
                    key_col_text()                  #key collection is indicated to the player/user
                    item.change_colour(GREEN)       #colour of the exit is changed to indicate unlock
                    exit_hit_group = pygame.sprite.groupcollide(player_group, exit_group, False, False)     #indicates successful exit attempt after key is collected
                    for elem in exit_hit_group:     
                        level_clear()
                        end_level = True    
                        print('Level Completed')

        except:
            NameError                           #prperties of an active level, all dynamic objects are updated, so their flipbook animations can be iterated through if the level i not finished
        enemy_vision_group.draw(screen)
        all_sprites_group.draw(screen)
        player_group.update()
        enemy_group.update()
        enemy_vision_group.update()


        if level_failed:                #level failed screen is prompted
            level_failed_text()
            player.set_colenemy_state(False)
            level_clear()
            level_failed_button.draw(screen)

        if end_level:           #level ends in completion whent he 
            Background.update_image('graphics/Backgrounds/MenuBackground.png')
            play_game = False
            endlevel_button.draw(screen)
            level_complete_text()
            level_complete(current_level)
            level_clear()  # clears the all sprites group

    

    # -- flip display to draw the buttons on the screen

    pygame.display.flip()

    # - The clock ticks over
    clock.tick(60)

# End While - End of game loop -- game ends

pygame.quit()
