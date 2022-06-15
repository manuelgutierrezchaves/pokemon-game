import random


class pokemon():

    names_used = []

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 30
        self.name_validation()
        self.alive = 1

    def name_validation(self):
        if self.name not in self.names_used:
            self.names_used.append(self.name)
        else:
            print("Name already in use")
            del self

    def __str__(self):
        return self.name + ", Type: " + self.type + ", HP: " + str(round(self.hp))

    def evolution(self):
        self.max_hp = self.max_hp * 1.6
        self.hp = self.max_hp
        self.attack = self.attack * 1.6

    def cure(self, quantity):
        self.hp = self.max_hp if self.hp + quantity > self.max_hp else self.hp + quantity           

    def death(self): 
        print(self.name + "  has died.")
        self.alive = 0


#-------------------Testing-----------------------
poke = pokemon("Nidalee")
poke2 = pokemon("Nidalee")
print(poke)
print(poke2)
