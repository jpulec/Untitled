import pygame
import DisplayInfo
import ImageData
import PlayerData
import Overworld
import Party
from pytmx import tmxloader
pygame.init()
from pygame.locals import *
   
 


class Game:
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.display = DisplayInfo.DisplayInfo()
        self.textureManager = ImageData.ImageData()
        self.party = Party.Party()
        pygame.font.init()
        pygame.key.set_repeat(75, 75)
        self.initDisplay()
        self.font = pygame.font.Font(None, 24)
        self.windowContext = None
        self.overworld = None
        self.debug = False
        self.quitFlag = False
        
       

    def initDisplay(self):
        self.display.createScreen()       
        self.display.screen.fill((0, 0, 0))
    

    def mainloop(self):
        self.initWorld()
        while(not self.quitFlag):
            for e in pygame.event.get():
                self.handleEvents(e)
            self.windowContext.update()
            self.windowContext.draw()
            self.gameDraw()         #really only for debug stuff, since it will draw over the top of other contexts
            pygame.display.flip()
            self.timer.tick(60)
        #TODO:quit cleanup code here

    def gameDraw(self):
        if self.debug:
            self.display.screen.blit(self.font.render(str(self.timer.get_fps()), 0, (255,255,255)), (24,24))

    def initWorld(self):
        self.overworld = Overworld.Overworld(self.display)
        self.windowContext = self.overworld
        self.overworld.loadMap("maps/Bank_Inside.tmx")
        self.overworld.player = Overworld.Avatar("Miles", self.display, self.textureManager)
        self.overworld.player.currentSkin = "Miles_regular"
        self.overworld.player.facing = 7
        self.party.team["Miles"] = PlayerData.PlayerData("Miles_regular")


    def handleEvents(self, e):
        if e.type == QUIT:
            self.quitFlag = True
            return
        if e.type == KEYDOWN:
            self.mods =  pygame.key.get_mods()       
            if e.key == K_RETURN and (self.mods & KMOD_CTRL):   #pretty sure precise pangolin (12.04) screwed this up with Alt mapped to HUD, so now its CTRL
                self.display.isFullscreen = (self.display.isFullscreen + 1) % 2   
                self.display.createScreen()
            elif e.key == K_F1:    #debug stuff...at least fps
                self.debug = not self.debug
            else:
                self.windowContext.handleEvents(e)
            


if __name__ == "__main__":                                                   
    game = Game()
    game.mainloop()
