
import Creature
import pygame


class PlayerData(Creature.Creature):
    def __init__(self, name, display):
        Creature.Creature.__init__(self, name)        
        self.facing = 1
        #self.collisionRect = pygame.Rect(288, 216, 24, 24)
        #self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(display.screenwidth / 2, display.screenheight / 2, 32, 32)
        self.image = None
        self.currentSkin = None
        self.rHand = None
        self.lHand = None
        self.armor = None
        self.alive = True


    def drawOnMap(self, imageManager, screen):
        playerSurface =  imageManager.textures[self.currentSkin][0]
        playerSprite = imageManager.spriteRects[self.currentSkin][self.facing + 1]
        screen.blit(playerSurface, self.rect, playerSprite)

