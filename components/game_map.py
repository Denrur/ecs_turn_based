from collections import defaultdict


class GameMap:
    def __init__(self, width=0, height=0, chunk_size=50, player=None):
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.chunks = set()
        self.player = player
        self.entities_positions = defaultdict(list)
