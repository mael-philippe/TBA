class Player():
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.history = []  # Historique des salles visitées
    
    def move(self, direction):
        next_room = self.current_room.exits[direction]
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Ajouter la salle actuelle à l'historique AVANT de se déplacer
        # (sauf si c'est déjà la dernière salle de l'historique)
        if self.current_room and (not self.history or self.history[-1] != self.current_room):
            self.history.append(self.current_room)
        
        self.current_room = next_room
        
        # Afficher uniquement la description, PAS les sorties
        print(f"\nVous êtes {self.current_room.description}\n")
        
        # Marquer comme visitée
        if not self.current_room.visited:
            self.current_room.visited = True
        
        # Déclencher les événements de la salle
        if hasattr(self.current_room, 'event'):
            self.current_room.event(self)
            # Afficher les sorties APRÈS l'événement
            print(f"\n{self.current_room.get_exit_string()}\n")
        else:
            # Si pas d'événement, afficher les sorties immédiatement
            print(f"\n{self.current_room.get_exit_string()}\n")
        
        return True
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"\n💀 {self.name} est K.O.! Mission échouée...\n")
            return True  # Le joueur est mort
        return False
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        print(f"\n❤️  Santé restaurée de {amount} points! Santé actuelle: {self.health}/{self.max_health}\n")
    
    def add_item(self, item):
        self.inventory.append(item)
        print(f"\n🎒 {item} ajouté à l'inventaire!\n")
    
    def get_history(self):
        """Retourne une chaîne décrivant l'historique des salles visitées"""
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres salles.\n"
        
        history_str = "\nVous avez déjà visité les pièces suivantes:\n"
        for i, room in enumerate(self.history, 1):
            # Utiliser le nom de la salle (room.name) au lieu de la description (room.description)
            history_str += f"    {i}. {room.name}\n"
        return history_str
    
    def go_back(self):
        """Revenir à la salle précédente dans l'historique"""
        if not self.history:
            print("\nImpossible de revenir en arrière : historique vide !\n")
            return False
        
        # Retirer la dernière salle de l'historique
        previous_room = self.history.pop()
        
        # Déplacer le joueur vers la salle précédente
        self.current_room = previous_room
        print(f"\n↩️  Retour en arrière...")
        # Afficher uniquement la description
        print(f"Vous êtes {self.current_room.description}\n")
        
        # Afficher les sorties pour la salle de retour
        print(f"{self.current_room.get_exit_string()}\n")
        
        return True