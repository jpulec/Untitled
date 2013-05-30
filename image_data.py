import pygame,sys

class ImageData(object):
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
        
    def sprite_sheet(self, size, file, pos=(0,0), clip=(0,0)):

        #Initial Values
        len_sprt_x, len_sprt_y = size #sprite size
        sprt_rect_x, sprt_rect_y = pos #where to find first sprite on sheet

        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
        if clip == (0,0):
            clip = (sheet_rect.width, sheet_rect.height)
        sprites = []
        for i in xrange(0, clip[1], size[1]):#rows
            for i in xrange(0, clip[0], size[0]):#columns
                sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
                #print sprt_rect_x
                #print sprt_rect_y
                #print len_sprt_x
                #print len_sprt_y
                sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
                sprites.append(sprite)
                sprt_rect_x += len_sprt_x

            sprt_rect_y += len_sprt_y
            sprt_rect_x = 0
        return sprites

    def setup(self):
        self.textures["Miles_regular"] = self.sprite_sheet((32, 64), "images/characters/Miles/regular/Miles_regular.png") 
        #charskins = [("Miles", "regular")]      #TODO: change to file loading
        #for name, skin in charskins:
        #    self.load_texture(name+"_"+skin,"images/characters/" + name + "/" + skin + "/" + name + "_" + skin + ".png", -1)
        #    for y in range(0,4):
        #        for x in range(0,4):
        #            self.sprite_rects[name+"_"+skin].append(pygame.rect.Rect(x*32,y*64,32,64))
        self.textures["textbox"] = self.sprite_sheet((32, 32), "images/textbox.png")
        system = "system.png"
        #self.load_texture("system", "images/" + system, -1)
        #for y in range(0,4):
            #for x in range(0,4):
                #self.sprite_rects["system"].append(pygame.rect.Rect(x*32,y*32,32,32))
        
