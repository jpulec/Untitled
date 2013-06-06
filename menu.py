import cevent
import pygame
import text_box


class MenuHandler(text_box.TextBoxHandler):
    def __init__(self, *args, **kwargs):
        super(MenuHandler, self).__init__(*args, **kwargs)
        self.menu = None

    def initialize(self, *args, **kwargs):
        self.menu = Menu(*args, **kwargs)
    
    def on_key_down(self, event):
        if event.key == pl.K_RETURN:
            self.sprites.remove(self.menu)
            self.__class__ = overworld.Overworld

class Menu(text_box.TextBox):
    def __init__(self, items, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        print items
        self.items = items

    def construct_box(self):
        #this will be constructed box
        font_size = self.font.size(max(self.items, key=len))[0], len(self.items)*32
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
        for count, item in enumerate(self.items):
            surf.blit(self.font.render(item, True, self.color), (self.border[0], self.border[1] + count*32))
            self.image = surf

