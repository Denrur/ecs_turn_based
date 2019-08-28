from utils.esper import Processor
from components.renderable import Renderable
from systems.action_processor import ActionProcessor
from bearlibterminal import terminal as blt


class RenderProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.fps = 4
        pass

    def process(self, *args, **kwargs):
        blt.clear()
        # try:
        #     entities_order = self.world.get_processor(ActionProcessor).entities_order
        #     for ent in entities_order:
        #         rend = self.world.component_for_entity(ent, Renderable)
        #     # for ent, rend in self.world.get_component(Renderable):
        #         blt.color(rend.color)
        #         blt.layer(rend.layer)
        #         blt.put(rend.x, rend.y, rend.char)
        #         blt.color('white')
        #         blt.layer(0)
        #
        #         blt.refresh()
        #         blt.delay(1000 // self.fps)
        # except TypeError:
        for ent, rend in self.world.get_component(Renderable):
            blt.color(rend.color)
            blt.layer(rend.layer)
            blt.put(rend.x, rend.y, rend.char)
            blt.color('white')
            blt.layer(0)

        blt.refresh()
