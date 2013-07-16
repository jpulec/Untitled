# Global constant data
import image_loader
import display_info
import pygame.time
import utils


class Directions(object):
    (N, E, S, W) = (0, 4, 8, 12)

TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

DISPLAY = display_info.DisplayInfo(SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY.create_screen()
IM = image_loader.ImageLoader()
IM.setup()
TIMER = pygame.time.Clock()

# Custom events
TRANSITION = pygame.USEREVENT + 1
LOAD_MAP = pygame.USEREVENT + 2
OVERWORLD = pygame.USEREVENT + 3
