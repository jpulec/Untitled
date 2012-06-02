

class WindowContext:

    def __init__(self):
        pass

    def draw(self):
        print "Using generic windowContext draw"

    def update(self):
        print "Using generic windowContext update"

    def handleEvents(self, event):
        print "Using generic windowContext handleEvents for event:" + str(event)
