import pygame
import display_info
import image_loader
import player_data
import overworld
import sys
import cevent
import party
import battlefield
from constants import *

class Main(object):
    def __init__(self):
        super(Main, self).__init__()
        pygame.init()
        #self.party = party.Party()
        pygame.font.init()
        pygame.key.set_repeat(75, 75)
        self.init_display()
        self.font = pygame.font.Font(None, 24)
        self.context = None
        self.overworld = None
        self.debug = True

    def init_display(self):
        DISPLAY.create_screen()
        DISPLAY.screen.fill((0, 0, 0))


    def main_loop(self):
        self.init_world()
        while(True):
            for event in pygame.event.get():
                self.context.on_event(event)
            self.context.update()
            self.context.render(DISPLAY.screen)
            self.game_draw()
            pygame.display.flip()
            TIMER.tick(60)

    def game_draw(self):
        if self.debug:
            DISPLAY.screen.blit(self.font.render(str(TIMER.get_fps()), 0, (255,255,255)), (24,24))
            DISPLAY.screen.blit(self.font.render(str(self.context.cam_world_pos_x) + " " + str(self.context.cam_world_pos_y), 0, (255,255,255)), (600, 24))

    def init_world(self):
        self.overworld = overworld.Overworld("maps/Bank_Inside.tmx")
        self.context = self.overworld
        #self.party.team["Miles"] = player_data.PlayerData("Miles_regular")


if __name__ == "__main__":
    game = Main()
    game.main_loop()
