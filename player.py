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
            
            # Affichage de la nouvelle salle
            print(self.current_room.get_long_description())
            
            return True
        
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
            print(f"   Poids: {self.get_current_weight()}/{self.max_weight} kg")
            return True
        else:
            print(f"\n❌ Trop lourd! Impossible de prendre '{item.name}'.")
            print(f"   Poids actuel: {self.get_current_weight()}/{self.max_weight} kg")
            return False
    
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
        """Retourne une chaîne décrivant l'inventaire"""
        if not self.inventory:
            return "\n🎒 Votre inventaire est vide.\n"
        
        inventory_str = f"\n🎒 INVENTAIRE ({self.get_current_weight()}/{self.max_weight} kg):\n"
        for i, item in enumerate(self.inventory, 1):
            inventory_str += f"    {i}. {item}\n"
        
        # Afficher les objets importants
        important_items = [item for item in self.inventory 
                          if item.name in ["Documents", "Clé USB", "Livre"]]
        if important_items:
            inventory_str += "\n💎 PREUVES IMPORTANTES:\n"
            for item in important_items:
                inventory_str += f"    • {item.name}\n"
        
        return inventory_str
    
    def has_item(self, item_name):
        """Vérifie si le joueur possède un objet"""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)