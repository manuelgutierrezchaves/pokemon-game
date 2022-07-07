import os, random
import battle, pokemon, character
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

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

class move(): #Map and movements
    
    def __init__(self, player):
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
        self.player = player

    def map_menu(self):
        print("Where do you want to go?\n")
        for idx, i in enumerate(self.directions, start=1): print(f"{idx} - {i}")
        print(f"{len(self.directions)+1} - Go back")
        place_number = input_number(len(self.directions)+1)
        if place_number == len(self.directions) + 1: return
        self.update(self.directions[place_number-1])

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
        battle.battle(self.player, pokemon.pokemon(self.wilds[random.randint(0,len(self.wilds)-1)]))
        return

    def gym(self):
        if not self.leader: 
            input("This Gym is closed.\n\nPress enter to continue.")
            clear()
            return
        input(f"You are going to fight against gym leader {self.leader.get('Name')}. Prepare yourself.\n\nPress enter to continue.")
        clear()
        leader = character.character(self.leader.get("Name"), self.leader.get("Pokemons"))
        battle.battle(self.player, leader)

    def center(self):
        print("Pokemon Center:\n\n1 - Heal\n2 - Shop")
        if input_number(2) == 1:
            for poke in self.player.pokemon_bag:
                poke.hp = poke.max_hp
                poke.alive = True
            input("All your Pokemons have been restored to full HP.\n\nPress enter to continue.")
            clear()
        else:
            self.item_shop()

    def item_shop(self):
        print("Item shop\n")
        for idx, item in enumerate(self.items_sold, start=1): print(f"{idx} - {item}")
        item_number = input_number(len(self.items_sold))
        item = self.items_sold[item_number-1]
        self.player.add_item(item)