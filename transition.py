from constants import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT, TRANSITION
import pygame


class Transition(object):
    def __init__(self, dic):
        self.type = dic["type"]
        self.background = dic["background"]
        self.alpha = 0
        self.background.convert()
        self.event_wait = True

    def draw(self):
        if self.type == "fade":
            if self.alpha < 255:
                self.background.set_alpha(self.alpha)
                DISPLAY.screen.blit(self.background, (0,0))
            else:
                self.event_wait = False

    def update(self):
        if self.type == "fade":
            self.alpha += 10

    def handle_events(self, e):
        return
