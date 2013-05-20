import pygame
import pygame.locals as pl

class CEvent(object):
    def __init__(self):
        pass

    def on_exit(self):
        pass

    def on_user(self, event):
        pass

    def on_expose(self):
        pass

    def on_resize(self, event):
        pass

    def on_key_up(self, event):
        pass

    def on_key_down(self, event):
        pass

    def on_mouse_move(self, event):
        pass

    def on_event(self, event):
        if event.type == pl.QUIT:
            self.on_exit()

        elif event.type >= pl.USEREVENT:
            self.on_user(event)

        elif event.type == pl.VIDEOEXPOSE:
            self.on_expose()

        elif event.type == pl.VIDEORESIZE:
            self.on_resize(event)

        elif event.type == pl.KEYUP:
            self.on_key_up(event)

        elif event.type == pl.KEYDOWN:
            self.on_key_down(event)

        elif event.type == pl.MOUSEMOTION:
            self.on_mouse_move(event)
