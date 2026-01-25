"""
Module du joueur.
"""


class Player:
    """
    Représente le joueur dans le jeu.
    
    Le joueur est l'entité contrôlée par l'utilisateur. Il peut se déplacer
    entre les salles, collecter des objets, interagir avec des personnages
    et accomplir des quêtes.
    
    Attributes:
        name (str): Nom du joueur
        current_room (Room): Salle actuelle du joueur
        game (Game): Référence au jeu principal
        health (int): Points de vie actuels
        max_health (int): Points de vie maximum
        inventory (list): Liste des objets portés
        history (list): Historique des salles visitées
        max_weight (float): Poids maximum portable
        current_weight (float): Poids actuellement porté
        earned_rewards (list): Récompenses obtenues
        visited_locations (dict): Suivi des lieux pour la quête d'exploration
        collected_items (dict): Suivi des objets pour la quête de collection
        explorer_quest_given (bool): Si la quête d'exploration a été donnée
        collector_quest_given (bool): Si la quête de collection a été donnée
    
    Methods:
        __init__(name, game=None): Initialise un nouveau joueur
        move(direction): Déplace le joueur dans une direction
        take_damage(amount): Inflige des dégâts au joueur
        heal(amount): Soigne le joueur
        get_current_weight(): Calcule le poids actuel de l'inventaire
        can_take_item(item): Vérifie si le joueur peut prendre un objet
        add_item(item): Ajoute un objet à l'inventaire
        remove_item(item_name): Retire un objet de l'inventaire
        get_item(item_name): Récupère un objet par son nom sans le retirer
        get_history(): Retourne l'historique des salles visitées
        go_back(): Reviens à la salle précédente
        get_inventory_string(): Retourne une représentation de l'inventaire
        has_item(item_name): Vérifie si le joueur possède un objet
        get_status_summary(): Retourne un résumé des catégories d'objets
        get_progress_string(): Retourne la progression des quêtes spéciales
    
    Exceptions:
        Aucune exception n'est levée directement par cette classe.
    
    Examples:
        >>> from player import Player
        >>> from game import Game
        >>> joueur = Player("Alex", None)
        >>> print(joueur.name)
        Alex
        >>> print(joueur.health)
        100
        >>> print(joueur.inventory)
        []
        >>> print(joueur.max_weight)
        5.0
    """
    
    def __init__(self, name, game=None):
        """
        Initialise un nouveau joueur.
        
        Args:
            name (str): Nom du joueur
            game (Game, optional): Référence au jeu. Defaults to None.
        """
        self.name = name
        self.current_room = None
        self.game = game
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.history = []
        self.max_weight = 5.0
        self.current_weight = 0.0
        self.earned_rewards = []
        
        # Suivi pour la quête "L'Explorateur Intrépide"
        self.visited_locations = {
            "Cave": False,
            "Observatoire": False,
            "Sauna": False,
            "Terrasse": False
        }
        
        # Suivi pour la quête "Le Collectionneur"
        self.collected_items = {
            "RedBull": False,
            "Part de pizza": False,
            "Bouteille de vin": False
        }
        
        # Flags pour les quêtes données
        self.explorer_quest_given = False
        self.collector_quest_given = False
    
    def move(self, direction):
        """
        Déplace le joueur dans une direction.
        
        Args:
            direction (str): Direction (N/E/S/O/U/D)
            
        Returns:
            bool: True si le déplacement a réussi
        """
        # Vérifier si la direction existe
        if direction not in self.current_room.exits:
            print(f"\n🚫 Il n'y a pas de sortie vers {direction} !\n")
            return False
            
        next_room = self.current_room.exits[direction]
        
        # Vérifier si la sortie est accessible
        if next_room is None:
            print("\n🚫 La porte est verrouillée ou inexistante !\n")
            return False
        
        # Ajouter la salle actuelle à l'historique
        if self.current_room and (not self.history or self.history[-1] != self.current_room):
            self.history.append(self.current_room)
        
        # Effectuer le déplacement
        self.current_room = next_room
        
        # Vérifier si le joueur entre dans le bureau du président
        if self.current_room.name == "Bureau du Président":
            victory = self._handle_president_encounter()
            if victory:
                # Terminer le jeu
                if self.game:
                    self.game.finished = True
            return True
        
        # Vérifier les quêtes de salle
        self._check_explorer_quest()
        
        # Afficher la nouvelle salle
        print(self.current_room.get_long_description())
        
        return True

    def _handle_president_encounter(self):
        """
        Gère la rencontre avec le président et vérifie la victoire.
        
        Returns:
            bool: True si le joueur a gagné
        """
        print("\n" + "="*50)
        print("BUREAU DU PRÉSIDENT DE L'UNIVERSITÉ")
        print("="*50)
        
        # Compter les quêtes complétées
        completed_count = 0
        
        # Méthode 1: Via le gestionnaire de quêtes
        if self.game and hasattr(self.game, 'quest_manager'):
            completed_count = len(self.game.quest_manager.completed_quests)
        
        # Méthode 2: Via les objets trophées
        if completed_count == 0:
            quest_items = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                          "Documents", "Réponses aux examens"]
            completed_count = sum(1 for item in self.inventory if item.name in quest_items)
        
        print(f"\n👔 Le Président vous regarde par-dessus ses lunettes.")
        print("« Alors, voyons ce que vous avez accompli... »")
        print(f"« Je vois que vous avez complété {completed_count} quêtes sur 5 possibles. »")
        
        if completed_count >= 4:
            print("\n🏆 « IMPRESSIONNANT ! »")
            print("« Vous avez prouvé votre valeur au sein de la fraternité Mystik. »")
            print("« Non seulement vous validez votre année, mais vous êtes nommé(e) président(e) ! »")
            print("\n" + "✨"*20 + " VICTOIRE ! " + "✨"*20)
            return True
        else:
            print("\n❌ « DÉSOLANT... »")
            print(f"« Seulement {completed_count} quêtes ? Vous n'êtes pas à la hauteur. »")
            print("« Revenez quand vous aurez accompli au moins 4 quêtes. »")
            print("\n💡 Conseil: Tapez 'quests' pour voir vos progrès.")
            return False
    
    def _check_explorer_quest(self):
        """Vérifie la progression de la quête 'L'Explorateur Intrépide'."""
        if not self.current_room:
            return
        
        current_room_name = self.current_room.name
        
        # Vérifier si c'est une salle de la quête
        if current_room_name in self.visited_locations:
            if not self.visited_locations[current_room_name]:
                self.visited_locations[current_room_name] = True
                print(f"\n🎯 Progression 'Explorateur': {current_room_name} visité !")
                
                # Compter les salles visitées
                visited_count = sum(1 for visited in self.visited_locations.values() if visited)
                total_count = len(self.visited_locations)
                print(f"   {visited_count}/{total_count} lieux explorés")
                
                # Vérifier si la quête est complète
                if visited_count == total_count and self.game:
                    self._complete_explorer_quest()
    
    def _check_collector_quest(self):
        """Vérifie la progression de la quête 'Le Collectionneur'."""
        # Vérifier si le joueur a les objets requis
        has_redbull = self.has_item("RedBull")
        has_pizza = self.has_item("Part de pizza")
        has_vin = self.has_item("Bouteille de vin")
        
        # Mettre à jour l'état
        self.collected_items["RedBull"] = has_redbull
        self.collected_items["Part de pizza"] = has_pizza
        self.collected_items["Bouteille de vin"] = has_vin
        
        # Compter les objets collectés
        collected_count = sum(1 for collected in self.collected_items.values() if collected)
        total_count = len(self.collected_items)
        
        if collected_count == total_count and self.game:
            self._complete_collector_quest()
    
    def _complete_explorer_quest(self):
        """Complète la quête 'L'Explorateur Intrépide'."""
        print("\n" + "="*50)
        print("✅ QUÊTE 'L'EXPLORATEUR INTRÉPIDE' COMPLÉTÉE !")
        print("="*50)
        print("Vous avez exploré les 4 coins extrêmes du campus !")
        
        # Donner la récompense
        from item import Item
        reward = Item("Carte du campus", "révèle toutes les sorties avec descriptions", 0.1)
        
        if self.can_take_item(reward):
            self.inventory.append(reward)
            print(f"\n🎁 RÉCOMPENSE: {reward.name} !")
            print("   (Utilisez 'look' pour voir ses effets)")
        else:
            print(f"\n💔 Pas de place pour {reward.name} !")
        
        # Marquer la quête comme complétée
        if self.game and hasattr(self.game, 'quest_manager'):
            for quest in self.game.quest_manager.quests:
                if quest.name == "L'Explorateur Intrépide":
                    quest.complete(success=True)
                    if quest in self.game.quest_manager.active_quests:
                        self.game.quest_manager.active_quests.remove(quest)
                    self.game.quest_manager.completed_quests.append(quest)
                    break
    
    def _complete_collector_quest(self):
        """Complète la quête 'Le Collectionneur'."""
        print("\n" + "="*50)
        print("✅ QUÊTE 'LE COLLECTIONNEUR' COMPLÉTÉE !")
        print("="*50)
        print("Vous avez rassemblé les 3 objets de confort !")
        
        # Donner la récompense
        from item import Item
        reward = Item("Coffre de rangement", "augmente votre capacité de 2kg", 1.0)
        
        # Augmenter la capacité
        old_max = self.max_weight
        self.max_weight += 2.0
        
        if self.can_take_item(reward):
            self.inventory.append(reward)
            print(f"\n🎁 RÉCOMPENSE: {reward.name} !")
            print(f"   Capacité augmentée: {old_max}kg → {self.max_weight}kg")
        else:
            print(f"\n💔 Pas de place pour {reward.name} !")
            print(f"   Mais votre capacité augmente quand même: {old_max}kg → {self.max_weight}kg")
        
        # Marquer la quête comme complétée
        if self.game and hasattr(self.game, 'quest_manager'):
            for quest in self.game.quest_manager.quests:
                if quest.name == "Le Collectionneur":
                    quest.complete(success=True)
                    if quest in self.game.quest_manager.active_quests:
                        self.game.quest_manager.active_quests.remove(quest)
                    self.game.quest_manager.completed_quests.append(quest)
                    break
    
    def add_reward(self, reward_description):
        """
        Ajoute une récompense au joueur.
        
        Args:
            reward_description (str): Description de la récompense
        """
        self.earned_rewards.append(reward_description)
        print(f"   (Note: '{reward_description}' ajouté à vos accomplissements)")
    
    def take_damage(self, amount):
        """
        Inflige des dégâts au joueur.
        
        Args:
            amount (int): Nombre de points de vie perdus
            
        Returns:
            bool: True si le joueur est mort
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"\n💀 {self.name} est K.O.!")
            return True
        print(f"\n❤️  Vous perdez {amount} points de vie. Santé: {self.health}/{self.max_health}")
        return False
    
    def heal(self, amount):
        """
        Soigne le joueur.
        
        Args:
            amount (int): Nombre de points de vie restaurés
            
        Returns:
            int: Nombre de points réellement restaurés
        """
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        healed = self.health - old_health
        print(f"\n❤️  Santé restaurée de {healed} points! Santé: {self.health}/{self.max_health}")
        return healed
    
    def get_current_weight(self):
        """
        Calcule le poids actuel de l'inventaire.
        
        Returns:
            float: Poids total des objets portés
        """
        return sum(item.weight for item in self.inventory)
    
    def can_take_item(self, item):
        """
        Vérifie si le joueur peut prendre un objet.
        
        Args:
            item (Item): Objet à vérifier
            
        Returns:
            bool: True si le joueur peut prendre l'objet
        """
        return self.get_current_weight() + item.weight <= self.max_weight
    
    def add_item(self, item):
        """
        Ajoute un objet à l'inventaire.
        
        Args:
            item (Item): Objet à ajouter
            
        Returns:
            bool: True si l'objet a été ajouté
        """
        if self.can_take_item(item):
            self.inventory.append(item)
            print(f"\n🎒 Vous avez pris '{item.name}'.")
            print(f"   Poids: {self.get_current_weight():.1f}/{self.max_weight} kg")
            
            # Vérifier la quête de collection
            self._check_collector_quest()
            
            return True
        else:
            print(f"\n❌ Trop lourd! Impossible de prendre '{item.name}'.")
            print(f"   Poids actuel: {self.get_current_weight():.1f}/{self.max_weight} kg")
            print(f"   Poids de l'objet: {item.weight:.1f} kg")
            print(f"   L'objet reste dans la salle.")
            return False
    
    def remove_item(self, item_name):
        """
        Retire un objet de l'inventaire.
        
        Args:
            item_name (str): Nom de l'objet à retirer
            
        Returns:
            Item or None: L'objet retiré, ou None s'il n'existe pas
        """
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                removed_item = self.inventory.pop(i)
                print(f"\n📦 Vous avez déposé '{removed_item.name}'.")
                
                # Vérifier la quête de collection
                self._check_collector_quest()
                
                return removed_item
        print(f"\n❌ L'objet '{item_name}' n'est pas dans votre inventaire.")
        return None
    
    def get_item(self, item_name):
        """
        Récupère un objet par son nom sans le retirer.
        
        Args:
            item_name (str): Nom de l'objet
            
        Returns:
            Item or None: L'objet trouvé, ou None s'il n'existe pas
        """
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None
    
    def get_history(self):
        """
        Retourne l'historique des salles visitées.
        
        Returns:
            str: Historique formaté
        """
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres salles.\n"
        
        history_str = "\n📜 Historique des salles visitées:\n"
        for i, room in enumerate(self.history, 1):
            history_str += f"    {i}. {room.name}\n"
        return history_str
    
    def go_back(self):
        """
        Reviens à la salle précédente.
        
        Returns:
            bool: True si le retour a réussi
        """
        if not self.history:
            print("\n❌ Impossible de revenir en arrière: historique vide!")
            return False
        
        previous_room = self.history.pop()
        self.current_room = previous_room
        
        print(f"\n↩️  Retour en arrière...")
        print(self.current_room.get_long_description())
        return True
    
    def get_inventory_string(self):
        """
        Retourne une représentation de l'inventaire par catégories.
        
        Returns:
            str: Inventaire formaté
        """
        if not self.inventory:
            return "\n🎒 Votre inventaire est vide.\n"
        
        # Définir les catégories d'objets
        trophies = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                    "Documents", "Réponses aux examens"]
        powers = ["GPS", "Chien"]
        consumables = ["RedBull", "Part de pizza"]
        specials = ["Carte du campus", "Coffre de rangement"]
        
        # Trier les objets
        trophy_items = []
        power_items = []
        consumable_items = []
        special_items = []
        other_items = []
        
        for item in self.inventory:
            if item.name in trophies:
                trophy_items.append(item)
            elif item.name in powers:
                power_items.append(item)
            elif item.name in consumables:
                consumable_items.append(item)
            elif item.name in specials:
                special_items.append(item)
            else:
                other_items.append(item)
        
        # Construire l'affichage
        inventory_str = f"\n🎒 INVENTAIRE ({self.get_current_weight():.1f}/{self.max_weight} kg):\n"
        
        # Afficher par catégories
        if trophy_items:
            inventory_str += "\n🏆 TROPHÉES (pour gagner):\n"
            for i, item in enumerate(trophy_items, 1):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if power_items:
            inventory_str += "\n🔧 OUTILS SPÉCIAUX:\n"
            start_idx = len(trophy_items) + 1
            for i, item in enumerate(power_items, start_idx):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if special_items:
            inventory_str += "\n🎁 RÉCOMPENSES DE QUÊTES:\n"
            start_idx = len(trophy_items) + len(power_items) + 1
            for i, item in enumerate(special_items, start_idx):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if consumable_items:
            inventory_str += "\n🍖 CONSOMMABLES (soins):\n"
            start_idx = len(trophy_items) + len(power_items) + len(special_items) + 1
            for i, item in enumerate(consumable_items, start_idx):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if other_items:
            inventory_str += "\n📦 AUTRES OBJETS:\n"
            start_idx = len(trophy_items) + len(power_items) + len(special_items) + len(consumable_items) + 1
            for i, item in enumerate(other_items, start_idx):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        # Ajouter un résumé
        inventory_str += f"\n📊 Résumé: {len(self.inventory)} objets"
        if trophy_items:
            inventory_str += f" | 🏆 Trophées: {len(trophy_items)}/5"
        if power_items:
            inventory_str += f" | 🔧 Outils: {len(power_items)}"
        if special_items:
            inventory_str += f" | 🎁 Récompenses: {len(special_items)}"
        if consumable_items:
            inventory_str += f" | 🍖 Soins: {len(consumable_items)}"
        
        return inventory_str
    
    def has_item(self, item_name):
        """
        Vérifie si le joueur possède un objet.
        
        Args:
            item_name (str): Nom de l'objet
            
        Returns:
            bool: True si le joueur possède l'objet
        """
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def get_status_summary(self):
        """
        Retourne un résumé des catégories d'objets possédés.
        
        Returns:
            str: Résumé formaté
        """
        trophies = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                    "Documents", "Réponses aux examens"]
        powers = ["GPS", "Chien"]
        consumables = ["RedBull", "Part de pizza"]
        specials = ["Carte du campus", "Coffre de rangement"]
        
        # Compter les objets par catégorie
        trophy_count = sum(1 for item in self.inventory if item.name in trophies)
        power_count = sum(1 for item in self.inventory if item.name in powers)
        consumable_count = sum(1 for item in self.inventory if item.name in consumables)
        special_count = sum(1 for item in self.inventory if item.name in specials)
        
        summary = f"🎒 Inventaire: {len(self.inventory)} objets"
        
        if trophy_count > 0:
            summary += f" | 🏆 Trophées: {trophy_count}/5"
        if power_count > 0:
            summary += f" | 🔧 Outils: {power_count}"
        if special_count > 0:
            summary += f" | 🎁 Récompenses: {special_count}"
        if consumable_count > 0:
            summary += f" | 🍖 Consommables: {consumable_count}"
        
        return summary
    
    def get_progress_string(self):
        """
        Retourne la progression des quêtes spéciales.
        
        Returns:
            str: Progression formatée
        """
        result = "\n" + "="*50 + "\n"
        result += "PROGRESSION DES QUÊTES SPÉCIALES\n"
        result += "="*50 + "\n"
        
        # Quête d'exploration
        result += "\n🌍 L'Explorateur Intrépide:\n"
        visited_count = 0
        for location, visited in self.visited_locations.items():
            status = "✓" if visited else "○"
            result += f"   {status} {location}\n"
            if visited:
                visited_count += 1
        result += f"   Progression: {visited_count}/4 lieux\n"
        
        # Quête de collection
        result += "\n🎒 Le Collectionneur:\n"
        collected_count = 0
        for item_name, collected in self.collected_items.items():
            # Vérifier si le joueur a réellement l'objet
            has_item = self.has_item(item_name)
            status = "✓" if has_item else "○"
            result += f"   {status} {item_name}\n"
            if has_item:
                collected_count += 1
        result += f"   Progression: {collected_count}/3 objets\n"
        
        # Quêtes proposées
        result += "\n📜 Quêtes proposées:\n"
        if self.explorer_quest_given:
            result += "   ✓ Explorateur Intrépide (par le Garde)\n"
        else:
            result += "   ○ Explorateur Intrépide (parle au Garde)\n"
            
        if self.collector_quest_given:
            result += "   ✓ Le Collectionneur (par l'Ivre)\n"
        else:
            result += "   ○ Le Collectionneur (parle à l'Ivre)\n"
        
        return result