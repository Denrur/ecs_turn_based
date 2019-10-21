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
from components.camera import Camera

from systems.action_processor import ActionProcessor
from systems.ai_processor import AiProcessor
from systems.event_system import EventSystem
from systems.input_processor import InputProcessor
from systems.physic_processor import PhysicProcessor
from systems.render_processor import RenderProcessor
from systems.camera_processor import CameraProcessor


def play_game():
    world = World()

    player = world.create_entity()
    player.name = 'Player'
    world.add_component(player, Position(x=10, y=10))
    world.add_component(player, Camera(width=20, height=20))

    world.add_component(player, Joystick())
    world.add_component(player, Renderable(char='@', layer=2))
    world.add_component(player, Action(cost=1))
    world.add_component(player, Damager())
    world.add_component(player, Physics(collidable=True))

    dagger = world.create_entity()
    dagger.name = 'Dagger'
    world.add_component(dagger, Position(x=1, y=10))
    world.add_component(dagger, Item(coast=5, weight=4))
    world.add_component(dagger, Renderable(char='-', posx=9, posy=10, color='blue'))

    enemy = world.create_entity()
    enemy.name = 'Worm'
    world.add_component(enemy, Position(x=19, y=10))
    world.add_component(enemy, Renderable(char='s', posx=19, posy=10, color='red', layer=1))
    world.add_component(enemy, Ai(NPC()))
    world.add_component(enemy, Action(cost=3))
    world.add_component(enemy, Damager())
    world.add_component(enemy, Physics(collidable=True))

    enemy = world.create_entity()
    enemy.name = 'Goblin'
    world.add_component(enemy, Position(x=2, y=10))
    world.add_component(enemy, Renderable(char='g', posx=2, posy=10, color='green', layer=1))
    world.add_component(enemy, Ai(NPC()))
    world.add_component(enemy, Action(cost=4))
    world.add_component(enemy, Damager())
    world.add_component(enemy, Physics(collidable=True))

    processors = [InputProcessor, AiProcessor, ActionProcessor, PhysicProcessor,
                  EventSystem, CameraProcessor, RenderProcessor]

    for prior, processor in enumerate(processors):
        world.add_processor(processor(), priority=prior)
    world.get_processor(CameraProcessor).get_camera()
    world.get_processor(CameraProcessor).process()
    world.get_processor(EventSystem).process()
    world.get_processor(RenderProcessor).process()
    blt.refresh()

    while True:
        world.process()


if __name__ == '__main__':
    blt.open()
    play_game()
    blt.close()
