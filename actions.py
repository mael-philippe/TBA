# Description: The actions module.

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).
        """
        player = game.player
        l = len(list_of_words)
        
        # Vérifier qu'on a au moins un paramètre
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Prendre seulement le premier mot pour la direction
        direction = list_of_words[1].upper()
        if direction not in ["N", "E", "S", "O"]:
            print(f"\nDirection '{direction}' non valide. Les directions possibles sont: N (Nord), E (Est), S (Sud), O (Ouest).\n")
            return False
        
        success = player.move(direction)
        if success:
            # Afficher l'historique après chaque déplacement réussi
            print(player.get_history())
        return success

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
            # Afficher l'historique après un retour réussi
            print(player.get_history())
        return success

    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un personnage.
        Gère les noms composés.
        """
        player = game.player
        l = len(list_of_words)
        
        # Vérifier qu'on a au moins un paramètre
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Reconstituer le nom complet du personnage
        character_name_parts = list_of_words[1:]  # Prendre tous les mots après "talk"
        character_name = " ".join(character_name_parts)  # Reconstituer le nom complet
        
        current_room = player.current_room
        
        # Vérifier si le personnage existe dans la salle
        success = current_room.interact_with_character(character_name, player)
        if not success:
            print(f"\nIl n'y a personne nommé '{character_name}' ici.\n")
            print("Personnes présentes:")
            for character in current_room.characters:
                print(f"  - {character.name}")
            print()
        return success

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
        
        # Afficher les objets dans la salle
        print(current_room.get_inventory_string())
        
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        Prendre un objet dans la salle.
        Gère les noms composés comme "Clé USB".
        """
        player = game.player
        l = len(list_of_words)
        
        # Vérifier qu'on a au moins un paramètre
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Reconstituer le nom complet de l'objet (tous les mots après la commande)
        item_name_parts = list_of_words[1:]  # Prendre tous les mots après "take"
        item_name = " ".join(item_name_parts)  # Reconstituer le nom complet
        
        current_room = player.current_room
        
        # Vérifier si l'objet existe dans la salle
        item = current_room.remove_item(item_name)
        if item:
            if player.add_item(item):
                return True
            else:
                # Remettre l'objet dans la salle si le joueur ne peut pas le prendre
                current_room.add_item(item)
                return False
        else:
            print(f"\n❌ L'objet '{item_name}' n'est pas dans cette salle.\n")
            return False

    def drop(game, list_of_words, number_of_parameters):
        """
        Déposer un objet de l'inventaire dans la salle.
        Gère les noms composés comme "Clé USB".
        """
        player = game.player
        l = len(list_of_words)
        
        # Vérifier qu'on a au moins un paramètre
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        # Reconstituer le nom complet de l'objet (tous les mots après la commande)
        item_name_parts = list_of_words[1:]  # Prendre tous les mots après "drop"
        item_name = " ".join(item_name_parts)  # Reconstituer le nom complet
        
        current_room = player.current_room
        
        # Retirer l'objet de l'inventaire du joueur
        item = player.remove_item(item_name)
        if item:
            # Ajouter l'objet à la salle
            current_room.add_item(item)
            return True
        else:
            return False

    def map(game, list_of_words, number_of_parameters):
        """
        Afficher la carte de la fraternité.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        game.show_map()
        return True
