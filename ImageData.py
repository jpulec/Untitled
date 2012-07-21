
import pygame,sys


class ImageData:
    def __init__(self):
        self.textures = dict()
        self.sprite_rects = dict()

    def load_texture(self, dictionary_entry, texture_filename, color_key = None):
        try:
            #completeName = os.path.join('images',textureFilename)
            if color_key == -1:
                texture = pygame.image.load(texture_filename)
                texture.set_colorkey(texture.get_at((0,0)))
                sheet_rect = texture.get_rect()
                self.textures[dictionary_entry] = [texture,sheet_rect]
                self.sprite_rects[dictionary_entry] = [sheet_rect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))
            else:
                texture = pygame.image.load(texture_filename)
                sheet_rect = texture.get_rect()
                self.textures[dictionary_entry] = [texture,sheet_rect]
                self.sprite_rects[dictionary_entry] = [sheet_rect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))    
        except:
            print "Failed to load texture file '%s'!"%texture_filename
            return

    def assign_texture(self, dictionary_entry, surface):
        sheet_rect = surface.get_rect()
        self.textures[dictionary_entry] = [surface,sheet_rect]
        self.sprite_rects[dictionary_entry] = [sheet_rect]

    def setup(self):
        charskins = [("Miles", "regular")]      #TODO: change to file loading
        for name, skin in charskins:
            self.load_texture(name+"_"+skin,"images/characters/" + name + "/" + skin + "/" + name + "_" + skin + ".png", -1)
            for y in range(0,4):
                for x in range(0,4):
                    self.sprite_rects[name+"_"+skin].append(pygame.rect.Rect(x*32,y*64,32,64))
