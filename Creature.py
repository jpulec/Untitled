import string
import pygame
import Attributes

class Creature(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.attributes = Attributes.Attributes() 
        self.HP = int(self.attributes.maxHP())
        self.shit = []
        self.carryAbility = 0



