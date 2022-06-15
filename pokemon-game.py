import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.hp = 100
        self.attack = 30

    def __str__(self):
        text = self.name + " " + self.hp
        return text



