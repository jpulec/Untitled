import cevent
import math
import pygame
import pygame.locals as pl
import overworld
from constants import *

class TextBoxHandler(overworld.Overworld):
    def __init__(self, *args, **kwargs):
        super(TextBoxHandler, self).__init__(*args, **kwargs)
        self.text_box = None

    def initialize(self, *args, **kwargs):
        self.text_box = TextBox(*args, **kwargs)

    def on_key_down(self, event):
        if event.key == pl.K_t:
            self.sprites.remove(self.text_box)
            self.__class__ = overworld.Overworld

class TextBox(pygame.sprite.Sprite):
    def __init__(self, position, text, color, *args, **kwargs):
        super(TextBox, self).__init__(*args, **kwargs)
        self.text = text
        self.rect = position
        self.image = IM.textures["textbox"]
        self.font = pygame.font.Font(None, 24)
        self.color = color
        self.border = (7,7)
        self.construct_box()

    def construct_box(self):
        #this will be constructed box
        font_size = self.font.size(self.text)
        if font_size[1] < 64:
            font_size = (font_size[0], 64)
        font_size = font_size[0] + self.border[0], font_size[1] + self.border[1]
        font_size = int(32 * (font_size[0]/32 + 1)), int(32 * (font_size[1]/32 + 1))
        surf = pygame.Surface(font_size)
        for row in xrange(0, font_size[0], 32): #rows
            for col in xrange(0, font_size[1], 32): #cols
                if row == 0:
                    if col == 0:
                        surf.blit(self.image[0], (row,col))
                    elif (col + 32) >= font_size[1]:
                        surf.blit(self.image[6], (row,col))
                    else:
                        surf.blit(self.image[3], (row,col))
                elif (row + 32) >= font_size[0]:
                    if col == 0:
                        surf.blit(self.image[2], (row,col))
                    elif (col + 32) >= font_size[1]:
                        surf.blit(self.image[8], (row,col))
                    else:
                        surf.blit(self.image[5], (row,col))
                else:
                    if col == 0:
                        surf.blit(self.image[1], (row,col))
                    elif (col + 32) >= font_size[1]:
                        surf.blit(self.image[7], (row,col))
                    else:
                        surf.blit(self.image[4], (row,col))

        surf.blit(self.font.render(self.text, True, self.color), self.border)
        self.image = surf
