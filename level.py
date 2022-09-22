import imp
from multiprocessing.spawn import import_main_path
import pygame
from player import Player
from settings import *

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        
        self.setup()
    
    def run(self, dt):
        self.display_surf.fill('black')
        self.all_sprites.draw(self.display_surf)
        self.all_sprites.update(dt)
    
    def setup(self):
        self.player = Player((640,360), self.all_sprites)