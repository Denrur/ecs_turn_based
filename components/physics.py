class Physics:
    def __init__(self, movx: int = 0, movy: int = 0, collidable: bool = False):
        self.x: int = movx
        self.y: int = movy
        self.move: bool = False
        self.movement_cost: int = 3
        self.collidable = collidable
