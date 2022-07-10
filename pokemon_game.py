from misc import input_number, clear
import battle, character, items, move, pokemon

# TO DO LIST
# meter niveles y experiencia
# mejorar las batallas y los movimientos
# (probabilidad de fallar, estados alterados, cambios en stats, etc)
# meter mapa completo y actividades interesantes (dungeons, legendarios)
# meter movimientos a los pokemon que dependan del nivel
# meter evoluciones
# guardar y cargar partida
# https://www.youtube.com/watch?v=dQw4w9WgXcQ

def main_menu():
    
    clear()
    print(f"{map.print_loc()}\n\n1 - Pokemons\n2 - Move\n3 - Activities\n4 - Items\n5 - Exit game")
    option = input_number()
    if option == 1: #Show pokemons
        player.show_pokemons()
        print("\n1 - Choose order\n2 - Back")
        if input_number(2) == 1:
            for idx, poke in enumerate(player.pokemon_bag): print(str(idx+1) + " - {:<15s} {:<15s} {:<15s} {:<15s} {}".format(f"{poke.name}",f"Type: {poke.type}",f"Attack: {poke.attack}",f"HP: {poke.hp}/{poke.max_hp}",f"Moves: {poke.moves[0].get('Name')} & {poke.moves[1].get('Name')}"))
            pokelist = list()
            numpoke = len(player.pokemon_bag)
            while numpoke > 0:
                num = input_number(len(player.pokemon_bag))
                if num not in pokelist:
                    pokelist.append(num)
                    numpoke -= 1
                    clear()
                for idx, poke in enumerate(player.pokemon_bag): print(str(idx+1) + " - {:<15s} {:<15s} {:<15s} {:<15s} {}".format(f"{poke.name}",f"Type: {poke.type}",f"Attack: {poke.attack}",f"HP: {poke.hp}/{poke.max_hp}",f"Moves: {poke.moves[0].get('Name')} & {poke.moves[1].get('Name')}"))
                print("\nCurrent order:",pokelist)

            player.pokemon_bag = [player.pokemon_bag[int(i)-1] for i in pokelist]
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
player = character.character("PlayerOne")
map = move.move(player)
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
