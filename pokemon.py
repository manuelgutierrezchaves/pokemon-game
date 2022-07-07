import os
import pandas as pd
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
pokemon_df = pd.read_csv("pokemon_data.csv")
moves_df = pd.read_csv("move_sets.csv")

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