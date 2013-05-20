#Global constant data
import image_data
import display_info
import pygame.time
import utils

DIRECTIONS = utils.Enum(["N", "E", "S", "W"])

TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

IM = image_data.ImageData()
IM.setup()
DISPLAY = display_info.DisplayInfo(SCREEN_WIDTH, SCREEN_HEIGHT)
TIMER =  pygame.time.Clock()

#Custom events
TRANSITION  = pygame.USEREVENT + 1
LOAD_MAP    = pygame.USEREVENT + 2
OVERWORLD   = pygame.USEREVENT + 3
