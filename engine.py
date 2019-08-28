from bearlibterminal import terminal as blt
from utils.esper import World

from components.action import Action
from components.ai import Ai, NPC
from components.damager import Damager
from components.item import Item
from components.joystick import Joystick
from components.physics import Physics
from components.position import Position
from components.renderable import Renderable

from systems.action_processor import ActionProcessor
from systems.ai_processor import AiProcessor
from systems.event_system import EventSystem
from systems.input_processor import InputProcessor
from systems.physic_processor import PhysicProcessor
from systems.render_processor import RenderProcessor


def play_game():
    world = World()

    player = world.create_entity()
    world.add_component(player, Position(x=10, y=10))
    world.add_component(player, Joystick())
    world.add_component(player, Renderable(char='@', posx=10, posy=10, layer=2))
    world.add_component(player, Action())
    world.add_component(player, Damager())
    world.add_component(player, Physics(collidable=True))

    dagger = world.create_entity()
    world.add_component(dagger, Position(x=9, y=9))
    world.add_component(dagger, Item(coast=5, weight=4))
    world.add_component(dagger, Renderable(char='-', posx=9, posy=10, color='blue'))

    enemy = world.create_entity()
    world.add_component(enemy, Position(x=11, y=11))
    world.add_component(enemy, Renderable(char='x', posx=11, posy=11, color='red', layer=1))
    world.add_component(enemy, Ai(NPC()))
    world.add_component(enemy, Action())
    world.add_component(enemy, Damager())
    world.add_component(enemy, Physics(collidable=True))

    enemy = world.create_entity()
    world.add_component(enemy, Position(x=15, y=11))
    world.add_component(enemy, Renderable(char='x', posx=15, posy=11, color='green', layer=1))
    world.add_component(enemy, Ai(NPC()))
    world.add_component(enemy, Action())
    world.add_component(enemy, Damager())
    world.add_component(enemy, Physics(collidable=True))

    processors = [InputProcessor, AiProcessor, EventSystem, ActionProcessor, PhysicProcessor, RenderProcessor]

    for prior, processor in enumerate(processors):
        world.add_processor(processor(), priority=prior)
    world.get_processor(EventSystem).process()
    world.get_processor(RenderProcessor).process()
    blt.refresh()

    while True:

        world.process()


if __name__ == '__main__':
    blt.open()
    play_game()
    blt.close()
