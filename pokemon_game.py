import os
import random
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
import pandas as pd
damage_df = pd.read_csv("damage_multiplier.csv")
moves_df = pd.read_csv("move_sets.csv")
pokemon_df = pd.read_csv("pokemon_data.csv")


class character():

    def __init__(self, name):
        self.name = name
        self.pokemon_bag = []
        self.item_bag = [{"Item": "Potion", "Kind": "Heal", "HP": 10, "Quantity": 2},
                        {"Item": "Super Potion", "Kind": "Heal", "HP": 20, "Quantity": 2},
                        {"Item": "Mega Potion", "Kind": "Heal", "HP": 30, "Quantity": 2},
                        {"Item": "Revive", "Kind": "Revive", "% HP": 50, "Quantity": 2},
                        {"Item": "Max Revive", "Kind": "Revive", "% HP": 100, "Quantity": 2}]

    def add_pokemon(self, pokedex_number): #Need to not allow duplicates
        clear()
        new_pokemon = pokemon(pokedex_number)
        self.pokemon_bag.append(new_pokemon)
        print("Name: {0.name}\nType: {0.type}\nAttack: {0.attack}\nHP: {0.hp}/{0.max_hp}".format(new_pokemon))
        input("\nPress enter to continue.")
        clear()

    def show_pokemons(self):
        for poke in self.pokemon_bag: print("{0.name}\t\tType: {0.type}\tAttack: {0.attack}\tHP: {0.hp}/{0.max_hp}\tMoves: {1} & {2}".format(poke, poke.moves[0].get("Name"), poke.moves[1].get("Name")))
        for poke in self.pokemon_bag: print(f"{poke.name}\t\tType: {poke.type}\tAttack: {poke.attack}\tHP: {poke.hp}/{poke.max_hp}\tMoves: {poke.moves[0].get('Name')} & {poke.moves[1].get('Name')}")


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

    def revive(self, quantity): #Quantity is a percentage of max HP
        if not self.alive:
            self.hp = round(quantity * self.max_hp / 100)
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
        
        move_dict = next(item for item in self.pokemons[i].moves if item["Name"] == move_name)
        move_dmg = move_dict.get("Power")
        move_type = move_dict.get("Type")
        multiplier = damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemons[not i].type)]['Multiplier'].values[0]
        damage = round(self.pokemons[i].attack * multiplier * move_dmg / 300 * random.uniform(0.8, 1.2))
        self.pokemons[not i].hp -= damage          
        print("{0.name} hits {1.name} with {2} for {3} points.".format(self.pokemons[i], self.pokemons[not i], move_name, damage))
        if multiplier > 1: print("\nIt's super effective.")
        if multiplier < 1: print("\nIt's not very effective.")          
        input("\nPress enter to continue.")
        clear()
        if self.pokemons[not i].hp <= 0: self.pokemons[not i].death()
    
    def __str__(self):
        string = "{0}\n{1}".format(self.pokemons[0], self.pokemons[1])
        return string



def battle_fun(enemy):
    run_battle = True
    user_pokemon = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
    if user_pokemon == None:
        print("All your Pokemons are dead.")
        input("\nPress enter to continue.")
        clear()
        return

    if isinstance(enemy, character):
        enemy_pokemon = enemy.pokemon_bag[0]
        battle_instance = battle(user_pokemon, enemy_pokemon)
        i = 11
        while run_battle == True:
            if i%2 == 1:
                if not user_pokemon.alive:
                    user_pokemon = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
                    battle_instance = battle(user_pokemon, enemy_pokemon)
                    if user_pokemon == None:
                        run_battle = False
                        print("You lost")
                        input("\nPress enter to continue.")
                        clear()
                        break
                        
                run_battle, i = battle_menu(battle_instance, user_pokemon, i)
                
            else:
                if not enemy_pokemon.alive:
                    enemy_pokemon = next((poke for poke in enemy.pokemon_bag if poke.alive == True), None)
                    battle_instance = battle(user_pokemon, enemy_pokemon)
                    if enemy_pokemon == None:
                        run_battle = False
                        print("You win")
                        input("\nPress enter to continue.")
                        clear()
                        break

                battle_instance.attack(2, enemy_pokemon.moves[random.randint(0, 1)].get("Name"))
            
            i += 1


    if isinstance(enemy, pokemon):
        enemy_pokemon = enemy
        battle_instance = battle(user_pokemon, enemy_pokemon)
        i = 11
        while run_battle == True:
            if i%2 == 1:
                if not user_pokemon.alive:
                    user_pokemon = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
                    battle_instance = battle(user_pokemon, enemy_pokemon)
                    if user_pokemon == None:
                        run_battle = False
                        print("You lost")
                        input("\nPress enter to continue.")
                        clear()
                        break
                        
                run_battle, i = battle_menu(battle_instance, user_pokemon, i)
                
            else:
                if not enemy_pokemon.alive:
                    run_battle = False
                    print("You win")
                    input("\nPress enter to continue.")
                    clear()
                    break

                battle_instance.attack(2, enemy_pokemon.moves[random.randint(0, 1)].get("Name"))
            
            i += 1



def battle_menu(battle_instance, user_pokemon, i):
    print("{0}\n\nBattle Menu\n\n1 - Attack\n2 - Items\n3 - Run away".format(battle_instance))
    option = input_number(3)
    clear()

    if option == 1:
        print("Choose move:\n\n1 - " + user_pokemon.moves[0].get("Name") + "\n2 - " + user_pokemon.moves[1].get("Name"))
        print("3 - Cancel")
        option_move_name = input_number(3)
        clear()
        if option_move_name == 1:
            battle_instance.attack(1, user_pokemon.moves[0].get("Name"))  
        elif option_move_name == 2:
            battle_instance.attack(1, user_pokemon.moves[1].get("Name"))
        elif option_move_name == 3:
            i -= 1
    
    elif option == 2:
        item_menu()
    
    elif option == 3:
        print("Running away.")
        input("\nPress enter to continue.")
        clear()
        return False, i
    
    return True, i


def main_menu():

    print("Main Menu\n\n1 - Pokemons\n2 - Fight \n3 - Items\n4 - Exit menu")
    option = input_number()
    clear()
    if option == 1: #Show pokemons
        player.show_pokemons()
        print("\n1 - Choose order\n2 - Back")
        if input_number(2) == 1:
            clear()
            for idx, poke in enumerate(player.pokemon_bag): print(str(idx+1) + " - {0.name}\t\tType: {0.type}\tAttack: {0.attack}\tHP: {0.hp}/{0.max_hp}\tMoves: {1} & {2}".format(poke, poke.moves[0].get("Name"), poke.moves[1].get("Name")))
            pokemon_order = input("\nEnter order: ") #Breaks if wrong input
            clear()
            int_order = [(int(i)-1) for i in pokemon_order]
            player.pokemon_bag = [player.pokemon_bag[i] for i in int_order]
            player.show_pokemons()
            input("\n\nPress enter to continue.")
            clear()
        else: clear()


    elif option == 2: #Fighting
        enemy = character("Enemy")
        enemy.pokemon_bag.append(pokemon(19))
        enemy.pokemon_bag.append(pokemon(20))
        battle_fun(enemy)

    elif option == 3: #Items
        item_menu()

    elif option == 4: #Exit
        global run
        run = False     


def item_menu():
    print("Inventory.\n")
    [print(str(idx) + " - " + i["Item"] + " x" + str(i["Quantity"])) for idx, i in enumerate(player.item_bag, start=1)]
    print(str(len(player.item_bag) + 1) + " - Go back")
    item_number = input_number(len(player.item_bag)+1)
    clear()
    if item_number != len(player.item_bag) + 1:
        if player.item_bag[item_number-1]["Quantity"] == 0: 
            print("You don't have any more.")
            input("\n\nPress enter to continue.")
            clear()
            return
        player.item_bag[item_number-1]["Quantity"] -= 1
        print("Choose Pokemon: \n")
        [print(str(idx) + " - " + str(x.name)) for idx, x in enumerate(player.pokemon_bag, start=1)]
        print(str(len(player.pokemon_bag) + 1) + " - Cancel")
        pokemon_number = input_number(len(player.pokemon_bag)+1)
        clear()
        if pokemon_number != len(player.pokemon_bag) + 1:
            user_pokemon = player.pokemon_bag[int(pokemon_number) - 1]
            if player.item_bag[int(item_number)-1]["Kind"] == "Heal": user_pokemon.feed(player.item_bag[int(item_number)-1]["HP"])
            if player.item_bag[int(item_number)-1]["Kind"] == "Revive": user_pokemon.revive(player.item_bag[int(item_number)-1]["% HP"])
            
     

def input_number(length=1000):
    number_str = input("\n\nEnter number: ")
    try:
        number_int = int(number_str)
        if 0 < number_int <= length:
            return number_int
        else:
            print (2 * "\033[A                             \033[A") #Delete previous line x2
            return input_number(length)
    except: 
        print (2 * "\033[A                             \033[A") #Delete previous line x2
        return input_number(length)


#-------------------Main-----------------------
clear()
player = character("PlayerOne")
clear()
# first_num = input("Choose your first pokemon.\n\n1 - Bulbasaur\n2 - Charmander\n3 - Squirtle\n\nEnter number: ")
# clear()
# player.add_pokemon(1) if first_num == "1" else player.add_pokemon(4) if first_num == "2" else player.add_pokemon(7) if first_num == "3" else input("Try another number.\n\nPress enter to continue.")
# clear()

#TEST-------------
player.pokemon_bag.append(pokemon(3))
player.pokemon_bag.append(pokemon(6))
player.pokemon_bag.append(pokemon(9))


#-----------------

run = True
while run:
    main_menu()
#----------------------------------------------
