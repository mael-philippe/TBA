# Description: The actions module.

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).
        """
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        direction = list_of_words[1].upper()
        if direction not in ["N", "E", "S", "O", "U", "D"]:
            print(f"\nDirection '{direction}' non valide. Les directions possibles sont: N, E, S, O, U (Up), D (Down).\n")
            return False
        
        success = player.move(direction)
        if success:
            print(player.get_history())
        return success

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def status(game, list_of_words, number_of_parameters):
        """Afficher l'état du joueur"""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(f"\n=== État de {player.name} ===")
        print(f"❤️  Santé: {player.health}/{player.max_health}")
        print(f"🎒 Inventaire: {len(player.inventory)} objets")
        print(f"⚖️  Poids: {player.get_current_weight()}/{player.max_weight} kg")
        if player.health < 30:
            print("⚠️  Attention: Santé critique!")
        print()
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """Vérifier l'inventaire du joueur"""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(player.get_inventory_string())
        return True

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        """
        Afficher l'historique des salles visitées.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(player.get_history())
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Revenir à la salle précédente.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        success = player.go_back()
        if success:
            print(player.get_history())
        return success

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un personnage.
        """
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        character_name_parts = list_of_words[1:]
        character_name = " ".join(character_name_parts)
        
        current_room = player.current_room
        
        character = current_room.get_character(character_name)
        if character:
            return character.interact(player, game)
        else:
            print(f"\nIl n'y a personne nommé '{character_name}' ici.\n")
            return False

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Regarder autour de soi (affiche les objets et personnages).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        
        print("\nVous regardez autour de vous...")
        print(current_room.get_long_description())
        
        print(current_room.get_inventory_string())
        
        if current_room.characters:
            print("\nPersonnes présentes:")
            for character in current_room.characters:
                print(f"  - {character.name}: {character.description}")
        
        print()
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Prendre un objet dans la salle.
        """
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        item_name_parts = list_of_words[1:]
        item_name = " ".join(item_name_parts)
        
        current_room = player.current_room
        
        item = current_room.remove_item(item_name)
        if item:
            if player.add_item(item):
                return True
            else:
                current_room.add_item(item)
                return False
        else:
            print(f"\n❌ L'objet '{item_name}' n'est pas dans cette salle.\n")
            return False

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Déposer un objet de l'inventaire dans la salle.
        """
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        item_name_parts = list_of_words[1:]
        item_name = " ".join(item_name_parts)
        
        current_room = player.current_room
        
        item = player.remove_item(item_name)
        if item:
            current_room.add_item(item)
            return True
        else:
            return False
        
    @staticmethod
    def use(game, list_of_words, number_of_parameters):
        """
        Utiliser un objet de l'inventaire (ex: use GPS, use Chien).
        """
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            print("\nQue voulez-vous utiliser ? (ex: use GPS)")
            return False
        
        # Reconstruire le nom de l'objet (ex: "Clé USB")
        item_name = " ".join(list_of_words[1:]).lower()
        
        # 1. Vérifier si l'objet est dans l'inventaire
        item_to_use = None
        for item in player.inventory:
            if item.name.lower() == item_name:
                item_to_use = item
                break
        
        if not item_to_use:
            print(f"\n🚫 Vous n'avez pas '{list_of_words[1]}' dans votre inventaire.")
            return False

        # --- EFFET DU GPS ---
        if item_to_use.name == "GPS":
            print("\n📡 --- ACTIVATION DU GPS MYSTIK --- 📡")
            print("Scan des signaux en cours...")
            found = False
            for char in game.characters:
                # On n'affiche pas les PNJ qui sont dans la même salle (on les voit déjà)
                if char.current_room != player.current_room:
                    print(f"  📍 {char.name} se trouve : {char.current_room.name}")
                    found = True
            
            if not found:
                print("  (Aucun signal distant détecté. Tout le monde est peut-être ici ?)")
            return True

        # --- EFFET DU CHIEN ---
        elif item_to_use.name == "Chien":
            print("\n🐶 Vous flattez la tête du chien et lui dites de chercher.")
            print("Le chien renifle l'air...")
            found_something = False
            
            # Vérifier les salles adjacentes (Exits)
            current_room = player.current_room
            for direction, room in current_room.exits.items():
                if room and room.inventory: # Si la salle existe et a des objets
                    # On liste les objets (sauf les objets cachés/spéciaux si besoin)
                    items_names = [i.name for i in room.inventory]
                    if items_names:
                        print(f"  🐕 Wouf ! Wouf ! (Il aboie vers le {direction} !)")
                        print(f"     (Il semble avoir senti : {', '.join(items_names)})")
                        found_something = True
            
            if not found_something:
                print("  😿 Le chien couine doucement. Il ne sent rien d'intéressant autour.")
            return True
            
        # --- AUTRES OBJETS ---
        else:
            print(f"\nVous ne savez pas comment utiliser '{item_to_use.name}' ici.")
            return False
