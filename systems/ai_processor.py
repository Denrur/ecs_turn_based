from utils.esper import Processor
from components.ai import Ai
from components.action import Action
from components.position import Position


class AiProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self, *args, **kwargs):
        print('Ai processor')
        for ent, ai in self.world.get_component(Ai):
            self.ai_action(ent, ai_type=ai.ai_type)

    def ai_action(self, ent, ai_type):
        pos = self.world.component_for_entity(ent, Position)
        action = self.world.component_for_entity(ent, Action)
        world = self.world
        action.type, action.param, action.flag, action.cost = ai_type.take_turn(world=world, pos=pos)

