import random

character_descriptions = {
    'skeleton': '',
    'second_name': '',
    'yo momma': ''
}

room_description = {
    '', '', '', '', ''
}


class Room:
    def __init__(self):
        x = random.randint(0, 1)
        if x == 0:
            self.enemy = Character(random.randint(2, 8), random.randint(5, 10))
        else:
            self.enemy = Character(random.randint(6, 12), random.randint(10, 20))
        self.description = random.choice(room_description)


class Character:
    def __init__(self, health, damage, name=None):
        self.health = health
        self.damage = damage
        self.name = name if not None else random.choice(['skeleton', 'second_name', "yo momma"])
        self.description = character_descriptions[self.name]
        self.friendly = random.choice([True, False])

    def damage_character(self, amount):
        self.health -= amount
        return self.health

    def heal_character(self, amount):
        self.health += amount
        return self.health

    def is_friendly(self):
        return self.friendly

    def talk(self):
        return "Hello friend, I'm leaving now."
