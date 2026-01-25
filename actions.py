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
        
        # Utiliser le nouveau résumé au lieu du simple comptage
        print(player.get_status_summary())
        
        print(f"⚖️  Poids: {player.get_current_weight():.1f}/{player.max_weight} kg")
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
        
        item = current_room.get_item(item_name)  # ← MODIFIÉ : get_item() au lieu de remove_item()
        if item:
            # Vérifier d'abord si le joueur peut prendre l'objet
            if player.can_take_item(item):
                # Si oui, retirer de la salle et ajouter à l'inventaire
                current_room.remove_item(item_name)
                player.add_item(item)
                return True
            else:
                # Si non, laisser dans la salle et afficher message
                print(f"\n❌ Trop lourd! Impossible de prendre '{item.name}'.")
                print(f"   Poids actuel: {player.get_current_weight():.1f}/{player.max_weight} kg")
                print(f"   Poids de l'objet: {item.weight:.1f} kg")
                print(f"   L'objet '{item.name}' reste dans la salle.")
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
        Utiliser un objet de l'inventaire (ex: use GPS, use Chien, use RedBull).
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
            print("\n📡 --- ACTIVATION DU GPS --- 📡")
            print("TRIANGULATION DES SIGNAUX...\n")
            
            # Séparer les PNJ par distance
            pnj_ici = []
            pnj_ailleurs = []
            
            for char in game.characters:
                if char.current_room:
                    if char.current_room == player.current_room:
                        pnj_ici.append(char.name)
                    else:
                        pnj_ailleurs.append((char.name, char.current_room.name))
            
            # Afficher d'abord ceux qui sont ici
            if pnj_ici:
                print("🎯 PNJ DANS VOTRE SALLE:")
                for name in pnj_ici:
                    print(f"  👤 {name} (vous le voyez)")
                print()
            
            # Puis ceux qui sont ailleurs
            if pnj_ailleurs:
                print("📡 PNJ À DISTANCE:")
                for name, room in pnj_ailleurs:
                    print(f"  📍 {name} — {room}")
                print()
            
            # Résumé
            total = len(pnj_ici) + len(pnj_ailleurs)
            if total == 0:
                print("  (Aucun signal détecté)")
            else:
                print(f"📊 {total} PNJ localisés")
            
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
        
        # --- EFFET DU REDBULL ---
        elif item_to_use.name == "RedBull":
            print("\n⚡ --- BOISSON ÉNERGISANTE --- ⚡")
            
            # Vérifier si le joueur est déjà en pleine santé
            if player.health >= player.max_health:
                print("💪 Vous êtes déjà en pleine forme !")
                print("(Vous gardez votre RedBull pour plus tard.)")
                return False
            
            # Calculer la quantité de soin
            heal_amount = 30
            old_health = player.health
            player.health = min(player.health + heal_amount, player.max_health)
            actual_heal = player.health - old_health
            
            # Retirer l'objet de l'inventaire
            player.remove_item("RedBull")
            
            print(f"💚 Vous buvez le RedBull et récupérez {actual_heal} PV !")
            print(f"❤️  Santé: {player.health}/{player.max_health}")
            
            if actual_heal < heal_amount:
                print("(Vous étiez presque en pleine santé.)")
            
            return True
        
        # --- EFFET DE LA PART DE PIZZA ---
        elif item_to_use.name == "Part de pizza":
            print("\n🍕 --- RESTAURANT ITALIEN --- 🍕")
            
            # Vérifier si le joueur est déjà en pleine santé
            if player.health >= player.max_health:
                print("🍽️  Vous êtes déjà rassasié !")
                print("(Vous gardez votre pizza pour plus tard.)")
                return False
            
            # Calculer la quantité de soin
            heal_amount = 50
            old_health = player.health
            player.health = min(player.health + heal_amount, player.max_health)
            actual_heal = player.health - old_health
            
            # Retirer l'objet de l'inventaire
            player.remove_item("Part de pizza")
            
            print(f"💚 Vous mangez la part de pizza et récupérez {actual_heal} PV !")
            print(f"❤️  Santé: {player.health}/{player.max_health}")
            
            if actual_heal < heal_amount:
                print("(Vous étiez presque en pleine santé.)")
            
            return True
        
        # --- EFFET DES TROPHÉES (optionnel - juste pour l'affichage) ---
        elif item_to_use.name in ["Manette dorée", "Bouteille de vin", "Clé USB", 
                                "Documents", "Réponses aux examens"]:
            print(f"\n🏆 Vous examinez votre trophée : {item_to_use.name}")
            print(f"📝 {item_to_use.description}")
            print("(Cet objet vous sera utile pour prouver votre valeur au président.)")
            return True
            
        # --- AUTRES OBJETS ---
        else:
            print(f"\n🤔 Vous ne savez pas comment utiliser '{item_to_use.name}' ici.")
            print("(Essayez dans une autre situation ou avec un autre personnage.)")
            return False