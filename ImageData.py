
import pygame,sys


class ImageData:
    def __init__(self):
        self.textures = dict()
        self.spriteRects = dict()
        self.setup()
    

    def loadTexture(self, dictionaryEntry, textureFilename, colorKey = None):
        try:
            #completeName = os.path.join('images',textureFilename)
            if colorKey == -1:
                texture = pygame.image.load(textureFilename)
                texture = pygame.transform.scale2x(texture)
                texture.set_colorkey(texture.get_at((0,0)))
                sheetRect = texture.get_rect()
                self.textures[dictionaryEntry] = [texture,sheetRect]
                self.spriteRects[dictionaryEntry] = [sheetRect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))
            else:
                texture = pygame.image.load(textureFilename)
                sheetRect = texture.get_rect()
                self.textures[dictionaryEntry] = [texture,sheetRect]
                self.spriteRects[dictionaryEntry] = [sheetRect]  # Sprite 0 = whole page
                #print "Successfully loaded texture file '%s' (%s)."%(textureFilename,str(sheetRect))    
        except:
            print "Failed to load texture file '%s'!"%textureFilename
            return

    def assignTexture(self, dictionaryEntry, surface):
        sheetRect = surface.get_rect()
        self.textures[dictionaryEntry] = [surface,sheetRect]
        self.spriteRects[dictionaryEntry] = [sheetRect]

    def setup(self):
        charskins = [("Miles", "regular")]      #TODO: change to file loading
        for name, skin in charskins:
            self.loadTexture(name+"_"+skin,"images/characters/" + name + "/" + skin + "/" + name + "_" + skin + ".png", -1)
            for y in range(0,4):
                for x in range(0,3):
                    self.spriteRects[name+"_"+skin].append(pygame.rect.Rect(x*32,y*64,32,64))
