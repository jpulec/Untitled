import pygame
import pytmx
import utils
import player_data
import inspect
import sys
import cevent
import sprite_bases
from constants import *
import pygame.locals as pl

class Overworld(cevent.CEvent):
    def __init__(self, map_name, *args, **kwargs):
        super(Overworld, self).__init__(*args, **kwargs)
        self.map = pytmx.tmxloader.load_pygame(map_name, pixelalpha=True)
        self.player = sprite_bases.Avatar("Miles_regular") 
        self.cam_world_pos_x = 0
        self.cam_world_pos_y = 0
        self.sprites = utils.SourceRectGroup()
        self.sprites.add(self.player)

    def render(self, surface):
        #TODO: Make this more efficient and a little cleaner, especially with the edge drawing

        DISPLAY.screen.fill((0,0,0))
        tw = self.map.tilewidth
        th = self.map.tileheight
        gt = self.map.getTileImage
        for l in xrange(0, len(self.map.tilelayers)):
            if self.map.tilelayers[l].visible:
                for y in xrange(0, self.map.height):
                    for x in xrange(0, self.map.width):
                        tile = gt(x, y, l)
                        if tile:
                            surface.blit(tile, (x*tw - self.cam_world_pos_x, y*th - self.cam_world_pos_y))
        self.sprites.draw(surface)
        for y in xrange(0, self.map.height):
            for x in xrange(0, self.map.width):
                tile = gt(x, y, 2)
                if tile:
                    surface.blit(tile, (x*tw - self.cam_world_pos_x, y*th - self.cam_world_pos_y))



    def update(self):
        self.update_world()
        self.sprites.update(pygame.time.get_ticks())

    def on_exit(self):
        #TODO: Probably need to handle this more gracefully
        sys.exit(0)

    def on_key_down(self, event):
        if event.key == pl.K_LEFT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                self.player.direction = Directions.W
                self.player.moving = True
            self.player.animate = True

        elif event.key == pl.K_RIGHT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                self.player.direction = Directions.E
                self.player.moving = True
            self.player.animate = True
               
        elif event.key == pl.K_UP:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                self.player.direction = Directions.N
                self.player.moving = True
            self.player.animate = True

        elif event.key == pl.K_DOWN:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                self.player.direction = Directions.S
                self.player.moving = True
            self.player.animate = True

        elif event.key == pl.K_b:
            self.battle()

    def update_world(self):
        if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0 and self.player.moving:
            self.check_collision(self.player.direction, 3)
        elif self.cam_world_pos_x % 32 != 0:
            if self.player.direction == Directions.W:
                self.player.col_rect.move_ip(-2, 0)
                self.cam_world_pos_x -= 2
            elif self.player.direction == Directions.E:
                self.player.col_rect.move_ip(2, 0)
                self.cam_world_pos_x += 2

        elif self.cam_world_pos_y % 32 != 0:
            if self.player.direction == Directions.N:
                self.player.col_rect.move_ip(0, -2)
                self.cam_world_pos_y -= 2
            elif self.player.direction == Directions.S:
                self.player.col_rect.move_ip(0, 2)
                self.cam_world_pos_y += 2
        elif self.player.moving:
            self.player.animate = False

    def check_collision(self, facing, coll_layer):
        # find the tile location of the hero
        tile_x = int((self.player.col_rect.left) / TILE_SIZE)
        tile_y = int((self.player.col_rect.top) / TILE_SIZE)


        step_x = 0
        step_y = 0

        if facing == Directions.E:
            step_x = 2
            step_y = 0
        elif facing == Directions.N:
            step_x = 0
            step_y = -2
        elif facing == Directions.S:
            step_x = 0
            step_y = 2
        elif facing == Directions.W:
            step_x = -2
            step_y = 0

        # find the tiles around the hero and extract their rects for collision
        tile_rects = []
        layer_data = self.map.getLayerData(coll_layer)
        for diry in (-1, 0 , 1):
            for dirx in (-1, 0, 1):
                if self.map.getTileImage(tile_x + dirx, tile_y + diry, coll_layer) != 0: #I believe this is gid for meta collision
                    tile_rects.append(pygame.rect.Rect((tile_x + dirx) * TILE_SIZE, (tile_y + diry) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        if self.player.col_rect.move(step_x, 0).collidelist(tile_rects) > -1:
            step_x = 0

        if self.player.col_rect.move(0, step_y).collidelist(tile_rects) > -1:
            step_y = 0

        self.player.col_rect.move_ip(step_x, step_y)
        self.cam_world_pos_x += step_x
        self.cam_world_pos_y += step_y



    def battle(self):
        self.__class__ = battlefield.Battlefield
        self.initialize()

import battlefield
