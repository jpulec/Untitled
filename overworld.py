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
    def __init__(self, map_name):
        super(Overworld, self).__init__()
        self.map = pytmx.tmxloader.load_pygame(map_name, pixelalpha=True)
        self.player = sprite_bases.Avatar("Miles_regular") 
        self.cam_world_pos_x = 0
        self.cam_world_pos_y = 0
        self.sprites = utils.SourceRectGroup()
        self.sprites.add(self.player)

    def render(self, surface):

        tw = self.map.tilewidth
        th = self.map.tileheight
        gt = self.map.getTileImage
        for l in xrange(0, len(self.map.tilelayers)):
            if self.map.tilelayers[l].name != "Collision":
                for y in xrange(0, self.map.height):
                    for x in xrange(0, self.map.width):
                        tile = gt(x, y, l)
                        if tile:
                            surface.blit(tile, (x*tw, y*th))
        self.sprites.update(pygame.time.get_ticks())
        self.sprites.draw(surface)

    def update(self):
        self.update_world()

    def on_exit(self):
        #TODO: Probably need to handle this more gracefully
        sys.exit(0)

    def on_key_down(self, event):
        if event.key == pl.K_LEFT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player._frame == 14:
                    self.player._frame = 12

        elif event.key == pl.K_RIGHT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player._frame == 6:
                    self.player._frame = 4
               
        elif event.key == pl.K_UP:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player._frame == 2:
                    self.player._frame = 0

        elif event.key == pl.K_DOWN:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player._frame == 10:
                    self.player._frame = 8

    def update_world(self):
        if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0 and not self.on_object:
            self.check_object(self.object_layers[0])
        if self.input:
            self.check_collision(self.player.facing, self.sprite_layers[3])
            self.input = False
            self.on_object = False
        elif self.cam_world_pos_x % 32 is not 0:
            if self.player.facing > 11:
                if self.cam_world_pos_x % 16 == 0:
                    self.player.facing += 1
                self.player.rect.move_ip(-2, 0)
                self.player.imrect.move_ip(-2, 0)
                self.cam_world_pos_x -= 2
            elif self.player.facing > 3:
                if self.cam_world_pos_x % 16 == 0:
                    self.player.facing += 1
                self.player.rect.move_ip(2, 0)
                self.player.imrect.move_ip(2, 0)
                self.cam_world_pos_x += 2

        elif self.cam_world_pos_y % 32 is not 0:
            if self.player.facing < 4:
                if self.cam_world_pos_y % 16 == 0:
                    self.player.facing += 1
                self.player.rect.move_ip(0, -2)
                self.player.imrect.move_ip(0, -2)
                self.cam_world_pos_y -= 2
            elif self.player.facing > 7:
                if self.cam_world_pos_y % 16 == 0:
                    self.player.facing += 1
                self.player.rect.move_ip(0, 2)
                self.player.imrect.move_ip(0, 2)
                self.cam_world_pos_y += 2
        elif self.player.facing % 4 == 1:
            self.player.facing +=1
        elif self.player.facing % 4 == 3:
            self.player.facing -= 3

    def check_collision(self, facing, coll_layer):
        if facing %2 != 0:
            return
        '''if facing % 4 != 0 or not self.cam_world_pos_x % 32 == 0 or not self.cam_world_pos_y % 32 == 0:
            return self.cam_world_pos_x, self.cam_world_pos_y'''

        # find the tile location of the hero
        tile_x = int((self.player.rect.left) / coll_layer.tilewidth)
        tile_y = int((self.player.rect.top) / coll_layer.tileheight)

        step_x = 0
        step_y = 0

        if facing == 4 or facing == 6:
            step_x = 2
            step_y = 0
        elif facing == 0 or facing == 2:
            step_x = 0
            step_y = -2
        elif facing == 8 or facing == 10:
            step_x = 0
            step_y = 2
        elif facing == 12 or facing == 14:
            step_x = -2
            step_y = 0

        # find the tiles around the hero and extract their rects for collision
        tile_rects = []
        for diry in (-1, 0 , 1):
            for dirx in (-1, 0, 1):
                if coll_layer.content2D[tile_y + diry][tile_x + dirx] is not None:
                    tile_rects.append(coll_layer.content2D[tile_y + diry][tile_x + dirx].rect)

        if self.player.rect.move(step_x, 0).collidelist(tile_rects) > -1:
            step_x = 0

        if self.player.rect.move(0, step_y).collidelist(tile_rects) > -1:
            step_y = 0

        self.player.rect.move_ip(step_x, step_y)
        self.player.imrect.move_ip(step_x, step_y)
        self.cam_world_pos_x += step_x
        self.cam_world_pos_y += step_y
    
    def check_object(self, object_layer):
        tile_x = int((self.player.rect.left) / TILE_SIZE)#object_layer.tilewidth)
        tile_y = int((self.player.rect.top) / TILE_SIZE)#object_layer.tileheight)
        if object_layer.objects is not None:
            objects = [x for x in object_layer.objects if ((x.x / TILE_SIZE) == tile_x) and ((x.y / TILE_SIZE) == tile_y)]
            if len(objects) == 0:
                self.on_object = False
            else:
                self.on_object = True
            for obj in objects:
                if obj.properties.has_key("portal"):
                    #try
                    #self.load_map("maps/" + obj.properties["portal"] + ".tmx", int(obj.properties["x"])*TILE_SIZE, int(obj.properties["y"])*TILE_SIZE)
                    pygame.event.post(pygame.event.Event(TRANSITION, {"type":"fade", "background":pygame.Surface(DISPLAY.screen.get_size())}))
                    pygame.event.post(pygame.event.Event(LOAD_MAP, {"map":obj.properties["portal"], "x":int(obj.properties["x"])*TILE_SIZE, "y":int(obj.properties["y"])*TILE_SIZE}))
                    #except Exception
                    #    pass
            #print str(objects)
            #if object_layer.content2D[tile_y][tile_x].

    def draw_world(self, screen):
        DISPLAY.screen.fill((0, 0, 0))
        self.sprite_layers[1].remove_sprite(self.player.sprite)
        self.player.draw()
        #print str(self.cam_world_pos_x)
        self.sprite_layers[1].add_sprite(self.player.sprite)
        self.draw_map(screen)

    def draw_map(self, screen):
        # adjust camera to position according to the keypresses
        self.renderer.set_camera_position(self.cam_world_pos_x, self.cam_world_pos_y, "topleft")
        # render the map
        for sprite_layer in self.sprite_layers:
            self.renderer.render_layer(screen, sprite_layer)
