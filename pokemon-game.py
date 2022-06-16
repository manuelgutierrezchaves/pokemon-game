import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 30
        self.alive = True

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
        self.alive = False

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
    
    def __str__(self):
        string = "Pokemon 1: " + str(self.pokemon1) + ", Pokemon 2: " + str(self.pokemon1)
        return string

def battle_fun(pokemon1, pokemon2):
    battle1 = battle(pokemon1, pokemon2)
    while pokemon1.alive and pokemon2.alive == True:
        battle1.attack(1)
        if pokemon2.hp <= 0: pokemon2.death()
        print(battle1)
        battle1.attack(2)
        if pokemon1.hp <= 0: pokemon1.death()
        print(battle1)






#-------------------Testing-----------------------
poke1 = pokemon("Nidalee")
poke2 = pokemon("Rengar")
battle1 = battle_fun(poke1, poke2)

