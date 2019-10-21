class Renderable:
    def __init__(self, char: str = '@', color='white', posx: int = 0, posy: int = 0, layer=None):
        self.x = posx
        self.y = posy
        self.char = char
        self.layer = layer
        self.color = color

