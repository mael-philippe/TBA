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
        
        # AJOUT : Contrôle du mouvement
        self.can_move_now = True
        self.waiting_for_player_move = False
        
        # Comportement spécial (Events)
        self.interaction_behavior = None
        
        # Ajouter le personnage à la salle initiale
        if initial_room:
            initial_room.add_character(self)
    
    def interact(self, player, game):
        """Interagir avec le personnage"""
        print(f"\n=== {self.name} ===")
        print(self.description)
        
        # AJOUT : Bloquer ce PNJ jusqu'au prochain déplacement du joueur
        self.can_move_now = False
        self.waiting_for_player_move = True
        
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
        # 1. Vérification si le mouvement est autorisé
        if not self.movement_enabled:  # ← Le Vieux est bloqué ici
            return False
                
        # 2. Vérification des flags (si bloqué après interaction)
        if not self.can_move_now:  # ← Bloqué après un talk
            return False
                
        # 3. Vérification si la salle existe
        if self.current_room is None:
            return False

        # 4. Liste des 6 directions possibles (même si certaines n'existent pas)
        all_directions = ["N", "E", "S", "O", "U", "D"]
        
        # 5. Choisir une direction au hasard parmi les 6
        direction = random.choice(all_directions)
        
        # 6. Vérifier si cette direction existe dans les sorties
        if direction not in self.current_room.exits:
            return False  # ← Direction n'existe pas, pas de déplacement
        
        # 7. Vérifier si la sortie n'est pas un mur (None)
        next_room = self.current_room.exits[direction]
        if next_room is None:
            return False  # ← C'est un mur, pas de déplacement
        
        # 8. AJOUT IMPORTANT : Vérifier si la prochaine salle est le Bureau du Président
        if next_room.name == "Bureau du Président":
            return False  # ← Les PNJ ne peuvent pas entrer dans le bureau
        
        # 9. Effectuer le déplacement
        # Retirer de la salle actuelle
        if self in self.current_room.characters:
            self.current_room.characters.remove(self)
        
        # Ajouter à la nouvelle salle
        next_room.add_character(self)
        self.current_room = next_room
        
        # Debug optionnel pour voir les mouvements
        # print(f"[DEBUG] {self.name} va vers {direction} ({next_room.name})")
        
        return True  # ← Déplacement réussi
    
    def reset_movement_flags(self):
        """Réactiver le mouvement après un déplacement du joueur"""
        self.can_move_now = True
        self.waiting_for_player_move = False
    
    def reset_position(self):
        """Ramène le personnage à son point de spawn (si besoin)"""
        if self.current_room != self.initial_room and self.initial_room:
            if self.current_room and self in self.current_room.characters:
                self.current_room.characters.remove(self)
            self.initial_room.add_character(self)
            self.current_room = self.initial_room