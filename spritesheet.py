import json
import pygame
import Colours as colour

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sheet = pygame.image.load(self.filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey(colour.BLACK)
        sprite.blit(self.sheet, (0,0),(x, y, width, height))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x = sprite['x']
        y = sprite['y']
        w = sprite['w']
        h = sprite['h']
        image = self.get_sprite(x, y,w, h)
        return image

    def get_width(self, name):
        sprite = self.data['frames'][name]['frame']
        return sprite['w']

    def get_height(self, name):
        sprite = self.data['frames'][name]['frame']
        return sprite['h']