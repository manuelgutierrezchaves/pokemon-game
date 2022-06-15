import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 30
        self.alive = 1

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

class battle():

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def attack(self, attacker):
        if attacker == 1: 
            self.pokemon2.hp = self.pokemon2.hp - self.pokemon1.attack
            if self.pokemon2.hp <= 0: self.pokemon2.death()
        if attacker == 2:
            self.pokemon1.hp = self.pokemon1.hp - self.pokemon2.attack
            if self.pokemon1.hp <= 0: self.pokemon1.death()






#-------------------Testing-----------------------
poke1 = pokemon("Nidalee")
poke2 = pokemon("Rengar")
print(poke1)
print(poke2)
battle1 = battle(poke1, poke2)
battle1.attack(1)
battle1.attack(1)
battle1.attack(1)
battle1.attack(1)
battle1.attack(2)
print(poke1)
print(poke2)
