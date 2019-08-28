from math import sqrt
from utils.pathfinding.a_star_search import a_star_search
from utils.pathfinding.dijkstra import reconstruct_path
from utils.pathfinding.graph import GridWithWeights
from components.joystick import Joystick
from components.position import Position


class Ai:
    def __init__(self, ai_type):
        self.ai_type = ai_type


class NPC:
    def __init__(self):
        self.name = 'NPC'
        self.graph = GridWithWeights

    def take_turn(self, world=None, pos=None):
        start = (pos.x, pos.y)
        goal = [(p.x, p.y) for ent, p in world.get_component(Position) if world.has_component(ent, Joystick)][0]

        if sqrt((pos.x - goal[0]) ** 2 + (pos.y - goal[1]) ** 2) < 1.5:
            action_type = 'attack'
            action_flag = True
            param = (goal[0] - pos.x, goal[1] - pos.y)
            cost = 3

        else:
            graph = self.graph(world, pos.x, pos.y, 20)
            came_from, cost_so_far = a_star_search(graph, start, goal)
            path = reconstruct_path(came_from, start, goal)
            coords = path.pop(0)
            destination = (coords[0] - pos.x, coords[1] - pos.y)
            action_type = 'move'
            action_flag = True
            param = destination
            cost = 3
        return action_type, param, action_flag, cost
