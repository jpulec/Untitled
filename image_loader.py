import pygame
import sys
import image_data


class ImageLoader(object):

    def __init__(self):
        self.textures = dict()
        self.sprite_rects = dict()

    def sprite_sheet(self, size, file, pos=(0, 0), clip=(0, 0)):

        # Initial Values
        len_sprt_x, len_sprt_y = size  # sprite size
        sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

        sheet = pygame.image.load(file).convert_alpha()  # Load the sheet
        sheet_rect = sheet.get_rect()
        if clip == (0, 0):
            clip = (sheet_rect.width, sheet_rect.height)
        sprites = []
        for i in xrange(0, clip[1], size[1]):  # rows
            for i in xrange(0, clip[0], size[0]):  # columns
                sheet.set_clip(
                    pygame.Rect(sprt_rect_x,
                                sprt_rect_y,
                                len_sprt_x,
                                len_sprt_y))  # find sprite you want
                #grab the sprite you want
                sprite = sheet.subsurface(sheet.get_clip())
                sprites.append(sprite)
                sprt_rect_x += len_sprt_x

            sprt_rect_y += len_sprt_y
            sprt_rect_x = 0
        return sprites

    def setup(self):
        for k, v in image_data.system.iteritems():
            self.textures[k] = self.sprite_sheet(**v)
        for k, v in image_data.characters.iteritems():
            self.textures[k] = self.sprite_sheet(**v)
