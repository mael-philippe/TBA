class Room:
    def __init__(self, name, description, event=None):
        self.name = name
        self.description = description
        self.exits = {}
        self.event = event  # Fonction à exécuter quand le joueur entre
        self.visited = False
    
    def get_long_description(self):
        """Retourne la description complète avec les sorties"""
        description = f"\nVous êtes {self.description}\n"
        
        # Afficher un message spécial pour la première visite
        if not self.visited:
            self.visited = True
        
        # NE PAS ajouter les sorties ici - elles seront affichées après les événements
        return description
    
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string