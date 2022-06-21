import os

from numpy import empty
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
import random
import pandas as pd
damage_df = pd.read_csv("damage_multiplier.csv")
moves_df = pd.read_csv("move_sets.csv")
pokemon_df = pd.read_csv("pokemon_data.csv")


class character():

    def __init__(self, name):
        self.name = name
        self.pokemon_bag = []
        self.item_bag = []

    def add_pokemon(self, pokedex_number):
        clear()
        new_pokemon = pokemon(pokedex_number)
        self.pokemon_bag.append(new_pokemon)
        print("Name: {0.name}\nType: {0.type}\nAttack: {0.attack}\nHP: {0.hp}/{0.max_hp}".format(new_pokemon))
        input("\nPress enter to continue.")
        clear()

    def show_pokemons(self):
        for poke in self.pokemon_bag: print("{0.name}\t\tType: {0.type}\tAttack: {0.attack}\tHP: {0.hp}/{0.max_hp}\tMoves: {1} & {2}".format(poke, poke.moves[0].get("Name"), poke.moves[1].get("Name")))
        input("\nPress enter to continue.")
        clear()


class pokemon():

    def __init__(self, pokedex_number):
        self.name = pokemon_df["Name"].iloc[pokedex_number - 1]
        self.type = pokemon_df["Type 1"].iloc[pokedex_number - 1]
        self.max_hp = pokemon_df["HP"].iloc[pokedex_number - 1]
        self.hp = self.max_hp #Health points
        self.attack = pokemon_df["Attack"].iloc[pokedex_number - 1]
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
        self.pokemons = [pokemon1, pokemon2]

    def attack(self, attacker, move_name):
        i = 0 if attacker == 1 else 1
        j = 1 if attacker == 1 else 0
        
        move_dict = next(item for item in self.pokemons[i].moves if item["Name"] == move_name)
        move_dmg = move_dict.get("Power")
        move_type = move_dict.get("Type")
        multiplier = damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemons[j].type)]['Multiplier'].values[0]
        damage = round(self.pokemons[i].attack * multiplier * move_dmg / 100)
        self.pokemons[j].hp -= damage
        if multiplier > 1: print("It's super effective.\n")
        if multiplier < 1: print("It's not very effective.\n")            
        print("{0.name} ({0.type}) hits {1.name} ({1.type}) with {2} ({4}) for {3} points.".format(self.pokemons[i], self.pokemons[j], move_name, damage, move_type))
        input("\nPress enter to continue.")
        clear()
        if self.pokemons[j].hp <= 0: self.pokemons[j].death()
    
    def __str__(self):
        string = "{0}\n{1}".format(self.pokemons[0], self.pokemons[1])

        return string
    
    def winner(self):
        print("The winner is " + self.pokemons[0].name) if self.pokemons[0].alive == True else print("The winner is " + self.pokemons[1].name)
        input("\nPress enter to continue.")
        clear()



def battle_fun(pokemon1, pokemon2):
    run_battle = True
    if pokemon1.alive and pokemon2.alive:

        battle_instance = battle(pokemon1, pokemon2)

        i = 11
        while pokemon1.alive and pokemon2.alive and run_battle == True:
            if i%2 == 1:
                option = input("{0}\n\nBattle Menu\n\n1 - Attack\n2 - Feed\n3 - Run away\n\nEnter number: ".format(battle_instance))
                clear()
                if option == "1":
                    option_move_name = input("Choose move:\n\n1 - " + pokemon1.moves[0].get("Name") + "\n2 - " + pokemon1.moves[1].get("Name") + "\n\nEnter number: ")
                    clear()
                    if option_move_name == "1":
                        battle_instance.attack(1, pokemon1.moves[0].get("Name"))  
                    elif option_move_name == "2":
                        battle_instance.attack(1, pokemon1.moves[1].get("Name"))
                    else:
                        print("Choose a valid move.")
                        input("\nPress enter to continue.")
                        clear()
                        i -= 1
                
                elif option == "2":
                    pokemon1.feed(25)
                
                elif option == "3":
                    print("Running away.")
                    input("\nPress enter to continue.")
                    clear()
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
        print("Your Pokemon is dead.")
        input("\nPress enter to continue.")
        clear()



def main_menu(player):

    option = input("Main Menu\n\n1 - New Pokemon\n2 - View Pokemons\n3 - Fight \n4 - Feed\n5 - Revive\n6 - Exit menu\n\nEnter number: ")
    clear()
    if option == "1": #Add new Pokemon
        player.add_pokemon()

    elif option == "2": #Show pokemons
        player.show_pokemons()

    elif option == "3": #Fighting
        print("Which Pokemon do you choose for the fight?\n\n")
        [print(str(idx + 1) + " - " + str(x.name)) for idx, x in enumerate(player.pokemon_bag)]
        pokemon_number = input("\n\nEnter number: ")
        clear()
        try:
            user_pokemon = player.pokemon_bag[int(pokemon_number) - 1]
            battle_fun(user_pokemon, pokemon("Random Pokemon"))
        except:
            print("Try another number.")
            input("\nPress enter to continue.")
            clear()
        

    elif option == "4": #Feed Pokemon
        name_to_find = input("Which Pokemon do you want to feed?: ")
        clear()
        user_pokemon = next((pokemon_to_feed for pokemon_to_feed in player.pokemon_bag if pokemon_to_feed.name == name_to_find), None)
        user_pokemon.feed(25)

    elif option == "5": #Revive Pokemon
        name_to_find = input("Which Pokemon do you want to revive?: ")
        clear()
        user_pokemon = next((pokemon_to_revive for pokemon_to_revive in player.pokemon_bag if pokemon_to_revive.name == name_to_find), None)
        user_pokemon.revive(75)

    elif option == "6": #Exit
        global run
        run = False

    else:
        print("Try again...")

    return player


#-------------------Main-----------------------
clear()
# player_name = character(input("What's your name?: "))
player = character("PlayerOne")
clear()
while  len(player.pokemon_bag) == 0:
    first_num = input("Choose your first pokemon.\n\n1 - Bulbasaur\n2 - Charmander\n3 - Squirtle\n\nEnter number: ")
    clear()
    player.add_pokemon(1) if first_num == "1" else player.add_pokemon(4) if first_num == "2" else player.add_pokemon(7) if first_num == "3" else input("Try another number.\n\nPress enter to continue.")
    clear()

run = True
while run:
    player = main_menu(player)
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