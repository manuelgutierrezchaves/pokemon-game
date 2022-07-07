import os, random
import pandas as pd
import pokemon, character, items
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
damage_df = pd.read_csv("damage_multiplier.csv")

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

class battle():

    def __init__(self, player, enemy):
        self.run_battle = True
        self.pokemons = [0, 1]
        self.pokemons[0] = next((poke for poke in player.pokemon_bag if poke.alive == True), None)
        self.player = player
        if self.pokemons[0] == None:
            print("All your Pokemons are dead.")
            input("\nPress enter to continue.")
            clear()
            return

        if isinstance(enemy, character.character): self.pokemons[1] = enemy.pokemon_bag[0]
        if isinstance(enemy, pokemon.pokemon): self.pokemons[1] = enemy

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
                used_item = items.item_menu(self.player)
                if not used_item: continue
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
            if isinstance(enemy, pokemon.pokemon) and not self.pokemons[1].alive:
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