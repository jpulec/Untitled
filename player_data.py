import sprite_bases
import pygame


class PlayerData(sprite_bases.Creature):

    def __init__(self, name):
        super(PlayerData, self).__init__(name)
        self.currentSkin = None
        self.rHand = None
        self.lHand = None
        self.armor = None
        self.alive = True

    def drawOnMap(self):
        playerSurface = imageManager.textures[self.currentSkin][0]
        playerSprite = imageManager.spriteRects[
            self.currentSkin][self.facing + 1]
        screen.blit(playerSurface, self.rect, playerSprite)
