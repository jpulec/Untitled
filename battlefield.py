import cevent
import overworld
import sprite_bases
from constants import *
import pygame.locals as pl

class Battlefield(overworld.Overworld):
    def __init__(self, *args, **kwargs):
        super(Battlefield, self).__init__(*args, **kwargs)
        self.cursor = None
        self.selected = None

    def initialize(self):
        self.cursor = Cursor(self.player.rect.copy(), "system", frame_count=4)
        self.sprites.add(self.cursor)

    def on_key_down(self, event):
        if event.key == pl.K_LEFT:
            self.cursor.rect.move_ip(-32, 0)

        elif event.key == pl.K_RIGHT:
            self.cursor.rect.move_ip(32, 0)
               
        elif event.key == pl.K_UP:
            self.cursor.rect.move_ip(0, -32)

        elif event.key == pl.K_DOWN:
            self.cursor.rect.move_ip(0, 32)

        elif event.key == pl.K_RETURN:
            for sprite in self.sprites:
                if self.cursor.rect.copy().move(-TILE_SIZE,0).contains(sprite.rect):
                    # oh yeah, here be sprites under my selector
                    #new_layer = TiledLayer(self.map, None)
                    #new_layer
                    self.map.tilelayers[0].data[self.cursor.rect.top / TILE_SIZE + 1][self.cursor.rect.left / TILE_SIZE - 1] = 111
                    self.map.tilelayers[1].data[self.cursor.rect.top / TILE_SIZE + 1][self.cursor.rect.left / TILE_SIZE - 1] = 111
                    print sprite
            print "Fuck yea, some crazy black magic voodoo class shit is going on here"
        
        elif event.key == pl.K_b:
            self.finished()

    def finished(self):
        self.sprites.remove(self.cursor)
        self.__class__ = overworld.Overworld

class Cursor(sprite_bases.AnimatedSprite):
    def __init__(self, location, *args, **kwargs):
        super(Cursor, self).__init__(*args, **kwargs)
        location.move_ip(TILE_SIZE, 0)
        self.rect = location
