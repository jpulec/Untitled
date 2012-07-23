#Global constant data
import ImageData
import DisplayInfo
import pygame.time
from pygame.locals import *

TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

IM = ImageData.ImageData()
IM.setup()
DISPLAY = DisplayInfo.DisplayInfo(SCREEN_WIDTH, SCREEN_HEIGHT)
TIMER =  pygame.time.Clock()

#Custom events
TRANSITION = pygame.USEREVENT + 1
