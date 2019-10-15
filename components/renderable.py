class Renderable:
    def __init__(self, char: str, posx: int = 0, posy: int = 0, color: str = 'white', layer: int = 0):
        self.char = char
        self.x = posx
        self.y = posy
        self.color = color
        self.layer = layer

