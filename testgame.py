import pygame
from spritesheet import Spritesheet

################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
###########################################################################################

my_spritesheet = Spritesheet('graphics/spritesheet.png')
charup = [my_spritesheet.parse_sprite('charup1.png'), my_spritesheet.parse_sprite('charup2.png'),my_spritesheet.parse_sprite('charup3.png'),
           my_spritesheet.parse_sprite('charup4.png')]
enemy3right = [my_spritesheet.parse_sprite('enemy3right1.png'), my_spritesheet.parse_sprite('enemy3right2.png'),my_spritesheet.parse_sprite('enemy3right3.png'),
           my_spritesheet.parse_sprite('enemy3right4.png')]
index = 0

while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            if event.key == pygame.K_SPACE:
                index = (index + 1) % len(charup)


    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((255,255,255))
    canvas.blit(charup[index], (0, DISPLAY_H - 128))
    canvas.blit(enemy3right[index], (128, DISPLAY_H - 128))
    window.blit(canvas, (0,0))
    pygame.display.update()