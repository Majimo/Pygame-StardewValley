import pygame
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import Generic, Tree, Water, WildFlower
from support import *
from overlay import Overlay

class Level:
    def __init__(self) -> None:
        self.display_surf = pygame.display.get_surface()
        
        # Sprites
        self.all_sprites = CameraGroup()
        
        self.setup()
        self.overlay = Overlay(self.player)
    
    def run(self, dt):
        self.display_surf.fill('black')
        # self.all_sprites.draw(self.display_surf)
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()
    
    def setup(self):        
        # Ground
        Generic(
                pos = (0,0),
                surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['ground'])
        
        tmx_data = load_pygame('data/map.tmx')
        
        # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x,y,surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites)
                
        # Fence
        for x,y,surf in tmx_data.get_layer_by_name('Fence').tiles():
                Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites)
                
        # Water
        water_frames = import_folder('graphics/water')
        for x,y,surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x*TITLE_SIZE, y*TITLE_SIZE), water_frames, self.all_sprites)
        
        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, self.all_sprites, obj.name)
        
        # Wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, self.all_sprites)
                
        # Player
        self.player = Player((640,360), self.all_sprites)
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - (SCREEN_WIDTH / 2)
        self.offset.y = player.rect.centery - (SCREEN_HEIGHT / 2)
         
        for layer in LAYERS.values():     
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surf.blit(sprite.image, offset_rect)