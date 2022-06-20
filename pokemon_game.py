import os
clear = lambda: os.system('clear')
import random
import pandas as pd
damage_df = pd.read_csv("damage_multiplier.csv")
moves_df = pd.read_csv("move_sets.csv")


class pokemon():

    def __init__(self, name):
        self.name = name
        self.type = random.choice(["Water", "Fire", "Grass"])
        self.max_hp = random.randint(300, 400)
        self.hp = self.max_hp #Health points
        self.attack = random.randint(90, 110)
        self.alive = True
        first_moves = moves_df.sample(2) # 2 random moves
        self.moves = [{"Name": first_moves["Name"].values[0], "Type": first_moves["Type"].values[0], "Power": first_moves["Power"].values[0]}, {"Name": first_moves["Name"].values[1], "Type": first_moves["Type"].values[1], "Power": first_moves["Power"].values[1]}]

    def __str__(self):
        return "{0.name}, HP: {0.hp}/{0.max_hp}".format(self)

    def evolution(self): #Not in use
        self.max_hp *= 1.6 #Needs rounding
        self.hp = self.max_hp
        self.attack *= 1.6 #Needs rounding

    def feed(self, quantity):
        if self.alive:
            self.hp = self.max_hp if self.hp + quantity > self.max_hp else self.hp + quantity
            print("{0.name} heals for {1}\n\n{0.name}'s HP is now: {0.hp}/{0.max_hp}".format(self, quantity))
            input("\nPress enter to continue.")
            clear()
        else:
            print("{0.name}'s dead. Try reviving.".format(self))
            input("\nPress enter to continue.")
            clear()

    def death(self): 
        print("{0.name} has died.".format(self))
        self.alive = False
        self.hp = 0
        input("\nPress enter to continue.")
        clear()

    def revive(self, quantity):
        if not self.alive:
            self.hp = self.max_hp if quantity > self.max_hp else quantity
            self.alive = True
            print("{0.name}'s HP is now: {0.hp}/{0.max_hp}".format(self))
            input("\nPress enter to continue.")
            clear()
        else:
            print("{0.name}'s already alive.".format(self))
            input("\nPress enter to continue.")
            clear()



class battle():

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def attack(self, attacker, move_name):
        if attacker == 1: 
            move_dict = next(item for item in self.pokemon1.moves if item["Name"] == move_name)
            move_dmg = move_dict.get("Power")
            move_type = move_dict.get("Type")
            multiplier = damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemon2.type)]['Multiplier'].values[0]
            damage = round(self.pokemon1.attack * multiplier * move_dmg / 100)
            self.pokemon2.hp -= damage
            if multiplier > 1: print("It's super effective.\n")
            if multiplier < 1: print("It's not very effective.\n")            
            print("{0.name} ({0.type}) hits {1.name} ({1.type}) with {2} ({4}) for {3} points.".format(self.pokemon1, self.pokemon2, move_name, damage, move_type))
            input("\nPress enter to continue.")
            clear()
            if self.pokemon2.hp <= 0: self.pokemon2.death()
            
        if attacker == 2:
            move_dict = next(item for item in self.pokemon2.moves if item["Name"] == move_name)
            move_dmg = move_dict.get("Power")
            move_type = move_dict.get("Type")            
            multiplier = damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemon1.type)]['Multiplier'].values[0]
            damage = round(self.pokemon2.attack * multiplier * move_dmg / 100)
            self.pokemon1.hp -= damage
            if multiplier > 1: print("It's super effective.\n")
            if multiplier < 1: print("It's not very effective.\n")
            print("{0.name} ({0.type}) hits {1.name} ({1.type}) with {2} ({4}) for {3} points.".format(self.pokemon2, self.pokemon1, move_name, damage, move_type))
            input("\nPress enter to continue.")
            clear()
            if self.pokemon1.hp <= 0: self.pokemon1.death()
    
    def __str__(self):
        string = "{0}\n{1}".format(self.pokemon1, self.pokemon2)

        return string
    
    def winner(self):
        print("The winner is " + self.pokemon1.name) if self.pokemon1.alive == True else print("The winner is " + self.pokemon2.name)
        input("\nPress enter to continue.")
        clear()



def battle_fun(pokemon1, pokemon2):
    run_battle = True
    if pokemon1.alive and pokemon2.alive:

        battle_instance = battle(pokemon1, pokemon2)

        i = 11
        while pokemon1.alive and pokemon2.alive and run_battle == True:
            if i%2 == 1:
                option = input("{0}\n\nBattle Menu\n\n1 - Attack\n2 - Feed\n3 - Exit battle\n\nEnter number: ".format(battle_instance))
                clear()
                if option == "1":
                    option_move_name = input("Choose move: (" + pokemon1.moves[0].get("Name") + "/" + pokemon1.moves[1].get("Name") + "): ")
                    clear()
                    if option_move_name in [pokemon1.moves[0].get("Name"), pokemon1.moves[1].get("Name")]:
                        battle_instance.attack(1, option_move_name)
                    else:
                        print("Choose a valid move.")
                        input("\nPress enter to continue.")
                        clear()
                        i -= 1
                
                elif option == "2":
                    pokemon1.feed(25)
                
                elif option == "3":
                    run_battle = False
                
                else:
                    print("Try again...")
                    input("\nPress enter to continue.")
                    clear()
                    i -= 1
            else:
                battle_instance.attack(2, pokemon2.moves[0].get("Name"))
            
            i += 1

        print("Battle finished.") if pokemon1.alive and pokemon2.alive == True else battle_instance.winner()

    else:
        print("One or both Pokemons are dead.")
        input("\nPress enter to continue.")
        clear()



def main_menu(pokemon_owned):

    clear()
    option = input("Main Menu\n\n1 - New Pokemon\n2 - View Pokemons\n3 - Fight \n4 - Feed\n5 - Revive\n6 - Exit menu\n\nEnter number: ")
    clear()
    if option == "1": #Add new Pokemon
        name = input("Name: ")
        clear()
        if next((pokemon_to_add for pokemon_to_add in pokemon_owned if pokemon_to_add.name == name), None) == None: #Check if name already in use
            new_pokemon = pokemon(name)
            pokemon_owned.append(new_pokemon)
            print("Name: {0.name}\nType: {0.type}\nAttack: {0.attack}\nHP: {0.hp}/{0.max_hp}".format(new_pokemon))
            input("\nPress enter to continue.")
            clear()
        else:
            print("Name already used.")
            input("\nPress enter to continue.")
            clear()

    elif option == "2": #Show pokemons
        for poke in pokemon_owned: print("{0.name}\t\tType: {0.type}\tAttack: {0.attack}\tHP: {0.hp}/{0.max_hp}\tMoves: {1} & {2}".format(poke, poke.moves[0].get("Name"), poke.moves[1].get("Name")))
        input("\nPress enter to continue.")
        clear()

    elif option == "3": #Fighting
        name_to_find = input("Which Pokemon do you choose for the fight?: ")
        clear()
        user_pokemon = next((pokemon_to_fight for pokemon_to_fight in pokemon_owned if pokemon_to_fight.name == name_to_find), None)
        battle_fun(user_pokemon, pokemon("Random Pokemon"))

    elif option == "4": #Feed Pokemon
        name_to_find = input("Which Pokemon do you want to feed?: ")
        clear()
        user_pokemon = next((pokemon_to_feed for pokemon_to_feed in pokemon_owned if pokemon_to_feed.name == name_to_find), None)
        user_pokemon.feed(25)

    elif option == "5": #Revive Pokemon
        name_to_find = input("Which Pokemon do you want to revive?: ")
        clear()
        user_pokemon = next((pokemon_to_revive for pokemon_to_revive in pokemon_owned if pokemon_to_revive.name == name_to_find), None)
        user_pokemon.revive(75)

    elif option == "6": #Exit
        global run
        run = False

    else:
        print("Try again...")

    return pokemon_owned


#-------------------Main-----------------------
first_poke = input("Choose a name for your first Pokemon: ")
clear()
pokemon_owned = [pokemon(first_poke)]

run = True
while run:
    pokemon_owned = main_menu(pokemon_owned)
    print("\n\n")
#----------------------------------------------



#-------------------Testing-----------------------
# pok1 = pokemon("Nidalee")
# pok2 = pokemon("Rengar")
# pok1.hp = 20
# pok2.hp = 0
# pok2.death()
# pok2.revive(100)
# pok1.revive(100)
# battle_fun(pok1, pok2)