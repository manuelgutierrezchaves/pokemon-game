import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 30

    def __str__(self):
        return self.name + ", Type: " + self.type + ", HP: " + str(round(self.hp))

    def evolution(self):
        self.max_hp = self.max_hp * 1.6
        self.hp = self.max_hp
        self.attack = self.attack * 1.6

    def cure(self, cantidad):
        self.hp = self.max_hp if self.hp + cantidad > self.max_hp else self.hp + cantidad           



#-------------------Testing-----------------------
poke = pokemon("Nidalee")
poke.cure(100)
print(poke)