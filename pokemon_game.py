import os
import random
from turtle import speed
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
import pandas as pd
damage_df = pd.read_csv("damage_multiplier.csv")
moves_df = pd.read_csv("move_sets.csv")
pokemon_df = pd.read_csv("pokemon_data.csv")
_DEBUG = True

class move(): #Map and movements
    
    def __init__(self):
        self.full_map = [{"Name": "Pallet Town", "Activities": [], "Directions": ["Route 1"], "Wilds": [], "Shop": []},
                        {"Name": "Route 1", "Activities": ["Fight wild Pokemons"], "Directions": ["Viridian City", "Pallet Town"], "Wilds": [16, 19], "Shop": []},
                        {"Name": "Viridian City", "Activities": ["Pokemon Center"], "Directions": ["Route 2", "Route 1"], "Wilds": [], "Shop": ["Potion", "Revive"]},
                        {"Name": "Route 2", "Activities": ["Fight wild Pokemons"], "Directions": ["Pewter City", "Viridian City"], "Wilds": [16, 19, 13, 10, 29, 32, 122], "Shop": []},
                        {"Name": "Pewter City", "Activities": ["Gym", "Pokemon Center"], "Directions": ["Route 3", "Route 2"], "Wilds": [], "Shop": ["Potion", "Super Potion", "Revive"]},
                        {"Name": "Route 3", "Activities": ["Fight wild Pokemons"], "Directions": ["Pewter City"], "Wilds": [16, 19, 13, 10, 29, 32, 122], "Shop": []}]

        self.gym_leaders = [{"Name": "Brock", "Town": "Pewter City", "Pokemons": [74, 95], "Badge": "Boulder Badge"},
                            {"Name": "Misty", "Town": "Cerulean City", "Pokemons": [120, 121], "Badge": "Cascade Badge"},
                            {"Name": "Lt. Surge", "Town": "Vermillion City", "Pokemons": [100, 25, 26], "Badge": "Thunder Badge"}]

        self.actual_loc_name = "Pallet Town"
        self.activities = next(place["Activities"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.directions = next(place["Directions"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.wilds = next(place["Wilds"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.items_sold = next((place["Shop"] for place in self.full_map if place["Name"] == self.actual_loc_name), None)
        self.leader = next((enemy for enemy in self.gym_leaders if enemy["Town"] == self.actual_loc_name), None)

    def map_menu(self):
        print("Where do you want to go?\n")
        for idx, i in enumerate(self.directions, start=1): print(f"{idx} - {i}")
        print(f"{len(self.directions)+1} - Go back")
        place_number = input_number(len(self.directions)+1)
        if place_number == len(self.directions) + 1: return
        map.update(self.directions[place_number-1])

    def activities_menu(self):
        if not self.activities:
            input("There's nothing to do here.\n\n\nPress enter to continue.")
            return
        print("What do you want to do?\n")
        for idx, i in enumerate(self.activities, start=1): print(f"{idx} - {i}")
        print(f"{len(self.activities)+1} - Go back")
        activity_number = input_number(len(self.activities)+1)
        if activity_number == len(self.activities) + 1: return
        activity_name = self.activities[activity_number-1]
        if activity_name == "Gym":
            self.gym()
        elif activity_name == "Pokemon Center":
            self.center()
        elif activity_name == "Fight wild Pokemons":
            self.fight_wild()

    def update(self, new_loc):
        self.actual_loc_name = new_loc
        self.activities = next(place["Activities"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.directions = next(place["Directions"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.wilds = next(place["Wilds"] for place in self.full_map if place["Name"] == self.actual_loc_name)
        self.leader = next((enemy for enemy in self.gym_leaders if enemy["Town"] == self.actual_loc_name), None)
        self.items_sold = next((place["Shop"] for place in self.full_map if place["Name"] == self.actual_loc_name), None)

    def print_loc(self):
        return f"You are in {self.actual_loc_name}"

    def fight_wild(self):
        battle(player, pokemon(self.wilds[random.randint(0,len(self.wilds)-1)]))
        return

    def gym(self):
        if not self.leader: 
            input("This Gym is closed.\n\nPress enter to continue.")
            clear()
            return
        input(f"You are going to fight against gym leader {self.leader.get('Name')}. Prepare yourself.\n\nPress enter to continue.")
        clear()
        leader = character(self.leader.get("Name"), self.leader.get("Pokemons"))
        battle(player, leader)

    def center(self):
        print("Pokemon Center:\n\n1 - Heal\n2 - Shop")
        if input_number(2) == 1:
            for poke in player.pokemon_bag:
                poke.hp = poke.max_hp
                poke.alive = True
            input("All your Pokemons have been restore to full HP.\n\nPress enter to continue.")
            clear()
        else:
            self.item_shop()

    def item_shop(self):
        print("Item shop\n")
        for idx, item in enumerate(self.items_sold, start=1): print(f"{idx} - {item}")
        item_number = input_number(len(self.items_sold))
        item = self.items_sold[item_number-1]
        player.add_item(item)


class character():

    def __init__(self, name, pokemons=[]):
        self.name = name
        self.pokemon_bag = []
        self.item_bag = [{"Item": "Potion", "Kind": "Heal", "HP": 10, "Quantity": 2},
                        {"Item": "Super Potion", "Kind": "Heal", "HP": 20, "Quantity": 2},
                        {"Item": "Mega Potion", "Kind": "Heal", "HP": 30, "Quantity": 2},
                        {"Item": "Revive", "Kind": "Revive", "% HP": 50, "Quantity": 2},
                        {"Item": "Max Revive", "Kind": "Revive", "% HP": 100, "Quantity": 2}]
        
        if pokemons: [self.pokemon_bag.append(pokemon(number)) for number in pokemons] #Only for the enemies    

    def add_pokemon(self, pokedex_number): #Need to not allow duplicates
        clear()
        new_pokemon = pokemon(pokedex_number)
        self.pokemon_bag.append(new_pokemon)
        print("Name: {0.name}\nType: {0.type}\nAttack: {0.attack}\nHP: {0.hp}/{0.max_hp}".format(new_pokemon))
        input("\nPress enter to continue.")
        clear()

    def add_item(self, item_name):
        idx = next((idx for (idx, dict) in enumerate(self.item_bag) if dict["Item"] == item_name), None)
        self.item_bag[idx]["Quantity"] = self.item_bag[idx].get("Quantity") + 1

    def show_pokemons(self):
        for poke in self.pokemon_bag: print(f"{poke.name}\t\tType: {poke.type}\tAttack: {poke.attack}\tHP: {poke.hp}/{poke.max_hp}\tMoves: {poke.moves[0].get('Name')} & {poke.moves[1].get('Name')}")
        print("")
        for item in self.item_bag: print(f"{item.get('Item')}\t\tKind: {item.get('Kind')}\t\Quantity: {item.get('Quantity')}")


class pokemon():

    def __init__(self, pokedex_number):
        self.name = pokemon_df["Name"].iloc[pokedex_number - 1]
        self.type = pokemon_df["Type 1"].iloc[pokedex_number - 1]
        self.max_hp = pokemon_df["HP"].iloc[pokedex_number - 1]
        self.hp = self.max_hp #Health points
        self.attack = pokemon_df["Attack"].iloc[pokedex_number - 1]
        self.speed = pokemon_df["Speed"].iloc[pokedex_number - 1]
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

    def __init__(self, player, enemy):
        self.run_battle = True
        self.pokemons = [0, 1]
        self.pokemons[0] = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
        if self.pokemons[0] == None:
            print("All your Pokemons are dead.")
            input("\nPress enter to continue.")
            clear()
            return

        if isinstance(enemy, character): self.pokemons[1] = enemy.pokemon_bag[0]
        if isinstance(enemy, pokemon): self.pokemons[1] = enemy

        self.battle_running(player, enemy)

    def victory(self):
        self.run_battle = False
        input("You win\n\nPress enter to continue.")
        clear()

    def loss(self):
        self.run_battle = False
        input("You lose\n\nPress enter to continue.")
        clear()

    def battle_menu(self):
        while(True):
            print(f"{self}\n\nBattle Menu\n\n1 - Attack\n2 - Items\n3 - Run away")
            option = input_number(3)

            if option == 1: #Attack
                print(f"Choose move:\n\n1 - {self.pokemons[0].moves[0].get('Name')}\n2 - {self.pokemons[0].moves[1].get('Name')}\n3 - Cancel")
                option_move_name = input_number(3)
                if (option_move_name == 1) or (option_move_name == 2):
                    if (self.pokemons[0].speed > self.pokemons[1].speed): # Check who is faster
                        lethal = self.attack(1, self.pokemons[0].moves[option_move_name - 1].get("Name"))
                        if not lethal: self.attack(2, self.pokemons[1].moves[random.randint(0, 1)].get("Name"))
                    elif (self.pokemons[0].speed < self.pokemons[1].speed):
                        lethal: self.attack(2, self.pokemons[1].moves[random.randint(0, 1)].get("Name"))
                        if not lethal: self.attack(1, self.pokemons[0].moves[option_move_name - 1].get("Name"))
                    else: # Speed tie
                        if (random.randint(0, 1)) == 1:
                            lethal: self.attack(1, self.pokemons[0].moves[option_move_name - 1].get("Name"))
                            if not lethal: self.attack(2, self.pokemons[1].moves[random.randint(0, 1)].get("Name"))
                        else: 
                            lethal: self.attack(2, self.pokemons[1].moves[random.randint(0, 1)].get("Name"))
                            if not lethal: self.attack(1, self.pokemons[0].moves[option_move_name - 1].get("Name"))
            
            elif option == 2: #Items
                item_menu()
                self.attack(2, self.pokemons[1].moves[random.randint(0, 1)].get("Name"))
            
            elif option == 3: #Run away
                print("Running away.")
                input("\nPress enter to continue.")
                clear()
                return False
            
            return True

    def battle_running(self, player, enemy):
        while self.run_battle == True:
            if not self.pokemons[0].alive:
                self.pokemons[0] = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
                if self.pokemons[0] == None:
                    self.loss()
                    return
            if isinstance(enemy, pokemon) and not self.pokemons[1].alive:
                self.victory()
                return
            if not self.pokemons[1].alive:
                self.pokemons[1] = next((poke for poke in enemy.pokemon_bag if poke.alive == True), None)
                if self.pokemons[1] == None:
                    self.victory()
                    return
            self.run_battle = self.battle_menu()

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
        if self.pokemons[not i].hp <= 0:
            self.pokemons[not i].death()
            return True # Return whether attack was lethal or not
        
        return False
    
    def __str__(self):
        string = "{0}\n{1}".format(self.pokemons[0], self.pokemons[1])
        return string



def main_menu():
    
    print(f"{map.print_loc()}\n\n1 - Pokemons\n2 - Move\n3 - Activities\n4 - Items\n5 - Exit menu")
    option = input_number()
    if option == 1: #Show pokemons
        player.show_pokemons()
        print("\n1 - Choose order\n2 - Back")
        if input_number(2) == 1:
            for idx, poke in enumerate(player.pokemon_bag): print(str(idx+1) + " - {0.name}\t\tType: {0.type}\tAttack: {0.attack}\tHP: {0.hp}/{0.max_hp}\tMoves: {1} & {2}".format(poke, poke.moves[0].get("Name"), poke.moves[1].get("Name")))
            pokemon_order = input("\nEnter order: ") #Breaks if wrong input
            clear()
            int_order = [(int(i)-1) for i in pokemon_order]
            player.pokemon_bag = [player.pokemon_bag[i] for i in int_order]
            player.show_pokemons()
            input("\n\nPress enter to continue.")
            clear()

    elif option == 2: #Move
        map.map_menu()

    elif option == 3: #Activities
        map.activities_menu()

    elif option == 4: #Items
        item_menu()

    elif option == 5: #Exit
        global run
        run = False     


def item_menu():
    print("Inventory.\n")
    [print(str(idx) + " - " + i["Item"] + " x" + str(i["Quantity"])) for idx, i in enumerate(player.item_bag, start=1)]
    print(str(len(player.item_bag) + 1) + " - Go back")
    item_number = input_number(len(player.item_bag)+1)
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
        if pokemon_number != len(player.pokemon_bag) + 1:
            user_pokemon = player.pokemon_bag[int(pokemon_number) - 1]
            if player.item_bag[int(item_number)-1]["Kind"] == "Heal": user_pokemon.feed(player.item_bag[int(item_number)-1]["HP"])
            if player.item_bag[int(item_number)-1]["Kind"] == "Revive": user_pokemon.revive(player.item_bag[int(item_number)-1]["% HP"])
            
     

def input_number(length=1000):
    number_str = input("\n\nEnter number: ")
    try:
        number_int = int(number_str)
        if 0 < number_int <= length:
            clear()
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
map = move()
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
