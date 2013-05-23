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
        self.cursor = Cursor(self.player.col_rect.copy(), "system", frame_count=4)
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
            for sprite in self.sprites.sprites:
                print sprite
            print "Fuck yea, some crazy black magic voodoo class shit is going on here"
        
        elif event.key == pl.K_TAB:
            self.finished()

    def finished(self):
        self.sprites.remove(self.cursor)
        self.__class__ = overworld.Overworld

class Cursor(sprite_bases.AnimatedSprite):
    def __init__(self, location, *args, **kwargs):
        super(Cursor, self).__init__(*args, **kwargs)
        self.rect = location
