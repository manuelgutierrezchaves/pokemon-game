import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.hp = 100
        self.attack = 30

    def __str__(self):
        return self.name + ", Type: " + self.type + ", HP: " + str(round(self.hp))

    def evolution(self):
        self.hp = self.hp * 1.6
        self.attack = self.attack * 1.6

    






#-------------------Testing-----------------------
poke1 = pokemon("Nidalee")
print(poke1)
poke1.evolution()
print(poke1)