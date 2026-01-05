class Player():
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.history = []
        self.max_weight = 20.0
        self.current_weight = 0.0
        self.earned_rewards = []  # Ajout pour stocker les récompenses
    
    def move(self, direction):
        next_room = self.current_room.exits[direction]
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        if self.current_room and (not self.history or self.history[-1] != self.current_room):
            self.history.append(self.current_room)
        
        self.current_room = next_room
        
        print(self.current_room.get_long_description())
        
        return True
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"\n💀 {self.name} est K.O.! Mission échouée...\n")
            return True
        return False
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        print(f"\n❤️  Santé restaurée de {amount} points! Santé actuelle: {self.health}/{self.max_health}\n")
    
    def get_current_weight(self):
        """Calculer le poids actuel de l'inventaire"""
        self.current_weight = sum(item.weight for item in self.inventory)
        return self.current_weight
    
    def can_take_item(self, item):
        """Vérifier si le joueur peut prendre l'objet"""
        return self.get_current_weight() + item.weight <= self.max_weight
    
    def add_item(self, item):
        """Ajouter un objet à l'inventaire du joueur"""
        if self.can_take_item(item):
            self.inventory.append(item)
            print(f"\n🎒 Vous avez pris '{item.name}'.\n")
            return True
        else:
            print(f"\n❌ Trop lourd! Vous ne pouvez pas prendre '{item.name}'. Poids actuel: {self.get_current_weight()}/{self.max_weight} kg\n")
            return False
    
    def remove_item(self, item_name):
        """Retirer un objet de l'inventaire par son nom (insensible à la casse)"""
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                removed_item = self.inventory.pop(i)
                print(f"\n📦 Vous avez déposé '{removed_item.name}'.\n")
                return removed_item
        print(f"\n❌ L'objet '{item_name}' n'est pas dans votre inventaire.\n")
        return None
    
    def get_item(self, item_name):
        """Récupérer un objet par son nom sans le retirer (insensible à la casse)"""
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None
    
    def get_history(self):
        """Retourne une chaîne décrivant l'historique des salles visitées"""
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres salles.\n"
        
        history_str = "\nVous avez déjà visité les pièces suivantes:\n"
        for i, room in enumerate(self.history, 1):
            history_str += f"    {i}. {room.name}\n"
        return history_str
    
    def go_back(self):
        """Revenir à la salle précédente dans l'historique"""
        if not self.history:
            print("\nImpossible de revenir en arrière : historique vide !\n")
            return False
        
        previous_room = self.history.pop()
        
        self.current_room = previous_room
        print(f"\n↩️  Retour en arrière...")
        print(self.current_room.get_long_description())
        
        return True
    
    def get_inventory_string(self):
        """Retourne une chaîne décrivant l'inventaire du joueur"""
        if not self.inventory:
            return "\n🎒 Votre inventaire est vide.\n"
        
        inventory_str = f"\n🎒 Inventaire ({self.get_current_weight()}/{self.max_weight} kg):\n"
        for i, item in enumerate(self.inventory, 1):
            inventory_str += f"    {i}. {item}\n"
        return inventory_str
    
    def add_reward(self, reward_description):
        """Ajouter une récompense au joueur"""
        self.earned_rewards.append(reward_description)
    
    def get_rewards_string(self):
        """Retourne une chaîne décrivant les récompenses du joueur"""
        if not self.earned_rewards:
            return "\n🎁 Aucune récompense gagnée pour le moment.\n"
        
        rewards_str = "\n🎁 RÉCOMPENSES GAGNÉES:\n"
        for i, reward in enumerate(self.earned_rewards, 1):
            rewards_str += f"    {i}. {reward}\n"
        return rewards_str