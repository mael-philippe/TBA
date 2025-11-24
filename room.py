class Room:
    def __init__(self, name, description, event=None):
        self.name = name
        self.description = description
        self.exits = {}
        self.event = event  # Fonction à exécuter quand le joueur entre
        self.visited = False
    
    def get_long_description(self):
        description = f"\nVous êtes {self.description}\n"
        
        # Afficher un message spécial pour la première visite
        if not self.visited:
            self.visited = True
        
        description += f"\n{self.get_exit_string()}\n"
        return description
    
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string