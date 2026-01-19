import random

class Character:
    def __init__(self, name, description, initial_room, quests=None):
        self.name = name
        self.description = description
        self.current_room = initial_room
        self.initial_room = initial_room # Point de spawn mémorisé
        self.quests = quests if quests else []
        self.dialogue_options = []
        self.movement_enabled = True
        self.interacted = False
        
        # Comportement spécial (Events)
        self.interaction_behavior = None
        
        # Ajouter le personnage à la salle initiale
        if initial_room:
            initial_room.add_character(self)
    
    def interact(self, player, game):
        """Interagir avec le personnage"""
        print(f"\n=== {self.name} ===")
        print(self.description)
        
        # 1. Interaction Spéciale (Mini-jeu)
        if self.interaction_behavior:
            success = self.interaction_behavior(player, game)
            if success and not self.interacted:
                self.interacted = True
                player.add_reward(f"Succès avec {self.name}")
            return success

        # 2. Interaction Standard
        if not self.interacted:
            self.interacted = True
            print(f"\n« Bonjour {player.name}. »")
            available_quests = [q for q in self.quests if not q.get('completed', False)]
            if available_quests:
                print("\nJ'ai des missions pour toi:")
                for i, quest in enumerate(available_quests, 1):
                    print(f"  {i}. {quest['description']}")
                player.add_reward(f"Rencontre avec {self.name}")
            return True
        else:
            print("\n« Nous avons déjà discuté. »")
            return True

    def move(self):
        """Déplacer le personnage vers une salle adjacente"""
        # Si le mouvement est désactivé (ex: Le Vieux)
        if not self.movement_enabled:
            return False
            
        # Sécurité
        if self.current_room is None:
            return False

        # Trouver les sorties valides (pas les murs/None)
        available_exits = [direction for direction, room in self.current_room.exits.items() 
                          if room is not None]
        
        # S'il n'y a nulle part où aller
        if not available_exits:
            return False
        
        # Choisir une direction au hasard
        direction = random.choice(available_exits)
        next_room = self.current_room.exits[direction]
        
        if next_room:
            # 1. Retirer de la salle actuelle
            if self in self.current_room.characters:
                self.current_room.characters.remove(self)
            
            # 2. Ajouter à la nouvelle salle
            next_room.add_character(self)
            self.current_room = next_room
            
            # Debug optionnel pour voir les mouvements dans la console
            # print(f"[DEBUG] {self.name} va vers {direction} ({next_room.name})")
            
            return True
        
        return False
    
    def reset_position(self):
        """Ramène le personnage à son point de spawn (si besoin)"""
        if self.current_room != self.initial_room and self.initial_room:
            if self.current_room and self in self.current_room.characters:
                self.current_room.characters.remove(self)
            self.initial_room.add_character(self)
            self.current_room = self.initial_room