import os
import pokemon
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

class character():

    def __init__(self, name, pokemons=[]):
        self.name = name
        self.pokemon_bag = []
        self.item_bag = [{"Item": "Potion", "Kind": "Heal", "HP": 10, "Quantity": 2},
                        {"Item": "Super Potion", "Kind": "Heal", "HP": 20, "Quantity": 2},
                        {"Item": "Mega Potion", "Kind": "Heal", "HP": 30, "Quantity": 2},
                        {"Item": "Revive", "Kind": "Revive", "% HP": 50, "Quantity": 2},
                        {"Item": "Max Revive", "Kind": "Revive", "% HP": 100, "Quantity": 2}]
        
        if pokemons: [self.pokemon_bag.append(pokemon.pokemon(number)) for number in pokemons] #Only for the enemies    

    def add_pokemon(self, pokedex_number): #Need to not allow duplicates
        clear()
        new_pokemon = pokemon.pokemon(pokedex_number)
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