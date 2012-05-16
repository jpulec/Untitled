import pygame
import DisplayInfo
import ImageData
import PlayerData
from pytmx import tmxloader
pygame.init()
from pygame.locals import *
   
 


class Game:
    def __init__(self):
        self.timer = pygame.time.Clock()
        self.display = DisplayInfo.DisplayInfo()
        self.textureManager = ImageData.ImageData()
        self.player = PlayerData.PlayerData("Miles", self.display)
        pygame.font.init()
        pygame.key.set_repeat(75, 75)
        self.initDisplay()
        self.font = pygame.font.Font(None, 24)
        self.map = tmxloader.load_pygame("maps/Bank_Inside.tmx", pixelalpha=True)
        self.xOffset = 0
        self.yOffset = 0
        self.quitFlag = False
        
       

    def initDisplay(self):
        self.display.createScreen()       
        self.display.screen.fill((0, 0, 0))
    

    def mainloop(self):
        self.initWorld()
        while(not self.quitFlag):
            for e in pygame.event.get():
                self.handleInput(e)
                pygame.event.pump()
            self.drawWorld()
            pygame.display.flip()
            self.timer.tick(60)
        #TODO:quit cleanup code here


    def initWorld(self):
        self.initPlayer()


    def initPlayer(self):
        self.player.currentSkin = "Miles_regular"

    def handleInput(self, e):
        if e.type == QUIT:
            self.quitFlag = True
            return
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.quitFlag = True
                return
            if e.key == K_LEFT: 
                if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                    if self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 - 1, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32,2)) is None:
                        self.xOffset -= 8
                    else:
                        if not self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 - 1, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32,2)).has_key("collidable"):
                            self.xOffset -= 8
                    self.player.facing = 10

            elif e.key == K_RIGHT:
                if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                    if self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + 1, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32,2)) is None:
                        self.xOffset += 8
                    else:
                        if not self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + 1, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32,2)).has_key("collidable"):
                            self.xOffset += 8
                    self.player.facing = 4
                   
            elif e.key == K_UP:
                if self.yOffset % 32 == 0 and self.xOffset % 32  == 0:
                    if self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 - 1,2)) is None:
                        self.yOffset -= 8
                    else:
                        if not self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 - 1,2)).has_key("collidable"):
                            self.yOffset -= 8
                    self.player.facing = 1
  
            elif e.key == K_DOWN:
                if self.yOffset % 32 == 0 and self.xOffset % 32  == 0:
                    if self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + 1,2)) is None:
                        self.yOffset += 8
                    else:
                        if not self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + 1,2)).has_key("collidable"):
                            self.yOffset += 8
                    self.player.facing = 7
        
            self.mods =  pygame.key.get_mods()       
            if e.key == K_RETURN and (self.mods & KMOD_CTRL):   #pretty sure precise pangolin (12.04) screwed this up with Alt mapped to HUD, so now its CTRL
                self.display.isFullscreen = (self.display.isFullscreen + 1) % 2   
                self.display.createScreen()

    def drawWorld(self):
        self.display.screen.fill((0, 0, 0))

        
        
        
       
        if (self.xOffset % 32) is not 0:
            if self.xOffset % 32 == 8 and self.player.facing < 6:
                self.player.facing = (self.player.facing - 1)
                self.xOffset += 8
            elif self.player.facing == 5: 
                self.player.facing = 4
                self.xOffet += 8            
            elif self.player.facing < 6:
                self.player.facing = (self.player.facing + 1)
                self.xOffset += 8
        

            elif self.xOffset % 32 == 24 and self.player.facing > 8:    #neg mods....
                self.player.facing = (self.player.facing - 1)
                self.xOffset -= 8
            elif self.player.facing == 11: 
                self.player.facing = 10
                self.xOffset -= 8
            elif self.player.facing > 8:
                self.player.facing = (self.player.facing + 1)
                self.xOffset -= 8            
            
        elif (self.yOffset % 32) is not 0:
            if self.yOffset % 32 == 24 and self.player.facing < 3:
                self.player.facing = (self.player.facing - 1)
                self.yOffset -= 8
            
            elif self.player.facing == 2: 
                self.player.facing = 1
                self.yOffset -= 8
            elif self.player.facing < 3:
                self.player.facing = (self.player.facing + 1)
                self.yOffset -= 8
   
            elif self.yOffset % 32 == 8 and self.player.facing > 5:
                self.player.facing = (self.player.facing - 1)
                self.yOffset += 8
            
            elif self.player.facing == 8: 
                self.player.facing = 7
                self.yOffset += 8
            elif self.player.facing > 5:
                self.player.facing = (self.player.facing + 1)
                self.yOffset += 8

        self.drawMap()
        self.player.drawOnMap(self.textureManager, self.display.getScreen())

    def drawMap(self):
        #TODO: make this way more efficient
        tw = self.map.tilewidth * 2
        th = self.map.tileheight *2
        gt = self.map.getTileImage
      
        for l in xrange(0, len(self.map.tilelayers)):
            if hasattr(self.map.layers[l], "meta"):
                continue
            for y in xrange(0, self.map.height):
                for x in xrange(0, self.map.width):
                    tile = gt(x, y, l)
                    if tile: self.display.screen.blit(pygame.transform.scale2x(tile), (x*tw - (self.map.objectgroups[0].objects[0].x*2 - (self.display.screenwidth) / 2) - self.xOffset, y*th - (self.map.objectgroups[0].objects[0].y*2 - 32 - (self.display.screenheight) / 2)  - self.yOffset))

if __name__ == "__main__":                                                   
    game = Game()
    game.mainloop()
