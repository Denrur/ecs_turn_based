class Physics:
    def __init__(self, movx=0, movy=0, collidable=False):
        self.x = movx
        self.y = movy
        self.move = False
        self.movement_cost = 3
        self.collidable = collidable
