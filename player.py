class Player():
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.history = []
        self.max_weight = 5.0
        self.current_weight = 0.0
        self.earned_rewards = []
    
    def move(self, direction):
        # Vérifie si la direction existe dans les sorties de la salle actuelle
        if direction not in self.current_room.exits:
            print(f"\n🚫 Il n'y a pas de sortie vers {direction} !\n")
            return False
            
        next_room = self.current_room.exits[direction]
        
        # Vérifie si la sortie est un "mur" (None)
        if next_room is None:
            print("\n🚫 La porte est verrouillée ou inexistante !\n")
            return False
        
        # Gestion de l'historique
        if self.current_room and (not self.history or self.history[-1] != self.current_room):
            self.history.append(self.current_room)
        
        # --- LE DÉPLACEMENT SE FAIT ICI ---
        self.current_room = next_room
        
        # AJOUT: Vérifier si le joueur entre dans le bureau du président
        if self.current_room.name == "Bureau du Président":
            self._handle_president_encounter()
            return True  # On continue quand même l'affichage
        
        # Affichage de la nouvelle salle
        print(self.current_room.get_long_description())
        
        return True

    def _handle_president_encounter(self):
        """Déclenche la rencontre avec le président"""
        print("\n" + "="*50)
        print("BUREAU DU PRÉSIDENT DE L'UNIVERSITÉ")
        print("="*50)
        
        # Liste des objets de quête (trophées)
        quest_items = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                    "Documents", "Réponses aux examens"]
        
        # Compter combien le joueur en a
        trophies_count = sum(1 for item in self.inventory if item.name in quest_items)
        
        print(f"\n👔 Le Président vous regarde par-dessus ses lunettes.")
        print("« Alors, jeune homme/jeune femme, voyons votre dossier... »")
        print(f"« Je vois que vous avez collecté {trophies_count} trophées sur 5 possibles. »")
        
        if trophies_count >= 4:
            print("\n🏆 « IMPRESSIONNANT ! »")
            print("« Vous avez prouvé votre valeur au sein de la fraternité Mystik. »")
            print("« Non seulement vous validez votre année, mais vous êtes nommé(e) président(e) ! »")
            print("\n" + "✨"*20 + " VICTOIRE ! " + "✨"*20)
            
            # Forcer la victoire (vous devrez gérer ça côté Game)
            return True
        else:
            print("\n❌ « DÉSOLANT... »")
            print(f"« Seulement {trophies_count} trophées ? Vous n'êtes pas à la hauteur. »")
            print("« Vous êtes renvoyé(e) de l'université pour manque de résultats. »")
            print("\n" + "💀"*20 + " DÉFAITE ! " + "💀"*20)
            
            # Forcer la défaite
            self.health = 0
            return False
        
    def add_reward(self, reward_description):
            """Ajouter une récompense au joueur"""
            self.earned_rewards.append(reward_description)
            print(f"   (Note: '{reward_description}' ajouté à vos accomplissements)")
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"\n💀 {self.name} est K.O.!")
            return True
        print(f"\n❤️  Vous perdez {amount} points de vie. Santé: {self.health}/{self.max_health}")
        return False
    
    def heal(self, amount):
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        healed = self.health - old_health
        print(f"\n❤️  Santé restaurée de {healed} points! Santé: {self.health}/{self.max_health}")
        return healed
    
    def get_current_weight(self):
        """Calculer le poids actuel de l'inventaire"""
        return sum(item.weight for item in self.inventory)
    
    def can_take_item(self, item):
        """Vérifier si le joueur peut prendre l'objet"""
        return self.get_current_weight() + item.weight <= self.max_weight
    
    def add_item(self, item):
        """Ajouter un objet à l'inventaire du joueur"""
        if self.can_take_item(item):
            self.inventory.append(item)
            print(f"\n🎒 Vous avez pris '{item.name}'.")
            print(f"   Poids: {self.get_current_weight():.1f}/{self.max_weight} kg")
            return True
        else:
            print(f"\n❌ Trop lourd! Impossible de prendre '{item.name}'.")
            print(f"   Poids actuel: {self.get_current_weight():.1f}/{self.max_weight} kg")
            print(f"   Poids de l'objet: {item.weight:.1f} kg")
            print(f"   L'objet reste dans la salle.")
            return False  # IMPORTANT : Retourner False pour que l'objet ne soit pas retiré de la salle
    
    def remove_item(self, item_name):
        """Retirer un objet de l'inventaire par son nom"""
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                removed_item = self.inventory.pop(i)
                print(f"\n📦 Vous avez déposé '{removed_item.name}'.")
                return removed_item
        print(f"\n❌ L'objet '{item_name}' n'est pas dans votre inventaire.")
        return None
    
    def get_item(self, item_name):
        """Récupérer un objet par son nom sans le retirer"""
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None
    
    def get_history(self):
        """Retourne une chaîne décrivant l'historique"""
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres salles.\n"
        
        history_str = "\n📜 Historique des salles visitées:\n"
        for i, room in enumerate(self.history, 1):
            history_str += f"    {i}. {room.name}\n"
        return history_str
    
    def go_back(self):
        """Revenir à la salle précédente dans l'historique"""
        if not self.history:
            print("\n❌ Impossible de revenir en arrière: historique vide!")
            return False
        
        previous_room = self.history.pop()
        self.current_room = previous_room
        
        print(f"\n↩️  Retour en arrière...")
        print(self.current_room.get_long_description())
        return True
    
    def get_inventory_string(self):
        """Retourne une chaîne décrivant l'inventaire par catégories"""
        if not self.inventory:
            return "\n🎒 Votre inventaire est vide.\n"
        
        # Définir les catégories
        trophies = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                    "Documents", "Réponses aux examens"]
        powers = ["GPS", "Chien"]
        consumables = ["RedBull", "Part de pizza"]
        
        # Trier les objets par catégories
        trophy_items = []
        power_items = []
        consumable_items = []
        other_items = []
        
        for item in self.inventory:
            if item.name in trophies:
                trophy_items.append(item)
            elif item.name in powers:
                power_items.append(item)
            elif item.name in consumables:
                consumable_items.append(item)
            else:
                other_items.append(item)
        
        # Construire l'affichage
        inventory_str = f"\n🎒 INVENTAIRE ({self.get_current_weight():.1f}/{self.max_weight} kg):\n"
        
        # Afficher par catégories avec des titres
        if trophy_items:
            inventory_str += "\n🏆 TROPHÉES (pour gagner):\n"
            for i, item in enumerate(trophy_items, 1):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if power_items:
            inventory_str += "\n🔧 OUTILS SPÉCIAUX:\n"
            for i, item in enumerate(power_items, len(trophy_items) + 1):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if consumable_items:
            inventory_str += "\n🍖 CONSOMMABLES (soins):\n"
            start_index = len(trophy_items) + len(power_items) + 1
            for i, item in enumerate(consumable_items, start_index):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        if other_items:
            inventory_str += "\n📦 AUTRES OBJETS:\n"
            start_index = len(trophy_items) + len(power_items) + len(consumable_items) + 1
            for i, item in enumerate(other_items, start_index):
                inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        
        # Ajouter un résumé en bas
        inventory_str += f"\n📊 Résumé: {len(self.inventory)} objets"
        if trophy_items:
            inventory_str += f" | 🏆 Trophées: {len(trophy_items)}/5"
        if power_items:
            inventory_str += f" | 🔧 Outils: {len(power_items)}"
        if consumable_items:
            inventory_str += f" | 🍖 Soins: {len(consumable_items)}"
        
        return inventory_str
    
    def has_item(self, item_name):
        """Vérifie si le joueur possède un objet"""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def get_status_summary(self):
        """Retourne un résumé des catégories d'objets"""
        trophies = ["Manette dorée", "Bouteille de vin", "Clé USB", 
                    "Documents", "Réponses aux examens"]
        powers = ["GPS", "Chien"]
        consumables = ["RedBull", "Part de pizza"]
        
        # Compter
        trophy_count = sum(1 for item in self.inventory if item.name in trophies)
        power_count = sum(1 for item in self.inventory if item.name in powers)
        consumable_count = sum(1 for item in self.inventory if item.name in consumables)
        
        summary = f"🎒 Inventaire: {len(self.inventory)} objets"
        
        if trophy_count > 0:
            summary += f" | 🏆 Trophées: {trophy_count}/5"
        if power_count > 0:
            summary += f" | 🔧 Outils: {power_count}"
        if consumable_count > 0:
            summary += f" | 🍖 Consommables: {consumable_count}"
        
        return summary