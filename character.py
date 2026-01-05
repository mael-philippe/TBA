class Character:
    def __init__(self, name, description, interaction_event=None, position=None, movement_pattern=None):
        self.name = name
        self.description = description
        self.interaction_event = interaction_event  # Fonction d'interaction
        self.already_interacted = False  # Pour éviter les interactions répétées
        self.position = position  # Position actuelle dans la map (coordonnées x, y ou référence à une salle)
        self.movement_pattern = movement_pattern  # Modèle de déplacement (ex: "random", "patrol", "static")
        self.current_target = None  # Cible actuelle pour le déplacement
        self.move_cooldown = 0  # Cooldown pour les déplacements
        self.dialogue_options = {}  # Options de dialogue supplémentaires
    
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
    
    def update_position(self, game_map, player_position=None):
        """Mettre à jour la position du PNJ selon son modèle de déplacement"""
        if self.movement_pattern == "random":
            self._move_random(game_map)
        elif self.movement_pattern == "patrol" and self.current_target:
            self._move_to_target(game_map, self.current_target)
        elif self.movement_pattern == "follow" and player_position:
            self._follow_player(game_map, player_position)
    
    def _move_random(self, game_map):
        """Déplacement aléatoire dans la map"""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        
        # Directions possibles
        directions = ["N", "E", "S", "O"]
        import random
        direction = random.choice(directions)
        
        # Vérifier si la direction est valide
        if self.position and hasattr(self.position, 'exits'):
            if self.position.exits.get(direction):
                self.position = self.position.exits[direction]
                self.move_cooldown = 2  # Cooldown de 2 tours
        
        print(f"\n{self.name} se déplace vers {direction}...")
    
    def _move_to_target(self, game_map, target_position):
        """Déplacement vers une cible spécifique"""
        if self.position == target_position:
            return
        
        # Logique de pathfinding simple
        # Dans une implémentation réelle, on utiliserait un algorithme comme A*
        print(f"\n{self.name} se dirige vers sa destination...")
    
    def _follow_player(self, game_map, player_position):
        """Suivre le joueur"""
        if self.position == player_position:
            return
        
        # Logique de poursuite simple
        print(f"\n{self.name} vous suit...")
    
    def set_dialogue_option(self, key, dialogue_text, callback_function=None):
        """Ajouter une option de dialogue supplémentaire"""
        self.dialogue_options[key] = {
            "text": dialogue_text,
            "callback": callback_function
        }
    
    def start_conversation(self, player):
        """Démarrer une conversation avec le joueur"""
        print(f"\n=== Conversation avec {self.name} ===")
        print(self.description)
        
        if self.dialogue_options:
            print("\nQue voulez-vous dire ?")
            for key, option in self.dialogue_options.items():
                print(f"  {key}. {option['text']}")
            
            choice = input("\nVotre choix: ")
            if choice in self.dialogue_options:
                if self.dialogue_options[choice]["callback"]:
                    self.dialogue_options[choice]["callback"](player)
                return True
        
        return self.interact(player)
    
    def trade(self, player):
        """Échanger des objets avec le joueur"""
        if not hasattr(self, 'inventory'):
            self.inventory = []
        
        print(f"\n=== Échange avec {self.name} ===")
        print(f"Inventaire de {self.name}:")
        if not self.inventory:
            print("  (vide)")
        else:
            for i, item in enumerate(self.inventory, 1):
                print(f"  {i}. {item}")
        
        print("\nVotre inventaire:")
        print(player.get_inventory_string())
        
        choice = input("\nÉchanger un objet ? (o/n): ").lower()
        if choice == 'o':
            item_name = input("Nom de l'objet à échanger: ")
            # Logique d'échange à implémenter
            print("Échange non implémenté dans cette version.")
        
        return False
    
    def assign_quest(self, player, quest):
        """Assigner une quête au joueur"""
        if not hasattr(self, 'assigned_quests'):
            self.assigned_quests = []
        
        self.assigned_quests.append(quest)
        print(f"\n{self.name} vous assigne une quête: {quest['name']}")
        print(f"Objectif: {quest['objective']}")
        if 'reward' in quest:
            print(f"Récompense: {quest['reward']}")
        
        return True
    
    def check_quest_completion(self, player):
        """Vérifier la complétion des quêtes assignées"""
        if not hasattr(self, 'assigned_quests') or not self.assigned_quests:
            return
        
        for quest in self.assigned_quests[:]:  # Copie de la liste pour modification
            if quest.get('check_completion', lambda p: False)(player):
                print(f"\nFélicitations ! Vous avez complété la quête: {quest['name']}")
                if 'completion_callback' in quest:
                    quest['completion_callback'](player)
                self.assigned_quests.remove(quest)
