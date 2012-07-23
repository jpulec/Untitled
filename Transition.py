from Constants import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT, TRANSITION
from pygame.locals import *


class Transition:
    def __init__(self, dic):
        self.type = dic["type"]
        self.color = dic["color"]
        self.r = 0
        self.g = 0
        self.b = 0
        if self.color == "white":
            self.r = self.g = self.b = 255
     

    def draw(self):
        if self.type == "fade":
            DISPLAY.screen.fill((self.r,self.g,self.b), None, BLEND_SUB)
                

    def update(self):
        if self.type == "fade":
            if self.color == "black":
                self.r += 1
                self.g += 1
                self.b += 1
                if self.r == 255:
                    pygame.Event(TRANSITION, {"type":"fade", "color":"white"})
            elif self.color == "white":
                self.r -= 1
                self.g -= 1
                self.b -= 1
                if self.r == 0:
                    pass#pygame.Event()

    def handle_events(self, e):
        return
