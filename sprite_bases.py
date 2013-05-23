import pygame
from constants import *

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name, fps=10, frame=1, frame_count=4, *args, **kwargs):
        super(AnimatedSprite, self).__init__(*args, **kwargs)
        self.name = name
        self.frame_count = frame_count
        self.image = IM.textures[name][0]
        self.src_rect = None
        self._frame = frame
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame > self.frame_count:
                self._frame = 1
            self.src_rect = IM.sprite_rects[self.name][self._frame]
            self._last_update = t

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, name, fps=60):
        super(MovingSprite, self).__init__()
        self.name = name
        self.image = IM.textures[name][0] 
        self._frame = 2
        self.src_rect = IM.sprite_rects[self.name][self._frame]
        self.col_rect = None
        self.moving = False
        self.animate = False
        self.direction = Directions.S
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):
        if self.animate:
            if t - self._last_update > self._delay:
                self._frame += 2
                if self._frame % 3 == 0:
                    self.moving = False
                if self._frame  >= 10:
                    self._frame = 2
                    if not self.moving:
                        self.animate = False
                self.src_rect = IM.sprite_rects[self.name][(self._frame / 2) + self.direction]
                self._last_update = t
        else:
            self._frame = 2
            self.src_rect = IM.sprite_rects[self.name][(self._frame / 2) + self.direction]
            self._last_update = t

class Creature(AnimatedSprite):
    def __init__(self, name):
        super(Creature, self).__init__(name)
        self.HP = 0
        self.shit = []
        self.carryAbility = 0

class Avatar(MovingSprite):
    def __init__(self, name):
        super(Avatar, self).__init__(name, fps=10)
        self.col_rect = pygame.Rect(DISPLAY.screen_width / 2 - TILE_SIZE / 2, DISPLAY.screen_height / 2 - TILE_SIZE / 2 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.rect = pygame.Rect(DISPLAY.screen_width / 2 - TILE_SIZE / 2, DISPLAY.screen_height / 2 - TILE_SIZE / 2, TILE_SIZE, TILE_SIZE)
