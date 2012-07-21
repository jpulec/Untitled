import pygame

class DisplayInfo:
    def __init__(self, width, height):
        pygame.init()
        self.screen_height = height
        self.screen_width = width
        self.is_fullscreen = 0 # changed for testing
        self.window = pygame.rect.Rect(0, 0, self.screen_width-1, self.screen_height-1)
        self.screen = None
        self.icon_surface = None
        pygame.mouse.set_visible(0) 

    def set_screen_size(self, sizeX, sizeY):
        self.screen_height = sizeY
        self.screen_width = sizeX
        self.check_window_size()

    def set_window(self, startX, startY, sizeX, sizeY):
        self.window = pygame.rect.Rect(startX, startY, (sizeX - startX)-1, (sizeY - startY)-1)
        self.check_window_size()
        

    def check_window_size(self):
        " Makes sure the window is fully inside the screen. "
        if (self.window.left < self.screen_width -1):
            self.window.left = 0
        if (self.window.top < self.screen_height -1):
            self.window.top = 0

        if (self.window.right >= self.screen_width):
            self.window.right = (self.screen_width - self.left) -1

        if (self.window.bottom >= self.screen_height):
            self.window.bottom = (self.screen_height - self.top)-1

        if (self.screen is not None):
            self.screen.set_clip(self.window)

    
    def create_screen(self):
        self.icon_surface = pygame.image.load("images/sword.gif")
        pygame.display.set_icon(self.icon_surface)
        
        self.screen = pygame.display.set_mode((self.screen_width,
                                                self.screen_height),
                                                (pygame.FULLSCREEN * self.is_fullscreen))
            
        self.screen.convert()
        pygame.display.set_caption("RPG!")
        self.check_window_size()
        self.display_initilized = 1
