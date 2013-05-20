import pygame

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

class SourceRectGroup(pygame.sprite.Group):
    def __init__(self, *args, **kwargs):
        super(SourceRectGroup, self).__init__(*args, **kwargs)

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect, spr.src_rect)
        self.lostsprites = []
