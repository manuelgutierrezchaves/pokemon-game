import random
import pandas as pd
df = pd.read_csv("damage_multiplier.csv")


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = random.randint(90, 110)
        self.hp = self.max_hp #Health points
        self.attack = random.randint(20, 40)
        self.alive = True

    def __str__(self):
        return self.name + ", HP: " + str(self.hp) + "/" + str(self.max_hp)

    def evolution(self): #Not in use
        self.max_hp *= 1.6 #Needs rounding
        self.hp = self.max_hp
        self.attack *= 1.6 #Needs rounding

    def feed(self, quantity):
        if self.alive:
            self.hp = self.max_hp if self.hp + quantity > self.max_hp else self.hp + quantity
            print(self.name + "'s HP is now: " + str(self.hp) + "/" + str(self.max_hp))
        else:
            print(self.name + "'s dead. Try reviving.")

    def death(self): 
        print(self.name + "  has died.")
        self.alive = False
        self.hp = 0

    def revive(self, quantity):
        if not self.alive:
            self.hp = self.max_hp if quantity > self.max_hp else quantity
            self.alive = True
            print(self.name + "'s HP is now: " + str(self.hp) + "/" + str(self.max_hp))
        else:
            print(self.name + "'s already alive.")

class battle():

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def attack(self, attacker):
        if attacker == 1: 
            multiplier = df[(df['Attacker']==self.pokemon1.type) & (df['Defender']==self.pokemon2.type)]['Multiplier'].values[0]
            damage = round(self.pokemon1.attack * multiplier)
            self.pokemon2.hp -= damage
            print(self.pokemon1.name + " hits " + self.pokemon2.name + " for " + str(damage) + " points.")
            if self.pokemon2.hp <= 0: self.pokemon2.death()
            
        if attacker == 2:
            multiplier = df[(df['Attacker']==self.pokemon2.type) & (df['Defender']==self.pokemon1.type)]['Multiplier'].values[0]
            damage = round(self.pokemon2.attack * multiplier)
            self.pokemon1.hp -= damage
            print(self.pokemon2.name + " hits " + self.pokemon1.name + " for " + str(damage) + " points.")
            if self.pokemon1.hp <= 0: self.pokemon1.death()
    
    def __str__(self):
        string = "Pokemon 1: " + str(self.pokemon1) + "\t Pokemon 2: " + str(self.pokemon2)
        return string
    
    def winner(self):
        print("The winner is " + self.pokemon1.name) if self.pokemon1.alive == True else print("The winner is " + self.pokemon2.name)

def battle_fun(pokemon1, pokemon2):
    if pokemon1.alive and pokemon2.alive:

        battle_instance = battle(pokemon1, pokemon2)
        i=1
        while pokemon1.alive and pokemon2.alive == True:
            print(battle_instance)
            battle_instance.attack((i%2)+1)
            i += 1
        battle_instance.winner()
    else:
        print("One or both Pokemons are dead.")

def main_menu(pokemon_owned):

    option = input("1 - New Pokemon\n2 - Fight \n3 - Feed\n4 - Revive\n5 - Exit menu\n\nEnter number: ")
    if option == "1": #Add new Pokemon
        name = input("Name: ")
        if next((pokemon_to_add for pokemon_to_add in pokemon_owned if pokemon_to_add.name == name), None) == None: #Check if name already in use
            pokemon_owned.append(pokemon(name))
            print("New pokemon added.")
        else:
            print("Name already in use.")

    elif option == "2": #Fighting
        name_to_find = input("Which Pokemon do you choose for the fight?: ")
        user_pokemon = next((pokemon_to_fight for pokemon_to_fight in pokemon_owned if pokemon_to_fight.name == name_to_find), None)
        enemy_pokemon = pokemon("Random")
        battle_fun(user_pokemon, enemy_pokemon)

    elif option == "3": #Feed Pokemon
        name_to_find = input("Which Pokemon do you want to feed?: ")
        user_pokemon = next((pokemon_to_feed for pokemon_to_feed in pokemon_owned if pokemon_to_feed.name == name_to_find), None)
        user_pokemon.feed(25)

    elif option == "4": #Revive Pokemon
        name_to_find = input("Which Pokemon do you want to revive?: ")
        user_pokemon = next((pokemon_to_revive for pokemon_to_revive in pokemon_owned if pokemon_to_revive.name == name_to_find), None)
        user_pokemon.revive(75)

    elif option == "5": #Exit
        global run
        run = False

    else:
        print("Try again...")

    return pokemon_owned


#-------------------Main-----------------------
# pokemon_owned = []
# run = True
# while run:
#     pokemon_owned = main_menu(pokemon_owned)
#     print([i.hp for i in pokemon_owned])

#-------------------Testing-----------------------
pok1 = pokemon("Nidalee")
pok2 = pokemon("Rengar")
print(pok1.type + str(pok1.attack))
print(pok2.type + str(pok2.attack))
battle_fun(pok1, pok2)