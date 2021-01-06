import pygame
import random
import math
import json

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (46,204,113)
ORANGE = (211,84,0)
PURPLE = (125,60,152)
AQUA = (22,160,133)
PINK = (255,89,222)
BROWN = (165,42,42)
CHOCOLATE = (210,105,30)
GREY =(128,128,128)
COLOUR = [WHITE,BLUE,YELLOW,RED,GREEN,ORANGE,PURPLE,
          AQUA,PINK,BROWN,CHOCOLATE,GREY]

# -- Initialise PyGame
pygame.init()

# -- Font
PLAYfont = pygame.font.SysFont('comicsans', 60)
font = pygame.font.Font('freesansbold.ttf',20)
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
## ---------------------------------------------------------------------Classes-----------------------------------------------------------------------##
class Player(pygame.sprite.Sprite):
    def __init__(self,colour,x,y):
        super().__init__()
        self.keycollected = False
        self.colenemy = False   #Boolean variable to hold whether the player has collided with any enemies
        self.speed = 10
        self.direction_x =0
        self.direction_y =0
        self.colour = colour
        self.image = pygame.Surface([20,20])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y


    def get_key_state(self):
        return self.keycollected
    def set_key_state(self):
        self.keycollected =True
    def get_colenemy_state(self):
        return self.colenemy
    def set_colenemy_state(self, state):
        self.colenemy = state

        
    #player movement methods
    def go_up(self):
        self.direction_y = self.speed*-1
    def go_down(self):
        self.direction_y = self.speed
    def go_right(self):
        self.direction_x = self.speed
    def go_left(self):
        self.direction_x =self.speed*-1
    def stop_x(self):
        self.direction_x = 0
    def stop_y(self):
        self.direction_y = 0
    
    def update(self):
        #------Level border collision logic and movement
        if (self.rect.x>=0 and self.rect.x<=980) and (self.rect.y >=0 and self.rect.y<=700):
            self.rect.x += self.direction_x
            self.rect.y += self.direction_y
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x >980:
            self.rect.x = 980
        if self.rect.y <0:
            self.rect.y =0
        if self.rect.y > 700:
            self.rect.y =700
        #-------Obstacle collision Logic
        
        obstacle_hit_group = pygame.sprite.groupcollide(player_group,obstacle_group,False,False)
        for player in obstacle_hit_group:
            self.rect.x-= self.direction_x
            self.rect.y -=self.direction_y


        # ------ Exit closed check
        exit_hit_group = pygame.sprite.groupcollide(player_group, exit_group, False, False)
        for elem in exit_hit_group:
            if not self.get_key_state():
                no_key_text()
                
        # ------- Enemy object collision
        enemybody_hit_group = pygame.sprite.groupcollide(player_group, enemy_group, False, False)
        for elem in enemybody_hit_group:
            print('collided with enemy')
            self.colenemy = True
            
        # ------Key Collection Logic (opens the gate)
        key_hit_group = pygame.sprite.groupcollide(player_group,key_group,False,True)
        for elem in key_hit_group:
            for item in exit_group:
                print('key collected')
                item.state_change(1)
                self.key_collected = True
                
        # -> additional logic of collection indicator in the info menu can be added
            #---Wirtten later in the code where the text displaying logic is
        
        # -> Logic for finishing a level after the key is collected
            # --- Also added later on in the code, using a text function.

                
                
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, facing):
        super().__init__()
        
        self.facing = facing
        self.direction_x = 0
        self.direction_y = 0   #-1 in y is UP!

                    
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #all instances of enemies face different sides at the start
        if self.facing ==61:   #Facing up
            self.direction_y = -1
        elif self.facing ==62: #Facing Down
            self.direction_y = 1
        elif self.facing == 63: #facing right
            self.direction_x = 1
        elif self.facing ==64:  #facing left
            self.direction_x = -1







                # --------------------------------------Useless E3 movement logic using try-except clause with exception classes
                
##            for elem in enemyobs_hit_group:
##                self.rect.x -= self.speed*self.direction_x
##                self.rect.y -=self.speed*self.direction_y
##
##                if self.direction_x ==0:
##                    self.direction_y = 0
##                    try:
##                        self.direction_x = 1
##                        enemyobs_hit_group= pygame.sprite.spritecollide(self, enemyobs_group, False)
##                        if len(enemyobs_hit_group)>0:
##                            raise WrongDirectionError_x
##                    except WrongDirectionError_x:
##                        self.direction_x = -1
##                        
##                elif self.direction_y == 0:
##                    self.direction_x = 0
##                    try:
##                        self.direction_y = 1
##                        enemyobs_hit_group = pygame.sprite.spritecollide(self,enemyobs_group,False)
##                        if len(enemyobs_hit_group)>0:
##                            raise WrongDirectionError_y
##                    except WrongDirectionError_y:
##                        self.direction_y = -1
##                 
##               elif self.direction_x ==1 and self.direction_y ==0:
##                    self.direction_y = 0
##                    try:
##                        self.direction_x = 1
##                        enemyobs_hit_group= pygame.sprite.spritecollide(self, enemyobs_group, False)
##                        if len(enemyobs_hit_group)>0:
##                            raise WrongDirectionError_x
##                    except WrongDirectionError_x:
##                        self.direction_x = -1
##                        
##                elif self.direction_y == 0:
##                    self.direction_x = 0
##                    try:
##                        self.direction_y = 1
##                        enemyobs_hit_group = pygame.sprite.spritecollide(self,enemyobs_group,False)
##                        if len(enemyobs_hit_group)>0:
##                            raise WrongDirectionError_y
##                    except WrongDirectionError_y:
##                        self.direction_y = -1
                        
        
##            for item in enemyobs_group:
##                print(item)
##                print(item.get_direction_y)
##                if pygame.sprite.collide_rect(self, item):
##                    
##                    if int(item.get_direction_y) !=0:
##                        self.direction_y = int(item.get_direction_y)
##                    elif int(item.get_direction_x) != 0:
##                        self.direction_x = int(item.get_direction_x)
                        
                    
                
                
##                if enemyobs_hit_group[0].get_direction_y != 0:
##                    self.direction_y = int(enemyobs_hit_group[0].get_direction_y)
##                elif enemyobs_hit_group[0].get_direction_x != 0:
##                    self.direction_x = int(enemyobs_hit_group[0].get_direction_x)


#sub classes of enemies are the different types of enemies
            
class Enemy1(Enemy):
    def __init__(self, x, y, facing):
        self.speed = 0
        self.colour = RED
        super().__init__(x, y, facing)
        

class Enemy2(Enemy):
    def __init__(self, x, y, facing):
        self.speed = 0
        self.colour = PINK
        super().__init__(x, y, facing)
        

class Enemy3(Enemy):
    def __init__(self, x, y, facing):
        self.speed = 2                           #!!!!!!!!!!!!! speed = 1 when movement is needed
        self.colour = ORANGE
        super().__init__(x, y, facing)
        
    def update(self):
        if self.direction_x != 0:
            self.rect.x += self.direction_x*self.speed
        if self.direction_y != 0:
            self.rect.y += self.direction_y*self.speed
            
        enemyobs_hit_group = pygame.sprite.spritecollide(self, enemyobs_group, False)
        
        for elem in enemyobs_hit_group:
            self.rect.x -= self.speed*self.direction_x
            self.rect.y -=self.speed*self.direction_y
            self.direction_x = elem.get_direction_x()
            self.direction_y = elem.get_direction_y()
    
        
        

        
class EnemyObstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,facing):
        super().__init__()
        self.facing = facing
        self.direction_y = 0
        self.direction_x = 0
        self.colour = PURPLE    #purple is the original colour
                                #the blocks with rotation have white colour
        if self.facing ==91:        #UP
            self.direction_y =-1
            self.colour = WHITE
        elif self.facing ==92:      #DOWN
            self.direction_y = 1
            self.colour = WHITE
        elif self.facing == 93:     #RIGHT
            self.direction_x = 1
            self.colour = WHITE
        elif self.facing == 94:     #LEFT
            self.direction_x = -1
            self.colour = WHITE
        
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def get_direction_x(self):
        return self.direction_x
    
    def get_direction_y(self):
        return self.direction_y
        

        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.colour = AQUA
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                                    
        
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.graphic = KeyImage
        self.colour = YELLOW
        self.width = 24
        self.height = 12
        self.image = pygame.transform.scale(self.graphic,(self.width, self.height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
                 
class Exit(pygame.sprite.Sprite):
    def __init__(self,x, y, w, h):
        super().__init__()
        self.colour = RED
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0    #exit closed by default

    def get_state(self):
        return self.state
        
    def change_colour(self,colour):
        self.colour = colour
        self.image.fill(self.colour)
        
    def state_change(self,state):
        self.state = int(state)
        #state = 0 -> exit is closed
        #state = 1 -> exit is open
        

        
class Button():
    def __init__(self, colour, x,  y,width,height,font, text=''):
        self.colour = colour
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        
    def set_text(self,value):
        self.text = value

    def draw(self,screen,outline=None):
        #Method to draw the button and its text onto the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.colour, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            
            text = self.font.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    
    ##class Cursor(pygame.sprite.Sprite):
##    def __init__(self, colour, x, y):
##        super().__init__()
##        self.colour = colour
##        self.image= pygame.Surface([6,6])
##        self.image.fill(self.colour)
##        self.rect = self.image.get_rect()
##        self.rect.x = x -2
##        self.rect.y = y -2
##
##    def update(self):
##        mouse_pos = pygame.mouse.get_pos()
##        self.rect.x = mouse_pos[0] -2
##        self.rect.y = mouse_pos[1] -2
##
##        #cursorbutton_hit_group = pygame.sprite.groupcollide(cursor_group, button_group,False, False)
##

    ##-------------Error class and subclasses I am going to be using in a try clause to guess the new available square for the Enemy3s to move

class MovementError(Exception):
    pass
class WrongDirectionError_x(MovementError):
    pass
class WrongDirectionError_y(MovementError):
    pass
    

    
##---------------------------------------------------------------------Functions/Procedures---------------------------------------------------------------------##
    
            
def set_level_colour(num, colour):
    level_buttons[num].colour = colour
def reset_level_colour(num, colour):
    level_buttons[num].colour = colour
        
def level_selector(num):
    num = int(num)
    if num == 1:
        level_1(num)
    if num == 2:
        level_2(num)
    if num == 3:
        level_3(num)
    if num ==4:
        level_4(num)
    if num ==5:
        level_5(num)
    if num ==6:
        level_6(num)
    if num ==7:
        level_7(num)
    if num ==8:
        level_8(num)
    if num ==9:
        level_9(num)
    if num ==10:
        level_l0(num)
        
def level_clear():                  #clears all the sprite groups 
    all_sprites_group.empty()
    obstacle_group.empty()
    player_group.empty()
    enemy_group.empty()
    enemyobs_group.empty()
    key_group.empty()
    exit_group.empty()
    

    
def map_creator(layout):
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            
            if layout[y][x] == 1:
                #places obstacle (followed +2 with width and height)
                create_obstacle(x*10,y*10,int(layout[y][x+1]),int(layout[y][x+2]))
                
            elif layout[y][x] == 2:
                #player spawn
                create_player(x*10,y*10)
                
            elif layout[y][x] == 3:
                #places exit (+2 for w and h)
                create_exit(x*10,y*10,int(layout[y][x+1]),int(layout[y][x+2]))
                
            elif layout[y][x] == 4:
                #places key
                create_key(x*10,y*10)
                
##            if layout[y][x] == 5:
##                # 5 IS NOT DEFINED IN THE MAP CREATION KEY
                
            elif layout[y][x] == 6:           #--- *1 = up, *2 = down, *3= right, *4 = left ---#
                #enemy type 1 (followed by +1 orientation)

                create_enemy(x*10,y*10,1, int(layout[y][x+1]))
                
            elif layout[y][x] == 7:
                #enemy type 2 (followed by +1 orientation)
                create_enemy(x*10,y*10,2,int(layout[y][x+1]))
                
            elif layout[y][x] == 8:
                #enemy type 3 (+1 orientation)
                create_enemy(x*10,y*10,3,int(layout[y][x+1]))
                
            elif layout[y][x] == 9 :
                #enemy obstacle (+1 rotation)
                if int(layout[y][x+1]) != 0:                    #<---- REMOVE this line to get back the default enemy obstacles.
                    create_enemyobstacle(x*10,y*10,int(layout[y][x+1]))


def level_complete(level):
    level = int(level) - 1
    level_colour_data[level] = [GREEN, AQUA]


###------------------------------------Level Creation Functions---------------------------------###
def level_1(num):
    print('level 1 - Test Level')
    leveltext_creator(num)
    create_player(300,500)
    create_obstacle(100, 100, 100, 200)
    create_key(300,300)
    create_exit(500,0,200,50)
    create_enemy(400, 400,1,61)
    create_enemy(500, 500,2,61)
    create_enemy(600, 600,3,61)
    create_enemyobstacle(600,300,92) #has direction direction
    create_enemyobstacle(700,300,0) #normal enemyobstacle object

    
def level_2(num):
    leveltext_creator(num)
    print('level 2')




    
def level_3(num):
    leveltext_creator(num)
    print('level 3')
    level_file = open('levels/level3.json','rt')
    layout = json.load(level_file)
    level_file.close()
    map_creator(layout)



    
def level_4(num):
    leveltext_creator(num)
    print('level 4')


    
def level_5(num):
    leveltext_creator(num)
    print('level 5')


    
def level_6(num):
    leveltext_creator(num)
    print('level 6')


    
def level_7(num):
    leveltext_creator(num)
    print('level 7')


    
def level_8(num):
    leveltext_creator(num)
    print('level 8')


    
def level_9(num):
    leveltext_creator(num)
    print('level 9')


    
def level_10(num):
    leveltext_creator(num)
    print("level 10")

    







                
###----------------------- Sprite Creation -----------------------------###
def create_player(x,y):
    global player
    player_group.empty()    # -- there can only be 1 player at one time!
    player = Player(BLUE,x,y)
    player_group.add(player)
    all_sprites_group.add(player)
    
def create_obstacle(x,y,w,h):
    global obstacle
    obstacle = Obstacle(x,y,w,h)
    obstacle_group.add(obstacle)
    all_sprites_group.add(obstacle)

def create_exit(x,y,w,h):
    global exit_
    exitblock = Exit(x,y,w,h)
    exit_group.add(exitblock)
    all_sprites_group.add(exitblock)

def create_key(x,y):
    global key
    key = Key(x,y)
    key_group.add(key)
    all_sprites_group.add(key)

def create_enemy(x,y,e_type,facing):
    global enemy
    
    if e_type == 1:
        enemy = Enemy1(x,y,facing)
    elif e_type == 2:
        enemy = Enemy2(x,y,facing)
    elif e_type == 3:
        enemy = Enemy3(x,y,facing)
        
    enemy_group.add(enemy)
    all_sprites_group.add(enemy)
        
def create_enemyobstacle(x,y,facing):
    global enemy_obs
    enemy_obs = EnemyObstacle(x,y,facing)
    enemyobs_group.add(enemy_obs)
    all_sprites_group.add(enemy_obs)    #----!!!!!line should be hashed so that the enemyobs are not visible to the user
    



    
###--------------------------------------------Text Boxes/Text Creator Functions----------------------------------###
def leveltext_creator(num):
    global leveltext
    global leveltextRect
    leveltext = bigfont.render('LEVEL '+ str(num),True, PURPLE)
    leveltextRect = leveltext.get_rect()
    leveltextRect.center = (1150,50)
    
def pause_menu_title():
    pausetext = bigfont.render('Pause Menu',True, BLUE)
    pausetextRect = pausetext.get_rect()
    pausetextRect.center = (640,200)
    return screen.blit(pausetext, pausetextRect)

def level_menu_title():
    leveltitle = bigfont.render('Level Menu',True,BLUE)
    leveltitleRect = leveltitle.get_rect()
    leveltitleRect.center = (640,200)
    return screen.blit(leveltitle,leveltitleRect)

def key_col_text():     #text to display when key is collected
    #global keytext
    #global keytextRect
    keytext = font.render('Key Collected',True, YELLOW)
    keytextRect = keytext.get_rect()
    keytextRect.center = (1150,550)
    return screen.blit(keytext, keytextRect)

def no_key_text():      #text to display when the key is not
                        #collected but the user tries to leave through the door
    global nokeytext
    global nokeytextRect
    nokeytext = font.render('Key was not collected', True, RED)
    nokeytextRect = nokeytext.get_rect()
    nokeytextRect.center = (1150,550)
    return screen.blit(nokeytext,nokeytextRect)

def level_complete_text():
    global comptext
    global comptextRect
    comptext = bigfont.render('Level Completed!',True,GREEN)
    comptextRect = comptext.get_rect()
    comptextRect.center = (640,300)
    return screen.blit(comptext, comptextRect)


def level_failed_text():
    global failedtext
    global failedtextRect
    failedtext = bigfont.render('Level Failed!', True, RED)
    failedtextRect = failedtext.get_rect()
    failedtextRect.center = (640, 300)
    return screen.blit(failedtext, failedtextRect)
    

        
    
##---------------------------------------------------------------------Sprite groups and Sprite Initiation---------------------------------------------------------------------##
all_sprites_group = pygame.sprite.Group()

player_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

enemyobs_group = pygame.sprite.Group()

obstacle_group = pygame.sprite.Group()

key_group = pygame.sprite.Group()

exit_group = pygame.sprite.Group()



    
##  --  Button/Cursor Sprites and Groups --  ##
##cursor_group = pygame.sprite.Group()
##cursor = Cursor(WHITE, 500, 500)
##cursor_group.add(cursor)
    

##button_group = pygame.sprite.Group()
##button_group.add(playbutton)

##cursorbutton_hit_group = pygame.sprite.Group()

##---------------------------------------------------------------------Variables---------------------------------------------------------------------##
game_over = False
play_game = False
end_level = False
pause_menu = False
level_failed = False
level_running = False

level_buttons = []
level_x_places=[190,390,590,790,990,190,390,590,790,990]
level_y_places=[250,250,250,250,250,460,460,460,460,460]
level_numbers = ['1','2','3','4','5','6','7','8','9','10']
level_colour_data = [[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW],[ORANGE, YELLOW]]




### -----------------------------------------------------------------Constant Buttons-------------------------------------------------------------------------------###
playbutton = Button(RED, 540,150,200,100,PLAYfont,'PLAY')
for counter in range(0,10):
    level_button = Button(level_colour_data[counter][0],level_x_places[counter], level_y_places[counter],100,100,PLAYfont,level_numbers[counter])
    level_buttons.append(level_button)

pause_button = Button(BLUE,1060,600,200,100,bigfont,'PAUSE')
pmenu_button = Button(ORANGE, 540, 250, 200, 50, font, 'MENU')
plevel_button = Button(ORANGE,540,350, 200,50,font,'LEVELS')
pquit_button = Button(RED, 540, 450, 200, 50, bigfont, 'QUIT')

endlevel_button = Button(ORANGE, 440, 350, 400, 50, bigfont, 'Return to Menu')

level_failed_button = Button(RED, 440, 350, 400, 50, bigfont, 'Restart')

# -- current_level //used later to determine which level is running

##                                                                                       _________             
##______________________________________________________________________________________/GAME LOOP\_____________________________________________________________________________________________________##
while not game_over:
    
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            game_over = True
        elif level_running and len(player_group)>0:
            if event.type ==pygame.KEYDOWN:
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.isOver(mouse_pos):
                print("pause button clicked")

                # This alternates the use of the pause menu, (if in the pause menu clicking the pause button takes you out of the pause menu)
                if pause_menu:
                    pause_menu = False
                    pause_button.set_text("PAUSE")
                else:
                    pause_menu = True
                    pause_button.set_text("RESUME")
                    
            if pause_menu and pmenu_button.isOver(mouse_pos):
                
                print("pmenu is clicked")
                level_running = False
                level_clear()
                play_game = False
                pause_menu = False
                pause_button.set_text("PAUSE")
                
            if pause_menu and plevel_button.isOver(mouse_pos):     #checks if we are in pause menu and if the levels button is clicked
                print("plevel is clicked")
                level_clear()
                level_running = False
                
                play_game = True
                pause_menu = False
                pause_button.set_text("PAUSE")
            
            if pause_menu and pquit_button.isOver(mouse_pos):       #checks if we are in pause menu and if 'QUIT' is pressed
                print("pquit is clicked")
                game_over  = True
                
            if end_level and endlevel_button.isOver(mouse_pos):             #checks if return to menu has been clicked
                print('return to menu is clicked')
                
                level_running = False
                play_game = True
                end_level = False
            if level_failed and level_failed_button.isOver(mouse_pos):
                print('restart level is clicked, after level failure')

                level_failed = False
                level_selector(current_level)
                
        #checks if the PLAY button is clicked and creates the level buttons
            
        if not(pause_menu) and not(play_game) and not level_running and event.type == pygame.MOUSEBUTTONDOWN:
            if playbutton.isOver(mouse_pos):
                print("play button clicked")
                play_game= True


                    
        # All the colour changes for any button done here             
        if event.type == pygame.MOUSEMOTION:
            # Play 
            if not play_game and playbutton.isOver(mouse_pos):
                playbutton.colour = GREEN
            else:
                playbutton.colour =RED
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

                
            for counter in range(0,10):
                if play_game and level_buttons[counter].isOver(mouse_pos):

                    set_level_colour(counter, level_colour_data[counter][1]) #-calls procedure to change button hover colour
                                        
                elif play_game:
                    set_level_colour(counter, level_colour_data[counter][0]) #-calls procedure that can revert the colour
                    
        if play_game and not(pause_menu) and not end_level and event.type == pygame.MOUSEBUTTONDOWN:  #checks if a level is clicked
            for counter in range(0,10):
                if level_buttons[counter].isOver(mouse_pos):
                    current_level =level_numbers[counter]
                    print(current_level, 'clicked')
                    level_running = True
                    level_selector(current_level)
                    


            
                    
    
     
    
   

    
    screen.fill(BLACK)        
##    cursor_group.update()
##    cursor_group.draw(screen)



    # Pause Menu
    pause_button.draw(screen)
    if pause_menu:
        pause_menu_title()
        pmenu_button.draw(screen)
        plevel_button.draw(screen)
        pquit_button.draw(screen)
            
    if not level_running and not pause_menu:   #-whether a level is running
        if not play_game and not end_level:   #-nothing runnnig displays title screen
            playbutton.draw(screen)
        if play_game:       #-play pressed into level screen
            level_menu_title()
            for counter in range(0,10):
                level_buttons[counter].draw(screen)
    elif level_running and not pause_menu:
        play_game = False
        #writes the level on the screen
        try:
            screen.blit(leveltext,leveltextRect)
        #checks whether the key has been collected to finish the level
            if player.get_colenemy_state() == True:
                level_failed = True
            for item in exit_group:
                if item.get_state() == 1:
                    player.set_key_state()
                    key_col_text()
                    item.change_colour(GREEN)
                    exit_hit_group = pygame.sprite.groupcollide(player_group, exit_group, False, False)
                    for elem in exit_hit_group:
                        level_clear()
                        end_level = True
                        
        except:
           NameError
        all_sprites_group.draw(screen)
        player_group.update()
        enemy_group.update()
        
        if level_failed:
            
            level_failed_text()
            player.set_colenemy_state(False)
            level_clear()
            level_failed_button.draw(screen)
            
        if end_level:
            play_game = False
            endlevel_button.draw(screen)
            level_complete_text()
            level_complete(current_level)
            level_clear()   #clears the all sprites group
        
        
        
        

##---------------------------------------------------------------------Draw here---------------------------------------------------------------------##
            




        
    # -- flip display to draw the buttons on the screen
    
    pygame.display.flip()

    # - The clock ticks over
    clock.tick(60)

#End While - End of game loop

pygame.quit()
