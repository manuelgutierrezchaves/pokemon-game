import os
import battle, character, items, move, pokemon
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

# TO DO LIST
# meter niveles y experiencia
# mejorar las batallas y los movimientos
# (probabilidad de fallar, estados alterados, cambios en stats, etc)
# meter mapa completo y actividades interesantes (dungeons, legendarios)
# meter movimientos a los pokemon que dependan del nivel
# meter evoluciones
# guardar y cargar partida

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

def main_menu():
    
    print(f"{map.print_loc()}\n\n1 - Pokemons\n2 - Move\n3 - Activities\n4 - Items\n5 - Exit game")
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
        _ = items.item_menu(player)

    elif option == 5: #Exit
        global run
        run = False


#-------------------Main-----------------------
clear()
player = character.character("PlayerOne")
map = move.move(player)
clear()
# first_num = input("Choose your first pokemon.\n\n1 - Bulbasaur\n2 - Charmander\n3 - Squirtle\n\nEnter number: ")
# clear()
# player.add_pokemon(1) if first_num == "1" else player.add_pokemon(4) if first_num == "2" else player.add_pokemon(7) if first_num == "3" else input("Try another number.\n\nPress enter to continue.")
# clear()

#TEST-------------
player.pokemon_bag.append(pokemon.pokemon(3))
player.pokemon_bag.append(pokemon.pokemon(6))
player.pokemon_bag.append(pokemon.pokemon(9))
#-----------------

run = True
while run:
    main_menu()
#----------------------------------------------
