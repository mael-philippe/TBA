class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.visited = False
        self.characters = []  # Liste des personnages présents dans la salle
        self.event_triggered = False  # Pour certains événements spéciaux
    
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
        """Interagir avec un personnage spécifique"""
        for character in self.characters:
            if character.name.lower() == character_name.lower():
                return character.interact(player)
        return False