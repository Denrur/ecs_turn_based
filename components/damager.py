class Damager:
    def __init__(self, attack_power: int = 1, attack_range: int = 1, attack_type: str = 'melee'):
        self.power = attack_power
        self.range = attack_range
        self.type = attack_type
        self.target = None
        self.attack = False
        self.cost = 2
