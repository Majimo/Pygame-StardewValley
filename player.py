import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group) -> None:
        super().__init__(group)
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_idx = 0
        
        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(center = pos)
        
        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        
        # Timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool),
            'tool_switch': Timer(200),
            'seed_use': Timer(350, self.use_seed),
            'seed_switch': Timer(200)
        }
        
        # Tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_idx = 0
        self.selected_tool = self.tools[self.tool_idx]
        
        # Seeds
        self.seeds = ['corn', 'tomatoe']
        self.seed_idx = 0
        self.selected_seed = self.seeds[self.seed_idx]
    
    def animate(self, dt):
        self.frame_idx += 4 * dt
        if self.frame_idx >= len(self.animations[self.status]):
            self.frame_idx = 0
        
        self.image = self.animations[self.status][int(self.frame_idx)]
    
    def get_status(self):
        # Idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # Tool use
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
    
    def import_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['tool_use'].active:
            # Directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
                
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            
            # Tool Use
            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_idx = 0
            # Tool Change
            if keys[pygame.K_a] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_idx += 1
                # if self.tool_idx >= len(self.tools):
                #     self.tool_idx = 0
                # 'Ternary' version
                self.tool_idx = self.tool_idx if self.tool_idx < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_idx]
                
            # Seed Use
            if keys[pygame.K_LCTRL]:
                self.timers['seed_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_idx = 0
            # Change Seed
            if keys[pygame.K_e] and not self.timers['seed_switch'].active:
                self.timers['seed_switch'].activate()
                self.seed_idx += 1
                self.seed_idx = self.seed_idx if self.seed_idx < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_idx]

    def move(self, dt):
        # Normalizing the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            
        # Horizontal mvt
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        
        # Vertical mvt
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def use_seed(self):
        pass
    
    def use_tool(self):
        pass
                 
    def update(self, dt) -> None:
        self.input()
        self.get_status()
        self.update_timers()
        
        self.move(dt)
        self.animate(dt)