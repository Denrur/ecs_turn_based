class Camera:
    def __init__(self, width=50, height=50, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.lock = True
