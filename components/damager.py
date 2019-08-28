class Damager:
    def __init__(self, attack_power=1, attack_range=1, attack_type='melee'):
        self.power = attack_power
        self.range = attack_range
        self.type = attack_type
        self.target = None
        self.attack = False
        self.cost = 2
