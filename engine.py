from bearlibterminal import terminal as blt
from utils.esper import World
from utils.layers import Layers

from components.action import Action
from components.ai import Ai, NPC
from components.damager import Damager
from components.condition import Condition
from components.item import Item
from components.inventory import Inventory
from components.game_map import GameMap
from components.joystick import Joystick
from components.health import Health
from components.physics import Physics
from components.position import Position
from components.renderable import Renderable
from components.camera import Camera

from systems.action_processor import ActionProcessor
from systems.ai_processor import AiProcessor
from systems.condition_process import ConditionProcessor
from systems.event_system import EventSystem
from systems.input_processor import InputProcessor
from systems.map_processor import MapProcessor
from systems.physic_processor import PhysicProcessor
from systems.render_processor import RenderProcessor
from systems.camera_processor import CameraProcessor


def play_game():
    world = World()

    player = world.create_entity(Renderable(char='@', layer=Layers.ENTITIES),
                                 Position(x=10, y=10),
                                 Action(cost=1),
                                 Camera(width=20, height=20),
                                 Damager(attack_power=100),
                                 Physics(collidable=True),
                                 Inventory(26),
                                 Health(),
                                 Joystick(),
                                 Condition(),
                                 name='Player'
                                 )

    world.create_entity(GameMap(player=player))

    world.create_entity(Item(coast=5, weight=4),
                        Position(x=1, y=10),
                        Renderable(char='-',  color='blue', layer=Layers.ITEMS),
                        name='Dagger')

    world.create_entity(Renderable(char='s', color='red', layer=Layers.ENTITIES),
                        Position(x=19, y=10),
                        Action(cost=3),
                        Physics(collidable=True),
                        Damager(),
                        Health(),
                        Condition(),
                        Ai(NPC()),
                        name='Worm')

    world.create_entity(Renderable(char='g', color='green', layer=Layers.ENTITIES),
                        Position(x=2, y=10),
                        Action(cost=2),
                        Physics(collidable=True),
                        Damager(),
                        Health(),
                        Condition(),
                        Ai(NPC()),
                        name='Goblin')

    processors = [InputProcessor, MapProcessor, AiProcessor, ActionProcessor, PhysicProcessor, ConditionProcessor,
                  EventSystem, CameraProcessor, RenderProcessor]

    for prior, processor in enumerate(processors):
        world.add_processor(processor(), priority=prior)

    world.get_processor(MapProcessor).get_current_map()
    world.get_processor(MapProcessor).process()
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
