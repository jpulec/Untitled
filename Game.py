import pygame
import DisplayInfo
import ImageData
import PlayerData
import Overworld
import Party
import Transition
from pygame.locals import *
from Constants import *

class Game:
    def __init__(self):
        self.party = Party.Party()
        pygame.font.init()
        pygame.key.set_repeat(75, 75)
        self.init_display()
        self.font = pygame.font.Font(None, 24)
        self.window_context = None
        self.overworld = None
        self.debug = False
        self.quit_flag = False
        
       

    def init_display(self):
        DISPLAY.create_screen()       
        DISPLAY.screen.fill((0, 0, 0))
    

    def main_loop(self):
        self.init_world()
        while(not self.quit_flag):
            for e in pygame.event.get():
                self.handle_events(e)
            self.window_context.update()
            self.window_context.draw()
            self.game_draw()         #really only for debug stuff, since it will draw over the top of other contexts
            pygame.display.flip()
            TIMER.tick(60)
        #TODO:quit cleanup code here

    def game_draw(self):
        if self.debug:
            DISPLAY.screen.blit(self.font.render(str(TIMER.get_fps()), 0, (255,255,255)), (24,24))

    def init_world(self):
        self.overworld = Overworld.Overworld()
        self.window_context = self.overworld
        self.overworld.load_map("maps/Bank_Inside.tmx", 0, 0)
        self.party.team["Miles"] = PlayerData.PlayerData("Miles_regular")


    def handle_events(self, e):
        if e.type == QUIT:
            self.quit_flag = True
            return
        if e.type == TRANSITION:
            print "TRANSITION"
            self.window_context = Transition.Transition(e.dict)
        if e.type == KEYDOWN:
            self.mods =  pygame.key.get_mods()       
            if e.key == K_RETURN and (self.mods & KMOD_CTRL):   #pretty sure precise pangolin (12.04) screwed this up with Alt mapped to HUD, so now its CTRL
                DISPLAY.is_fullscreen = (DISPLAY.is_fullscreen + 1) % 2   
                DISPLAY.create_screen()
            elif e.key == K_F1:    #debug stuff...at least fps
                self.debug = not self.debug
            else:
                self.window_context.handle_events(e)
            


if __name__ == "__main__":                                                   
    game = Game()
    game.main_loop()
