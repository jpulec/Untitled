import pygame
from constants import *

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name, fps=10):
        super(AnimatedSprite, self).__init__()
        self.name = name
        self.image = IM.textures[name][0] 
        self.src_rect = None
        self._frame = 1
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(IM.sprite_rects[self.name]):
                self._frame = 1
            self.src_rect = IM.sprite_rects[self.name][self._frame]
            self._last_update = t

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, name, fps=10):
        super(MovingSprite, self).__init__()
        self.name = name
        self.image = IM.textures[name][0] 
        self.src_rect = None
        self.moving = False
        self.direction = DIRECTIONS.N
        self._frame = 1
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):
        if self.moving:
            if t - self._last_update > self._delay:
                self._frame += 1
                if self._frame >= len(IM.sprite_rects[self.name]):
                    self._frame = 1
                self.src_rect = IM.sprite_rects[self.name][self._frame]
                self._last_update = t
        else:
            self._last_update = t

class Creature(AnimatedSprite):
    def __init__(self, name):
        super(Creature, self).__init__(name)
        self.HP = 0
        self.shit = []
        self.carryAbility = 0

class Avatar(MovingSprite):
    def __init__(self, name):
        super(Avatar, self).__init__(name)
        self.rect = pygame.Rect(DISPLAY.screen_width / 2 - 16, DISPLAY.screen_height / 2 - 16 + 32, TILE_SIZE, TILE_SIZE)
