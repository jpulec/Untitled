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
        self.collide = []
        self.nextTile = [0,0]

    def loadMap(self, mapName):
        self.map = tmxloader.load_pygame(mapName, pixelalpha = False)
        self.setupCollidables()

    def draw(self):
        self.drawWorld()
    
    def setupCollidables(self):
        pass        
        for array in self.map.tilelayers[2].data:
            for tile in array:
                if self.map.getTilePropertiesByGID(tile) is not None:
                    if self.map.getTilePropertiesByGID(tile).has_key("collidable"):
                        for x in self.map.getTileLocation(tile):
                            self.collide.append(pygame.Rect(x[0]*32 -1, x[1]*32 -1, 33, 33))
                        #self.collide.append(pygame.Rect(tile.x *32, tile.y*32, 32, 32))
        print str(len(self.collide))


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
                    self.nextTile = [-1,0]
                else:
                    if not self.mapTileCollidable(-1, 0):
                        self.nextTile = [-1,0]
                    else:
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
        return self.map.getTileProperties(((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y,2)) is None

    def mapTileCollidable(self, x, y):
        gid = self.map.getTileGID((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y,2)
        if gid:
            return self.map.getTilePropertiesByGID(gid).has_key("collidable")

    def mapTileCollectible(self, x, y):
        gid = self.map.getTileGID((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y,2)
        if gid:
            tiles = self.map.getLayerData(2)
            tiles[(self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x][(self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y] = None
            itemgid = self.map.getTileGID((self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x, (self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y,1)
            if itemgid:
                contents = self.map.getTilePropertiesByGID(itemgid)
                print "GOT ITEM" + str(contents)
            tiles = self.map.getLayerData(1)
            tiles[(self.map.objectgroups[0].objects[0].x*2  + self.xOffset) / 32 + x][(self.map.objectgroups[0].objects[0].y*2 + self.yOffset) / 32 + y] = None
        

    def drawWorld(self):
        self.display.screen.fill((0, 0, 0))
        self.drawMap()
        self.player.draw()
        #print "DRAWNEXT:" + str(self.nextTile[0])

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


class Avatar:
    def __init__(self, name, display, im):
        self.display = display
        self.im = im
        self.rect = pygame.Rect(display.screenwidth / 2, display.screenheight / 2, 32, 32)
        self.facing = 0
        self.currentSkin = None


    def draw(self):
        playerSurface =  self.im.textures[self.currentSkin][0]
        playerSprite = self.im.spriteRects[self.currentSkin][self.facing + 1]
        self.display.getScreen().blit(playerSurface, self.rect, playerSprite)

