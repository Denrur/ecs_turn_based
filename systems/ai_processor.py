from utils.esper import Processor
from components.ai import Ai
from components.action import Action
from components.joystick import Joystick
from components.position import Position
from components.physics import Physics
# from components.game_map import GameMap

from systems.map_processor import MapProcessor

from utils.decorators import benchmark
from utils.pathfinding.a_star_search import a_star_search
from utils.pathfinding.dijkstra import reconstruct_path


class AiProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self, *args, **kwargs):
        print(f'AI processor {self.world.timer=}')
        for ent, ai in self.world.get_component(Ai):
            self.ai_action(ent, ai_type=ai.ai_type)

    @benchmark
    def ai_action(self, ent, ai_type):
        action = self.world.component_for_entity(ent, Action)

        action.type, action.param, action.flag = self.take_turn(ent, ai_type)
        print(f'{ent.name=} prepare {action.type=}, {action.param=}, {action.flag=}, {action.cost=}')

    def take_turn(self, entity, ai_type):
        pos = self.world.component_for_entity(entity, Position)
        start = (pos.x, pos.y)
        map = self.world.get_processor(MapProcessor).current_map
        player = map.player
        pos = self.world.component_for_entity(player, Position)
        goal = self.get_free_cell_near_goal(pos, map)
        # goal = [(p.x, p.y) for ent, p in self.world.get_component(Position)
        #         if self.world.has_component(ent, Joystick)][0]
        print(f'{entity.name}, {goal=}, {pos.x=}, {pos.y=}')
        graph = ai_type.graph(self.world, pos.x, pos.y, 20)
        came_from, cost_so_far = a_star_search(graph, start, goal)
        coords = reconstruct_path(came_from, start, goal).pop(0)
        destination = (coords[0] - pos.x, coords[1] - pos.y)
        action_type = 'move'
        action_flag = True
        param = destination
        return action_type, param, action_flag

    def get_free_cell_near_goal(self, pos, map_):
        neighbours = [(-1, -1), (0, -1), (1, -1),
                      (-1, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)]
        x = pos.x
        y = pos.y
        for i in neighbours:
            if (x + i[0], y + i[1]) in map_.entities_positions:
                for entity in map_.entities_positions[(x + i[0], y + i[1])]:
                    if self.world.component_for_entity(entity, Physics).collidable:
                        pass

                    else:
                        return x + i[0], y + i[1]
        else:
            return i
