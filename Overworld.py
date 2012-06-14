import pygame
from pytmx import tmxloader
import PlayerData
import WindowContext
from pygame.locals import *

class Overworld(WindowContext.WindowContext):
    def __init__(self, display):
        WindowContext.WindowContext.__init__(self)
        self.display = display
        self.map = None
        self.player = None
        self.xOffset = 0
        self.yOffset = 0
        self.xStart = 0
        self.yStart = 0
        self.yStartOff = 0
        self.xStartOff = 0
        self.collide = []
        self.nextTile = [0,0]

    def loadMap(self, mapName):
        self.map = tmxloader.load_pygame(mapName, pixelalpha = False)
        for objgrp in self.map.objectgroups:
            for obj in objgrp.objects:
                if hasattr(obj, "gamestart"):
                    print str(obj.x*2 - self.display.screenwidth / 2),
                    print str(obj.y*2 - self.display.screenheight/ 2)
                    self.xStartOff = (obj.x*2 - self.display.screenwidth / 2)
                    self.yStartOff = (obj.y*2 - self.display.screenheight/ 2)
                    self.xStart = obj.x / 16
                    self.yStart = obj.y / 16

    def draw(self):
        self.drawWorld()

    def update(self):
        self.updateWorld()

    def handleEvents(self, e):
        if e.key == K_ESCAPE:
            #TODO: implement whatever behavior I want here
            return
        #TODO: this movement needs some work, should really fix collisions and such
        if e.key == K_LEFT: 
            if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                if self.mapTileNull(-1, 0):
                    print "NULL"
                    self.nextTile = [-1,0]
                else:
                    if not self.mapTileCollidable(-1, 0):
                        print "NOTCOLLIDE"
                        self.nextTile = [-1,0]
                    else:
                        print "COLLIDE"
                        self.nextTile[0] = 0
                self.player.facing = 12

        elif e.key == K_RIGHT:
            if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                if self.mapTileNull(1, 0):
                    self.nextTile = [1,0]
                else:
                    if not self.mapTileCollidable(1, 0):
                        self.nextTile = [1,0]
                    else:
                        self.nextTile[0] = 0
                self.player.facing = 4
               
        elif e.key == K_UP:
            if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                if self.mapTileNull(0, -1):
                    self.nextTile = [0,-1]
                else:
                    if not self.mapTileCollidable(0, -1):
                        self.nextTile = [0,-1]
                    else:
                        self.nextTile[1] = 0
                self.player.facing = 0

        elif e.key == K_DOWN:
            if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                if self.mapTileNull(0, 1):
                    self.nextTile = [0,1]
                else:
                    if not self.mapTileCollidable(0, 1):
                        self.nextTile = [0, 1]
                    else:
                        self.nextTile[1] = 0
                self.player.facing = 8

        elif e.key == K_RETURN:
            if self.xOffset % 32 == 0 and self.yOffset % 32  == 0:
                if self.player.facing == 0:
                    if not self.mapTileNull(0, -1):
                        if self.mapTileCollectible(0, -1):
                            print "ADD"
                elif self.player.facing == 4:
                    if not self.mapTileNull(1, 0):
                        if self.mapTileCollectible(1, 0):
                            print "ADD"

                elif self.player.facing ==8:
                    if not self.mapTileNull(0, 1):
                        if self.mapTileCollectible(0, 1):
                            print "ADD"

                elif self.player.facing == 12:
                    if not self.mapTileNull(-1, 0):
                        if self.mapTileCollectible(-1, 0):
                            print "ADD"

    def updateWorld(self):
        if self.nextTile[0] is not 0 or self.xOffset % 32 is not 0:
            if self.player.facing % 4 == 3 and self.xOffset % 32 == 0:
                self.player.facing -= 3
                self.nextTile[0] = 0
            elif self.player.facing % 4 == 0 and self.xOffset % 32 == 0:
                self.xOffset += 4*self.nextTile[0]
            

            elif self.xOffset % 8 == 0:
                self.player.facing += 1
                self.xOffset += 4*self.nextTile[0]
            
            elif self.xOffset % 4 == 0:
                self.xOffset += 4*self.nextTile[0]
            
            
        elif self.nextTile[1] is not 0 or self.yOffset % 32 is not 0:
            if self.player.facing % 4 == 0 and self.yOffset % 32 == 0:
                self.yOffset += 4*self.nextTile[1]
            elif self.player.facing % 4 == 3 and self.yOffset % 32 == 0:
                self.player.facing -= 3
                self.nextTile[1] = 0

            elif self.yOffset % 8 == 0:
                self.player.facing += 1
                self.yOffset += 4*self.nextTile[1]
            
            elif self.yOffset % 4 == 0:
                self.yOffset += 4*self.nextTile[1]

    def mapTileNull(self, x, y):
        return self.map.getTileProperties((self.xOffset / 32 + x, self.yOffset / 32 + y,2)) is None

    def mapTileCollidable(self, x, y):
        print str(self.xOffset / 32 + x),
        print str(self.yOffset / 32 + y)
        print str((self.xOffset - self.xStart) / 32 + x),
        print str((self.yOffset - self.yStart)/ 32 + y)
        gid = self.map.getTileGID((self.xOffset) / 32 + x + self.xStart, (self.yOffset)/ 32 + y + self.yStart,2)
        if gid:
            return self.map.getTilePropertiesByGID(gid).has_key("collidable")

    def mapTileCollectible(self, x, y):
        gid = self.map.getTileGID(self.xOffset / 32 + x, self.yOffset / 32 + y,2)
        if gid:
            tiles = self.map.getLayerData(2)
            itemgid = self.map.getTileGID(self.xOffset / 32 + x, self.yOffset / 32 + y,1)
            if itemgid:
                contents = self.map.getTilePropertiesByGID(itemgid)
                print str(self.map.objectgroups[0].objects[0])
                print "GOT ITEM" + str(contents)

    def mapPortal(self, x, y):
        for objgrp in self.map.objectgroups:
            for obj in objgrp.objects:
                if obj.has_key("portal"):
                    pass

    def getGameStart(self):
        return (self.map.objectgroups[0].objects[0].x*2, self.map.objectgroups[0].objects[0].y*2)
        

    def drawWorld(self):
        self.display.screen.fill((0, 0, 0))
        self.drawMap()
        self.player.draw()

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
                    if tile: self.display.screen.blit(pygame.transform.scale2x(tile), (x*tw - self.xOffset -self.xStart * 32, y*th - self.yOffset - self.yStart*32))


class Avatar:
    def __init__(self, name, display, im):
        self.display = display
        self.im = im
        self.rect = pygame.Rect(display.screenwidth / 2, display.screenheight / 2, 32, 32)
        self.facing = 0
        self.currentSkin = None


    def draw(self):
        playerSurface = self.im.textures[self.currentSkin][0]
        playerSprite = self.im.spriteRects[self.currentSkin][self.facing + 1]
        self.display.screen.blit(playerSurface, self.rect, playerSprite)

