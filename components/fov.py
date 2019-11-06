class Fov:
    def __init__(self, radius=10, color='yellow'):
        self.radius = radius
        self.cells = None
        self.color = color
        self.recalc_fov = True
