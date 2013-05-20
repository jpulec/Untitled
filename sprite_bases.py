import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, fps=10):
        super(AnimatedSprite, self).__init__()
        self._images = images

        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
                self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t

class Creature(AnimatedSprite):
    def __init__(self, name):
        super(Creature, self).__init__(name)
        self.name = name
        self.HP = 0
        self.shit = []
        self.carryAbility = 0



