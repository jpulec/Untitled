import pygame
import tiledtmxloader
import player_data
import context
from constants import *

class Overworld(context.Context):
    def __init__(self):
        super(Overworld, self).__init__()
        self.map = None
        self.renderer = None
        self.resources = None
        self.sprite_layers = None
        self.object_layers = None
        self.player = None
        self.input = False
        self.on_object = False
        self.event_wait = False
        self.cam_world_pos_x = 0
        self.cam_world_pos_y = 0
        self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        self.renderer = tiledtmxloader.helperspygame.RendererPygame()

    def load_map(self, mapName, x, y):
        self.map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(mapName)
        self.resources.load(self.map)

        # cam_offset is for scrolling
        cam_world_pos_x = x
        cam_world_pos_y = y

        # set initial cam position and size
        self.renderer.set_camera_position_and_size(self.cam_world_pos_x, self.cam_world_pos_y, SCREEN_WIDTH, SCREEN_HEIGHT, "topleft")

        # retrieve the layers
        self.sprite_layers = [layer for layer in tiledtmxloader.helperspygame.get_layers_from_map(self.resources) if not layer.is_object_group]
        self.object_layers = [layer for layer in tiledtmxloader.helperspygame.get_layers_from_map(self.resources) if layer.is_object_group]
        if self.player is None:
            self.player = Avatar("Miles")
            self.player.current_skin = "Miles_regular"
            self.player.draw()
            self.sprite_layers[1].add_sprite(self.player.sprite)
        surf = pygame.Surface(DISPLAY.screen.get_size())
        self.draw_world(surf)
        pygame.event.post(pygame.event.Event(TRANSITION, {"type":"fade", "background":surf}))
        pygame.event.post(pygame.event.Event(OVERWORLD))

    def draw(self):
        self.draw_world(DISPLAY.screen)

    def update(self):
        self.update_world()

    def handle_events(self, e):
        if e.key == K_ESCAPE:
            #TODO: implement whatever behavior I want here
            return
        #TODO: this movement needs some work, should really fix collisions and such
        if e.key == K_LEFT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player.facing == 14:
                    self.player.facing = 12
                self.input = True

        elif e.key == K_RIGHT:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player.facing == 6:
                    self.player.facing = 4
                self.input = True
               
        elif e.key == K_UP:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player.facing == 2:
                    self.player.facing = 0
                self.input = True

        elif e.key == K_DOWN:
            if self.cam_world_pos_x % 32 == 0 and self.cam_world_pos_y % 32 == 0:
                if not self.player.facing == 10:
                    self.player.facing = 8
                self.input = True

        elif e.key == K_RETURN:
            pass

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

class Avatar:
    def __init__(self, name):
        self.imrect = pygame.Rect(DISPLAY.screen_width / 2 - 16, DISPLAY.screen_height / 2 - 16, TILE_SIZE, TILE_SIZE * 2)
        self.rect = pygame.Rect(DISPLAY.screen_width / 2 - 16, DISPLAY.screen_height / 2 - 16 + 32, TILE_SIZE, TILE_SIZE)
        self.facing = 0
        self.current_skin = None
        self.image = None
        self.sprite = None
        

    def draw(self):
        src_rect = IM.sprite_rects[self.current_skin][self.facing + 1]
        self.image = IM.textures[self.current_skin][0]
        self.sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image, self.imrect, src_rect)

