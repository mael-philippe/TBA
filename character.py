class Character:
    def __init__(self, name, description, interaction_event=None):
        self.name = name
        self.description = description
        self.interaction_event = interaction_event  # Fonction d'interaction
        self.already_interacted = False  # Pour éviter les interactions répétées
    
    def interact(self, player):
        """Interagir avec le personnage"""
        if self.interaction_event:
            if not self.already_interacted:
                result = self.interaction_event(player)
                self.already_interacted = True
                return result
            else:
                print(f"\nVous avez déjà parlé à {self.name}.\n")
                return False
        else:
            print(f"\n{self.name} ne semble pas intéressé à parler.\n")
            return False
    
    def reset_interaction(self):
        """Réinitialiser l'état d'interaction"""
        self.already_interacted = False