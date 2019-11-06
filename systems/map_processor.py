import utils.esper as esper
from utils.noise_map import make_noise_map
from utils.layers import Layers
import itertools
from random import randint
from collections import defaultdict
from components.game_map import GameMap
from components.position import Position
from components.renderable import Renderable
from components.physics import Physics


class MapProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.current_map = None

    def process(self, *args, **kwargs):
        print('Map processor')
        player_position = self.world.component_for_entity(self.current_map.player, Position)
        self.add_new_chunks(player_position.x, player_position.y, self.current_map)
        self.get_entities_positions()

    def generate_chunk(self, x, y, game_map):
        size = game_map.chunk_size

        assert x % size == 0
        assert y % size == 0

        game_map.chunks.add((x, y))

        height_map, max_noise, min_noise = make_noise_map(x, y, size)

        for (j, k) in height_map:
            height_map[(j, k)] = (height_map[(j, k)] - min_noise) / (
                    max_noise - min_noise)
            terrain = self.world.create_entity()
            self.world.add_component(terrain, Position(j, k))
            self.world.add_component(terrain, Renderable('.',
                                                         color='dark yellow', layer=Layers.MAP))

            if height_map[(j, k)] < 0.3:
                water = self.world.create_entity()
                self.world.add_component(water, Position(j, k))
                self.world.add_component(water, Renderable('~',  color='blue',layer=Layers.MAP))
            elif height_map[(j, k)] < 0.7:
                if randint(0, 100) > 90:
                    tree = self.world.create_entity()
                    self.world.add_component(tree, Position(j, k))
                    self.world.add_component(tree, Physics(collidable=True))
                    self.world.add_component(tree, Renderable('*', color='green',layer=Layers.MAP))

            elif height_map[(j, k)] < 1:
                mountain = self.world.create_entity()
                self.world.add_component(mountain, Position(j, k))
                self.world.add_component(mountain, Physics(collidable=True))
                self.world.add_component(mountain, Renderable('^', color='grey',layer=Layers.MAP))

    def add_new_chunks(self, x, y, game_map):

        cx = (x // game_map.chunk_size) * game_map.chunk_size
        cy = (y // game_map.chunk_size) * game_map.chunk_size
        chunk_size = game_map.chunk_size

        for x, y in itertools.product([cx - chunk_size, cx, cx + chunk_size],
                                      [cy - chunk_size, cy, cy + chunk_size]):
            if (x, y) in game_map.chunks:
                continue
            self.generate_chunk(x, y, game_map)

    def get_current_map(self):
        for ent, game_map in self.world.get_component(GameMap):
            self.current_map = game_map

    def get_entities_positions(self):
        self.current_map.entities_positions = defaultdict(list)
        for ent, pos in self.world.get_component(Position):
            self.current_map.entities_positions[(pos.x, pos.y)].append(ent)
