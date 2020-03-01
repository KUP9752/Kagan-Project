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
COLOUR = [WHITE,BLUE,YELLOW,RED,GREEN,ORANGE,PURPLE,AQUA,PINK]

# -- Initialise PyGame
pygame.init()

# -- Font
PLAYfont = pygame.font.SysFont('comicsans', 60)
font = pygame.font.Font('freesansbold.ttf',20)
bigfont = pygame.font.Font('freesansbold.ttf', 32)

# -- Manages how fast screen refreshes

clock = pygame.time.Clock()


# -- Blank Screen

size = (1000,1000)
screen = pygame.display.set_mode(size)
screen.fill(BLACK)

# -- Title of new window/screen
pygame.display.set_caption("GAME")


## ---------------------------------------------------------------------Classes-----------------------------------------------------------------------##
class Cursor(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super().__init__()
        self.colour = colour
        self.image= pygame.Surface([6,6])
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x -2
        self.rect.y = y -2

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0] -2
        self.rect.y = mouse_pos[1] -2

        #cursorbutton_hit_group = pygame.sprite.groupcollide(cursor_group, button_group,False, False)
        
class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        
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
##---------------------------------------------------------------------Sprite groups and Sprite Initiation---------------------------------------------------------------------##
all_sprites_group = pygame.sprite.Group()

    
##  --  Button/Cursor Sprites and Groups --  ##
cursor_group = pygame.sprite.Group()
cursor = Cursor(WHITE, 500, 500)
cursor_group.add(cursor)
    

playbutton = Button(RED,200,200,200,200,PLAYfont,'PLAY')
##button_group = pygame.sprite.Group()
##button_group.add(playbutton)

##cursorbutton_hit_group = pygame.sprite.Group()

##---------------------------------------------------------------------Variables---------------------------------------------------------------------##
game_over = False

##                                                                                       _________             
##______________________________________________________________________________________/GAME LOOP\_____________________________________________________________________________________________________##
while not game_over:
    
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            game_over = True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playbutton.isOver(mouse_pos):
                print("button clicked")
        if event.type == pygame.MOUSEMOTION:
            if playbutton.isOver(mouse_pos):
                playbutton.colour = GREEN
            else:
                playbutton.colour =RED
    
    screen.fill(BLACK)        
    cursor_group.update()
    cursor_group.draw(screen)
    playbutton.draw(screen)
        

##---------------------------------------------------------------------Draw here---------------------------------------------------------------------##
            
























        
    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - The clock ticks over
    clock.tick(60)

#End While - End of game loop

pygame.quit()
