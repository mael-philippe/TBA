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
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        direction = list_of_words[1].upper()
        if direction not in ["N", "E", "S", "O"]:
            print(f"\nDirection '{direction}' non valide. Les directions possibles sont: N (Nord), E (Est), S (Sud), O (Ouest).\n")
            return False
        
        success = player.move(direction)
        if success:
            # Vérifier les quêtes de type 'room'
            game.quest_manager.check_quest_triggers(player, 'enter', player.current_room.name)
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
            print(player.get_history())
        return success

    def talk(game, list_of_words, number_of_parameters):
        """
        Parler à un personnage.
        Gère les noms composés.
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
        
        success = current_room.interact_with_character(character_name, player)
        if success:
            # Vérifier les quêtes de type 'talk'
            game.quest_manager.check_quest_triggers(player, 'talk', character_name)
        else:
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
        
        print(current_room.get_inventory_string())
        
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        Prendre un objet dans la salle.
        Gère les noms composés comme "Clé USB".
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
                # Vérifier les quêtes de type 'item'
                game.quest_manager.check_quest_triggers(player, 'take', item.name)
                return True
            else:
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
    
    def quests(game, list_of_words, number_of_parameters):
        """Lister toutes les quêtes disponibles."""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        print(game.quest_manager.get_active_quests_string())
        print(game.quest_manager.get_completed_quests_string())
        return True
    
    def quest(game, list_of_words, number_of_parameters):
        """Afficher les détails d'une quête spécifique."""
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        quest_name = " ".join(list_of_words[1:])
        
        for quest in game.quest_manager.quests:
            if quest.name.lower() == quest_name.lower():
                print(f"\n=== {quest.name} ===")
                print(f"Description: {quest.description}")
                print(f"Statut: {'Active' if quest.is_active else 'Inactive'}")
                print(f"Complétée: {'Oui' if quest.is_completed else 'Non'}")
                print(f"Progression: {quest.get_progress()}")
                
                if quest.objectives:
                    print("\nObjectifs:")
                    for obj in quest.objectives:
                        status = "✓" if obj['completed'] else "○"
                        print(f"  {status} {obj['description']}")
                
                if quest.rewards:
                    print("\nRécompenses:")
                    for reward in quest.rewards:
                        print(f"  • {reward['description']}")
                
                print()
                return True
        
        print(f"\n❌ Quête '{quest_name}' non trouvée.\n")
        return False
    
    def activate(game, list_of_words, number_of_parameters):
        """Activer une quête spécifique."""
        player = game.player
        l = len(list_of_words)
        
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        quest_name = " ".join(list_of_words[1:])
        
        if game.quest_manager.activate_quest(quest_name):
            print(f"\n✅ Quête '{quest_name}' activée!\n")
            for quest in game.quest_manager.active_quests:
                if quest.name.lower() == quest_name.lower():
                    print(str(quest))
            return True
        else:
            print(f"\n❌ Impossible d'activer la quête '{quest_name}'.\n")
            return False
    
    def rewards(game, list_of_words, number_of_parameters):
        """Lister toutes les récompenses gagnées."""
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        completed_count = len(game.quest_manager.completed_quests)
        
        print(f"\n=== RÉCOMPENSES ===")
        print(f"Quêtes complétées: {completed_count}/3")
        
        if completed_count == 0:
            print("Aucune récompense gagnée pour le moment.")
        else:
            print("Récompenses gagnées:")
            for i, quest in enumerate(game.quest_manager.completed_quests, 1):
                print(f"  {i}. {quest.name}")
                for reward in quest.rewards:
                    print(f"     • {reward['description']}")
        
        print()
        return True