import os
import pandas as pd
os.system("color")
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
damage_df = pd.read_csv("damage_multiplier.csv")
pokemon_df = pd.read_csv("pokemon_data.csv", keep_default_na=False)
moves_df = pd.read_csv("move_sets.csv")

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

# https://i.stack.imgur.com/j7e4i.gif
class colors:
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    GOLD = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    BLINK = '\033[5m'
    END = '\033[0m'