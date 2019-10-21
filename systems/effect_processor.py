from utils.esper import Processor
from components.effects import Effects
from components.ai import Ai
from components.action import Action
from components.renderable import Renderable
from components.physics import Physics
from systems.event_system import EventSystem
from utils.layers import Layers


class EffectProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print(f'EffectsProcessor {self.world.timer=}')
        for ent, effects in self.world.get_component(Effects):
            active_effects = self.proceed(ent, effects.effects)
            if 'death' in active_effects:
                print(f'{ent.name=} dead')
                for component in (Ai, Action):
                    if self.world.has_component(ent, component):
                        self.world.remove_component(ent, component)
                if ent in self.world.get_processor(EventSystem).turn_scheduler.keys():
                    self.world.get_processor(EventSystem).turn_scheduler.cancel_event(ent)

                rend = self.world.component_for_entity(ent, Renderable)

                rend.char = 'x'
                rend.layer = Layers.CORPSES
                phys = self.world.component_for_entity(ent, Physics)
                phys.collidable = False

    def add_effect(self, entity, effect, duration=-1, power=None):
        effects = self.world.component_for_entity(entity, Effects)
        if effect not in effects.effects:
            effects.effects[effect] = [duration, power]

    def remove_effect(self, entity, effect):
        effects = self.world.component_for_entity(entity, Effects)
        if effects.effects[effect]:
            del effects.effects[effect]

    def proceed(self, entity, effects):
        for effect in effects:
            if effects[effect][0] > 0:
                effects[effect][0] -= 1
                if effects[effect][0] == 0:
                    self.remove_effect(entity, effect)
        return effects.keys()


