from misc import input_number, clear

def item_menu(player):
    print("Inventory.\n")
    [print(str(idx) + " - " + i["Item"] + " x" + str(i["Quantity"])) for idx, i in enumerate(player.item_bag, start=1)]
    print(str(len(player.item_bag) + 1) + " - Go back")
    item_number = input_number(len(player.item_bag)+1)
    if item_number != len(player.item_bag) + 1:
        if player.item_bag[item_number-1]["Quantity"] == 0: 
            print("You don't have any more.")
            input("\n\nPress enter to continue.")
            clear()
            return False
        player.item_bag[item_number-1]["Quantity"] -= 1
        print("Choose Pokemon: \n")
        [print(str(idx) + " - " + str(x.name)) for idx, x in enumerate(player.pokemon_bag, start=1)]
        print(str(len(player.pokemon_bag) + 1) + " - Cancel")
        pokemon_number = input_number(len(player.pokemon_bag)+1)
        if pokemon_number != len(player.pokemon_bag) + 1:
            user_pokemon = player.pokemon_bag[int(pokemon_number) - 1]
            if player.item_bag[int(item_number)-1]["Kind"] == "Heal": user_pokemon.feed(player.item_bag[int(item_number)-1]["HP"])
            if player.item_bag[int(item_number)-1]["Kind"] == "Revive": user_pokemon.revive(player.item_bag[int(item_number)-1]["% HP"])
            return True # Return whether item was used or not
    return False
