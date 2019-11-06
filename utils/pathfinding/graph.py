from components.position import Position
from components.physics import Physics

from utils.decorators import benchmark


class GridWithWeights:
    def __init__(self, world, _x, _y, size):
        self.world = world
        self.size = size
        self.x = _x
        self.y = _y
        self.weights = dict()
        self.obstacle = [(pos.x, pos.y) for ent, pos in self.world.get_component(Position) if
                         self.world.component_for_entity(ent, Physics).collidable]
        self.edges = self.make_graph(self.obstacle, _x, _y, size)

    @benchmark
    def make_graph(self, obstacle, _x, _y, size):
        edges = dict()
        for x in range(_x - size, _x + size):
            for y in range(_y - size, _y + size):
                if (x, y) not in obstacle:
                    edges[(x, y)] = self.neighbors((x, y))

        return edges

    def in_bounds(self, loc):
        (x, y) = loc
        return self.x - self.size <= x <= self.x + self.size and self.y - self.size <= y <= self.y + self.size

    def passable(self, loc):
        return loc not in self.obstacle

    # @benchmark
    def neighbors(self, loc):
        (x, y) = loc
        neighbors = list()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbors.append((x + i, y + j))
                if abs(i) == abs(j):
                    self.weights[(x + i, y + j)] = 1.41
                else:
                    self.weights[(x + i, y + j)] = 1

        neighbors = list(filter(self.in_bounds, neighbors))
        neighbors = list(filter(self.passable, neighbors))
        return neighbors

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

    def rescan_map(self):
        self.obstacle = [(pos.x, pos.y) for ent, pos in self.world.get_component(Position) if
                         self.world.component_for_entity(ent, Physics).collidable]

