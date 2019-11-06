from utils.esper import Processor
from utils.pathfinding.a_star_search import a_star_search
from utils.pathfinding.a_star_search import reconstruct_path
from utils.decorators import benchmark

from systems.event_system import EventSystem
from components.action import Action
from components.ai import Ai
from components.damager import Damager
from components.inventory import Inventory
from components.item import Item
from components.position import Position
from components.physics import Physics
from components.renderable import Renderable

from systems.map_processor import MapProcessor


class ActionProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.current_entity = None
    @benchmark
    def process(self):
        print(f'Action Processor {self.world.timer=}'.center(100, '#'))
        scheduler = self.world.get_processor(EventSystem).turn_scheduler
        ent = scheduler.next_event()
        if self.world.has_component(ent, Ai):
            ai = self.world.component_for_entity(ent, Ai)
            self.ai_action(ent, ai.ai_type)

        pos = self.world.component_for_entity(ent, Position)

        action = self.world.component_for_entity(ent, Action)

        if action.type == 'move':
            phys = self.world.component_for_entity(ent, Physics)
            phys.x, phys.y = action.param
            phys.move = action.flag
        if action.type == 'attack':
            dmg = self.world.component_for_entity(ent, Damager)
            dmg.x, dmg.y = action.param
            dmg.attack = action.flag
        if action.type == 'pickup':
            items = [k for k, (p, i) in self.world.get_components(Position, Item)
                     if (p.x, p.y) == (pos.x, pos.y)]
            print(f'{items=}')
            if len(items) > 0:
                self.pickup_item(ent, items[0])
            else:
                print('Nothing to pick up')
        if action.type == 'drop_inventory':
            inventory = self.world.component_for_entity(ent, Inventory)
            if len(inventory.items) > 0:
                item = inventory.items[0]
                self.drop_item(ent, item)
                item_pos = self.world.component_for_entity(item, Position)
                print(f'Dropped {item.name=} in {item_pos.x=} {item_pos.y=}')
                print(f'Dropped {ent.name=} in {pos.x=} {pos.y=}')
            else:
                print('Nothing to drop')
        self.current_entity = ent
        print(f'{ent.name=}, {action.type=}')

    def pickup_item(self, entity, item):
        if self.world.has_component(item, Item):
            self.add_item(entity, item)
            self.world.remove_component(item, Position)
            self.world.remove_component(item, Renderable)

    def add_item(self, entity, item):
        inventory = self.world.component_for_entity(entity, Inventory)
        if len(inventory.items) >= inventory.capacity:
            print('Inventory is full')
        else:
            inventory.items.append(item)
        for ind, item in enumerate(inventory.items):
            print(f'{ind} {item.name}')

    def remove_item(self, entity, item):
        inventory = self.world.component_for_entity(entity, Inventory)
        inventory.items.remove(item)
        for ind, item in enumerate(inventory.items):
            print(f'{ind} {item.name}')

    def drop_item(self, entity, item):
        self.world.add_component(item, Position())
        item_pos = self.world.component_for_entity(item, Position)
        entity_pos = self.world.component_for_entity(entity, Position)

        item_pos.x = entity_pos.x
        item_pos.y = entity_pos.y

        self.remove_item(entity, item)

    def ai_action(self, ent, ai_type):
        action = self.world.component_for_entity(ent, Action)

        action.type, action.param, action.flag = self.take_turn(ent, ai_type)
        print(f'{ent.name=} prepare {action.type=}, {action.param=}, {action.flag=}, {action.cost=}')

    def take_turn(self, entity, ai_type):
        pos = self.world.component_for_entity(entity, Position)
        start = (pos.x, pos.y)

        map_ = self.world.get_processor(MapProcessor).current_map

        player = map_.player
        player_pos = self.world.component_for_entity(player, Position)

        goal = self.get_free_cell_near_goal(player_pos, map_)

        print(f'{entity.name}, {goal=}, {pos.x=}, {pos.y=}')

        graph = ai_type.graph(self.world, pos.x, pos.y, 20)
        came_from, cost_so_far = a_star_search(graph, start, goal)
        path = reconstruct_path(came_from, start, goal)
        print(f'{path=}')
        coords = path.pop(0)
        print(f'{coords=}')
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
                        return pos.x + i[0], pos.y + i[0]
        else:
            return pos.x + i[0], pos.y + i[0]
