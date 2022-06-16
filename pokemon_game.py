import random


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = random.randint(90, 110)
        self.hp = self.max_hp #Health points
        self.attack = random.randint(20, 40)
        self.alive = True

    def __str__(self):
        return self.name + ", Type: " + self.type + ", HP: " + str(round(self.hp))

    def evolution(self):
        self.max_hp *= 1.6
        self.hp = self.max_hp
        self.attack *= 1.6

    def feed(self, quantity):
        self.hp = self.max_hp if self.hp + quantity > self.max_hp else self.hp + quantity           

    def death(self): 
        print(self.name + "  has died.")
        self.alive = False
        self.hp = 0

    def revive(self, quantity):
        self.hp = self.max_hp if quantity > self.max_hp else quantity
        self.alive = True

class battle():

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def attack(self, attacker):
        if attacker == 1: 
            self.pokemon2.hp -= self.pokemon1.attack
            print(self.pokemon1.name + " hits " + self.pokemon2.name + " for " + str(self.pokemon1.attack) + " points.")
            if self.pokemon2.hp <= 0: self.pokemon2.death()
            
        if attacker == 2:
            self.pokemon1.hp -= self.pokemon2.attack
            print(self.pokemon2.name + " hits " + self.pokemon1.name + " for " + str(self.pokemon2.attack) + " points.")
            if self.pokemon1.hp <= 0: self.pokemon1.death()
    
    def __str__(self):
        string = "Pokemon 1: " + str(self.pokemon1) + "\t Pokemon 2: " + str(self.pokemon2)
        return string
    
    def winner(self):
        print("The winner is " + self.pokemon1.name) if self.pokemon1.alive == True else print("The winner is " + self.pokemon2.name)

def battle_fun(pokemon1, pokemon2):
    battle_instance = battle(pokemon1, pokemon2)
    i=1
    while pokemon1.alive and pokemon2.alive == True:
        print(battle_instance)
        battle_instance.attack((i%2)+1)
        i += 1
    battle_instance.winner()







#-------------------Testing-----------------------
# poke1 = pokemon("Nidalee")
# poke2 = pokemon("Rengar")
# battle_instance = battle_fun(poke1, poke2)

poke1 = pokemon("Nidalee")
print(poke1)
poke1.death()
print(poke1)
poke1.revive(200)
print(poke1)