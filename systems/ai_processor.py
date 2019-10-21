from utils.esper import Processor
from components.ai import Ai
from components.action import Action
from components.joystick import Joystick
from components.position import Position


from utils.pathfinding.a_star_search import a_star_search
from utils.pathfinding.dijkstra import reconstruct_path


class AiProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self, *args, **kwargs):
        print(f'AI processor {self.world.timer=}')
        for ent, ai in self.world.get_component(Ai):
            self.ai_action(ent, ai_type=ai.ai_type)

    def ai_action(self, ent, ai_type):
        action = self.world.component_for_entity(ent, Action)

        action.type, action.param, action.flag = self.take_turn(ent, ai_type)
        print(f'{ent.name=} prepare {action.type=}, {action.param=}, {action.flag=}, {action.cost=}')

    def take_turn(self, entity, ai_type):
        pos = self.world.component_for_entity(entity, Position)
        start = (pos.x, pos.y)
        goal = [(p.x, p.y) for ent, p in self.world.get_component(Position)
                if self.world.has_component(ent, Joystick)][0]

        graph = ai_type.graph(self.world, pos.x, pos.y, 20)
        came_from, cost_so_far = a_star_search(graph, start, goal)
        coords = reconstruct_path(came_from, start, goal).pop(0)
        destination = (coords[0] - pos.x, coords[1] - pos.y)
        action_type = 'move'
        action_flag = True
        param = destination
        return action_type, param, action_flag
