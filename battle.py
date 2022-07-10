import random
import pokemon, character, items
from misc import input_number, clear, colors, damage_df

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
        i = attacker - 1
        
        move_dict = next(item for item in self.pokemons[i].moves if item["Name"] == move_name)
        move_dmg = move_dict.get("Power")
        move_type = move_dict.get("Type")
        multiplier = damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemons[not i].type)]['Multiplier'].values[0]
        if self.pokemons[not i].type2 != "": # For double type defenders
            multiplier *= damage_df[(damage_df['Attacker'] == move_type) & (damage_df['Defender'] == self.pokemons[not i].type2)]['Multiplier'].values[0]
            
        #https://bulbapedia.bulbagarden.net/wiki/Damage
        #level = (2 * self.pokemons[i].level / 5) + 2 Meter esto en vez de lo de abajo cuando haya niveles
        level = 10
        att_def = self.pokemons[i].attack / self.pokemons[not i].defense
        weather = 1
        critical = 1.5 if (random.uniform(0, 1) < 0.05) else 1
        rand_factor = random.uniform(0.85, 1)
        stab = 1.5 if (self.pokemons[i].type == move_type) else 1
        damage = round(((level * att_def * move_dmg / 50) + 2) * weather * critical * rand_factor * stab * multiplier)
        self.pokemons[not i].hp -= damage          
        print("{0.name} hits {1.name} with {2} for {3} damage.".format(self.pokemons[i], self.pokemons[not i], move_name, damage))
        
        if critical != 1: print (colors.RED+"\nA critical hit!"+colors.END)
        if multiplier > 1:
            print(colors.WHITE+"\nIt's super effective."+colors.END)
        elif multiplier == 0:
            print(colors.GREY+"\nIt had no effect."+colors.END)
        elif multiplier < 1:
            print(colors.GREY+"\nIt's not very effective."+colors.END)
        input("\nPress enter to continue.")
        clear()
        
        if self.pokemons[not i].hp <= 0:
            self.pokemons[not i].death()
            return True # Return whether attack was lethal or not
        
        return False
    
    def __str__(self):
        string = "{0}\n{1}".format(self.pokemons[0], self.pokemons[1])
        return string
    