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
            # Afficher l'historique après un retour réussi
            print(player.get_history())
            # Ajout: Afficher aussi le nom de la salle où on revient
            print(f"↩️  Retour à: {player.current_room.name}")
        return success