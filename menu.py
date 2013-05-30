import cevent
import pygame
import text_box


class Menu(text_box.TextBox):
    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self.choices = {}



