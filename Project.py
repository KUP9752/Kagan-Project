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
COLOUR = [WHITE,BLUE,YELLOW,RED,GREEN,ORANGE,PURPLE,AQUA,PINK,BROWN,CHOCOLATE,GREY]

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


## ---------------------------------------------------------------------Classes-----------------------------------------------------------------------##
class Player(pygame.sprite.Sprite):
    def __init__(self,colour,x,y):
        super().__init__()
        self.speed =10
        self.direction_x =0
        self.direction_y =0
        self.colour = colour
        self.image = pygame.Surface([20,20])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def set_direction_x(self,value):
        self.direction_x = value

    def set_direction_y(self,value):
        self.direction_y = value
        
    def update(self):
        #------Level border collision logic
        if (self.rect.x>=0 and self.rect.x<=980) and (self.rect.y >=0 and self.rect.y<=700):
            self.rect.x = self.rect.x + self.direction_x*self.speed
            self.rect.y = self.rect.y + self.direction_y*self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x >980:
            self.rect.x = 980
        if self.rect.y <0:
            self.rect.y =0
        if self.rect.y > 700:
            self.rect.y =700
        #-------Level border collision logic

        # ------Key Collection Logic (opens the gate)
        key_hit_group = pygame.sprite.groupcollide(player_group,key_group,False,True)
        for elem in key_hit_group:
            for item in exit_group:
                item.state_change(1)
        # -> additional logic of collection indicator in the info menu can be added

        #--------Key Collection Logic (opens the gate)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type, facing):
        super().__init__()
        self.colour = BLUE
        self.type = e_type
        self.facing = facing
        self.direction_x = 0
        self.direction_y = 0   #-1 in y is UP!
        
        if self.facing ==61:   #Facing up
            self.direction_y = -1
        elif self.facing ==62: #Facing Down
            self.direction = 1
        elif self.facing == 63: #facing right
            self.direction_x = 1
        elif self.facing ==64:  #facing left
            self.direction_x = -1
            
        if self.type ==1:
            self.speed = 0
            self.colour = RED
        elif self.type ==2:
            self.speed = 0
            self.colour = PINK
        elif self.type == 3:
            self.speed = 10
            self.colour = ORANGE
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
class EnemyObstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,facing):
        super().__init__()
        self.facing = facing
        self.direction_y = 0
        self.direction_x = 0
        if self.facing ==91:        #UP
            self.direction_y =-1
        elif self.facing ==92:      #DOWN
            self.direction_y = 1
        elif self.facing == 93:     #RIGHT
            self.direction_x = 1
        elif self.facing == 94:     #LEFT
            self.direction_x = -1
        
        self.colour = PURPLE
        self.width = 20
        self.height = 20
        pygame.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect.x = x
        self.rect.y = y

        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.colour = GREEN
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
                                    
        
class Key(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.colour = YELLOW
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
                 
class Exit(pygame.sprite.Sprite):
    def __inti__(self,x, y, w, h):
        super().__init__()
        self.colour = RED
        self.width = w
        self.height = h
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0      #exit closed by default
        
    def state_change(self,state):
        self.state = state
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

    def draw(self,screen,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.colour, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            
            text = PLAYfont.render(self.text, 1, BLACK)
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

    
##---------------------------------------------------------------------Functions/Procedures---------------------------------------------------------------------##
    
            
def set_level_colour(num):
    level_buttons[num].colour = YELLOW
def reset_level_colour(num):
    level_buttons[num].colour = ORANGE
        
def level_selector(num):
    num = int(num)
    if num == 1:
        level_1()
    elif num == 2:
        level_2()
    elif num == 3:
        level_3()
    elif num ==4:
        level_4()
    elif num ==5:
        level_5()
    elif num ==6:
        level_6()
    elif num ==7:
        level_7()
    elif num ==8:
        level_8()
    elif num ==9:
        level_9()
    elif num == 10:
        level_l0()
        
def level_clear():
    all_sprites_group.empty()

def map_creator(layout):
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            if layout[y][x] == 1:
                #places obstacle (followed +2 with width and height)
                obstacle = Obstacle(x*10,y*10,layout[y][x+1],layout[y][x+2])
                obstacle_group.add(obstacle)
                all_sprites_group.add(obstacle)
            elif layout[y][x] == 2:
                #player spawn
                create_player(x*10,y*10)
            elif layout[y][x] == 3:
                #places exit (+2 for w and h)
                exit_ = Exit(x*10,y*10, layout[y][x+1], layout[y][x+2])
                exit_group.add(exit_)
                all_sprites_group.add(exit_)
            elif layout[y][x] == 4:
                #places key
                key = Key(x*10,y*10)
                key_group.add(key)
                all_sprites_group.add(key)
##            if layout[y][x] == 5:
##                # 5 IS NOT DEFINED IN THE MAP CREATION KEY
            elif layout[y][x] == 6:           #--- *1 = up, *2 = down, *3= right, *4 = left ---#
                #enemy type 1 (followed by +1 orientation)
                enemy = Enemy(x*10,y*10,1,layout[y][x+1])
                enemy_group.add(enemy)
                all_sprites_group.add(enemy)
                
            elif layout[y][x] == 7:
                #enemy type 2 (+1 orientation)
                enemy = Enemy(x*10,y*10,2,layout[y][x+1])
                enemy_group.add(enemy)
                all_sprites_group.add(enemy)
                
            elif layout[y][x] == 8:
                #enemy type 3 (+1 orientation)
                enemy = Enemy(x*10,y*10,3,layout[y][x+1])
                enemy_group.add(enemy)
                all_sprites_group.add(enemy)
                
            elif layout[y][x] == 9 :
                #enemy obstacle (+1 rotation)
                enemy_obs = EnemyObstacle(x*10,y*10,layout[y][x+1])
                enemyobs_group.add(enemy_obs)
                all_sprites_group.add(enemy_obs)

                
###----------------------- PLayer Creation -----------------------------###
def create_player(x,y):
    global player
    player_group.empty()    # -- there can only be 1 player at one time!
    player = Player(BLUE,x,y)
    player_group.add(player)
    all_sprites_group.add(player)
    
###---------------------------------------------------------------------###
    
def level_1():
    print('level 1')
    create_player(500,500)

    
def level_2():
    print('level 2')




    
def level_3():
    print('level 3')
    level_file = open('levels/level3.json','rt')
    layout = json.load(level_file)
    level_file.close()
    map_creator(layout)



    
def level_4():
    print('level 4')


    
def level_5():
    print('level 5')


    
def level_6():
    print('level 6')


    
def level_7():
    print('level 7')


    
def level_8():
    print('level 8')


    
def level_9():
    print('level 9')


    
def level_10():
    print('level 10')

    





    
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
    

playbutton = Button(RED, 540,150,200,100,PLAYfont,'PLAY')
##button_group = pygame.sprite.Group()
##button_group.add(playbutton)

##cursorbutton_hit_group = pygame.sprite.Group()

##---------------------------------------------------------------------Variables---------------------------------------------------------------------##
game_over = False
play_game = False

level_buttons = []
level_x_places=[190,390,590,790,990,190,390,590,790,990]
level_y_places=[260,260,260,260,260,460,460,460,460,460]
level_numbers = ['1','2','3','4','5','6','7','8','9','10']
level_running = False

end_level = False

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
                try:
                    if event.key ==pygame.K_w:
                        player.set_direction_y(-1)
                    elif event.key == pygame.K_s:
                        player.set_direction_y(1)
                    elif event.key == pygame.K_d:
                        player.set_direction_x(1)
                    elif event.key == pygame.K_a:
                        player.set_direction_x(-1)
                except:
                    NameError
            elif event.type == pygame.KEYUP:
                try:
                    player.set_direction_x(0)
                    player.set_direction_y(0)
                except:
                    NameError
        if not(play_game) and event.type == pygame.MOUSEBUTTONDOWN:
            if playbutton.isOver(mouse_pos):
                print("button clicked")
                play_game= True
                for counter in range(0,10):
                    level_button = Button(ORANGE,level_x_places[counter], level_y_places[counter],100,100,PLAYfont,level_numbers[counter])
                    level_buttons.append(level_button)
        if event.type == pygame.MOUSEMOTION:
            if playbutton.isOver(mouse_pos):
                playbutton.colour = GREEN
            else:
                playbutton.colour =RED
            for counter in range(0,10):
                if play_game and level_buttons[counter].isOver(mouse_pos):
                    set_level_colour(counter) #-calls procedure to change button hover colour
                elif play_game:
                    reset_level_colour(counter) #-calls procedure that can revert the coour
        if play_game and event.type == pygame.MOUSEBUTTONDOWN:  #checks if a level is clicked
            for counter in range(0,10):
                if level_buttons[counter].isOver(mouse_pos):
                    current_level =level_numbers[counter]
                    print(current_level, 'clicked')
                    level_running = True
                    level_selector(current_level)
                    
        

            
                    
    
     
    
   

    
    screen.fill(BLACK)        
##    cursor_group.update()
##    cursor_group.draw(screen)
    
    if not level_running:   #-whether a level is running
        if not play_game:   #-nothing runnnig displays title screen
            playbutton.draw(screen)
        if play_game:       #-play pressed into level screen
            for counter in range(0,10):
                level_buttons[counter].draw(screen)
    elif level_running:
        
        
        all_sprites_group.draw(screen)
        all_sprites_group.update()
        
        if end_level:
            end_level = False
            level_clear()   #clears the all sprites group
        
        
        
        

##---------------------------------------------------------------------Draw here---------------------------------------------------------------------##
            



        
    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - The clock ticks over
    clock.tick(60)

#End While - End of game loop

pygame.quit()
