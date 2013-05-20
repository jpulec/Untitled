import pygame
import display_info
import image_data
import player_data
import overworld
import sys
import cevent
import party
import transition
from constants import *

class Main(cevent.CEvent):
    def __init__(self):
        super(Main, self).__init__()
        pygame.init()
        self.party = party.Party()
        pygame.font.init()
        pygame.key.set_repeat(75, 75)
        self.init_display()
        self.font = pygame.font.Font(None, 24)
        self.window_context = None
        self.overworld = None
        self.debug = False
        self.event_wait = False
        self.quit_flag = False
        
    def init_display(self):
        DISPLAY.create_screen()       
        DISPLAY.screen.fill((0, 0, 0))
    

    def main_loop(self):
        self.init_world()
        while(not self.quit_flag):
            #event2 = pygame.event.peek([LOAD_MAP])
            for event in pygame.event.get():
                self.on_event(event)
            self.window_context.draw()
            pygame.display.flip()
            TIMER.tick(60)

    def on_key_down(self, event):
        print event
    
    def on_exit(self):
        self.quit_flag = True
        sys.exit(0)

    def game_draw(self):
        if self.debug:
            DISPLAY.screen.blit(self.font.render(str(TIMER.get_fps()), 0, (255,255,255)), (24,24))

    def init_world(self):
        self.overworld = overworld.Overworld()
        self.window_context = self.overworld
        self.overworld.load_map("maps/Bank_Inside.tmx", 0, 0)
        self.party.team["Miles"] = player_data.PlayerData("Miles_regular")


if __name__ == "__main__":                                                   
    game = Main()
    game.main_loop()
