class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.visited = False
        self.characters = []  # Liste des personnages présents dans la salle
        self.event_triggered = False  # Pour certains événements spéciaux
        self.inventory = []  # Inventaire des objets dans la salle
    
    def add_character(self, character):
        """Ajouter un personnage à la salle"""
        self.characters.append(character)
    
    def get_long_description(self):
        """Retourne la description complète avec les sorties"""
        description = f"\nVous êtes {self.description}\n"
        
        # Afficher un message spécial pour la première visite
        if not self.visited:
            self.visited = True
        
        # Afficher les personnages présents
        if self.characters:
            description += "\nPersonnes présentes:\n"
            for character in self.characters:
                description += f"  - {character.name}: {character.description}\n"
        
        # Afficher les sorties (elles seront réaffichées après les interactions)
        description += f"\n{self.get_exit_string()}\n"
        return description
    
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string
    
    def reset_event(self):
        """Réinitialiser l'état de l'événement de la salle"""
        self.event_triggered = False
    
    def interact_with_character(self, character_name, player):
        """Interagir avec un personnage spécifique (insensible à la casse)"""
        character_name_lower = character_name.lower()
        for character in self.characters:
            if character.name.lower() == character_name_lower:
                return character.interact(player)
        return False
    
    def get_inventory_string(self):
        """Retourne une chaîne décrivant les objets dans la salle"""
        if not self.inventory:
            return "\nIl n'y a rien ici.\n"
        
        inventory_str = "\nObjets dans la salle:\n"
        for i, item in enumerate(self.inventory, 1):
            inventory_str += f"    {i}. {item}\n"
        return inventory_str
    
    def add_item(self, item):
        """Ajouter un objet à la salle"""
        self.inventory.append(item)
    
    def remove_item(self, item_name):
        """Retirer un objet de la salle par son nom (insensible à la casse)"""
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                return self.inventory.pop(i)
        return None
    
    def get_item(self, item_name):
        """Récupérer un objet par son nom sans le retirer (insensible à la casse)"""
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None