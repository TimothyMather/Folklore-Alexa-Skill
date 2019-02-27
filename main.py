import random

character_descriptions = {
    'skeleton': 'goes doot doot',
    'giant spider': 'has long legs and many eyes',
    'masked bandit': 'is up to no good',
    'goblin': 'is loud and smells musty',
    'skeleton': 'wants your calcium',
    'giant rat': 'is probably the ugliest thing I have ever seen'
    'dwarf': 'is loud and looks angry'
}

room_description = [
    'torchlit room with stone walls and broken furniture',
    'spiraling wooden staircase with some steps missing',
    'old treasure room thats been emptied long ago',
    'long hallway filled with cobwebs',
    'heavily crowded chuckie cheese restaurant with tons of screaming kids'
]


class Room:
    def __init__(self, enemies):
        self.description = random.choice(room_description)
        self.enemies = enemies

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Character:
    def __init__(self, health=3, damage=3, name=None):
        self.health = health
        self.damage = damage
        self.name = random.choice(list(character_descriptions.keys()))
        self.description = character_descriptions[
            self.name] if self.name in character_descriptions else ' bit of a butt'
        self.friendly = random.choice([True, False])

    def damage_character(self, amount):
        self.health -= amount

    def heal_character(self, amount):
        self.health += amount
        return self.health

    def is_friendly(self):
        return self.friendly

    def talk(self):
        return "Hello friend, I'm just passing through."

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
