import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        
class Water(Generic):
    def __init__(self, pos, frames, groups) -> None:
        self.frames = frames
        self.frame_idx = 0
        
        super().__init__(
            pos = pos, 
            surf = self.frames[self.frame_idx], 
            groups = groups, 
            z = LAYERS['water'])
    
    def animate(self, dt):
        self.frame_idx += 5 * dt
        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0
        
        self.image = self.frames[int(self.frame_idx)]
    
    def update(self, dt) -> None:
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)

class Tree(Generic):
    def __init__(self, pos, surf, groups, name) -> None:
        super().__init__(pos, surf, groups)