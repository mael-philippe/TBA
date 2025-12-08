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
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

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
        if player.health < 30:
            print("⚠️  Attention: Santé critique!")
        print()
        return True

    def inventory(game, list_of_words, number_of_parameters):
        """Afficher l'inventaire du joueur"""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        if player.inventory:
            print(f"\n🎒 Inventaire de {player.name}:")
            for item in player.inventory:
                print(f"   - {item}")
        else:
            print(f"\n🎒 {player.name} n'a aucun objet dans l'inventaire.")
        print()
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
        """
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        character_name = list_of_words[1]
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
        Regarder autour de soi (pour les événements sans personnage).
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        current_room = player.current_room
        
        # Événements spéciaux pour certaines salles quand on utilise "look"
        room_name = current_room.name
        
        if room_name == "Cuisine" and not current_room.event_triggered:
            cuisine_look_event(player)
            current_room.event_triggered = True
            return True
        elif room_name == "Dortoir" and not current_room.event_triggered:
            dortoir_look_event(player)
            current_room.event_triggered = True
            return True
        elif room_name == "Bureau du président" and not current_room.event_triggered:
            bureau_president_look_event(player)
            current_room.event_triggered = True
            return True
        elif room_name == "Toit" and not current_room.event_triggered:
            toit_look_event(player)
            current_room.event_triggered = True
            return True
        else:
            print("\nVous regardez autour de vous...")
            print(current_room.get_long_description())
            return True