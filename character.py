"""
Module des personnages non-joueurs (PNJ).
"""

import random
import events


class Character:
    """
    Représente un personnage non-joueur (PNJ) dans le jeu.
    
    Attributes:
        name (str): Nom du personnage
        description (str): Description du personnage
        current_room (Room): Salle actuelle du personnage
        initial_room (Room): Salle de départ (spawn)
        quest (Quest): Quête associée au personnage
        movement_enabled (bool): Si le personnage peut se déplacer
        interacted (bool): Si le joueur a déjà parlé au personnage
        can_move_now (bool): Si le personnage peut bouger maintenant
        waiting_for_player_move (bool): Si le personnage attend le déplacement du joueur
    """
    
    def __init__(self, name, description, initial_room, quest=None):
        """
        Initialise un nouveau personnage.
        
        Args:
            name (str): Nom du personnage
            description (str): Description du personnage
            initial_room (Room): Salle de départ
            quest (Quest, optional): Quête associée. Defaults to None.
        """
        self.name = name
        self.description = description
        self.current_room = initial_room
        self.initial_room = initial_room
        self.quest = quest
        self.movement_enabled = True
        self.interacted = False
        
        # Contrôle du mouvement
        self.can_move_now = True
        self.waiting_for_player_move = False
        
        # Mapping des mini-jeux par nom de personnage
        self.minigame_mapping = {
            "Garde": events.guard_interaction,
            "Coach": events.captain_interaction,
            "Champion": events.champion_interaction,
            "Ivre": events.drunk_interaction,
            "Vieux": events.old_member_interaction
        }
        
        # Ajouter le personnage à sa salle initiale
        if initial_room:
            initial_room.add_character(self)
    
    def interact(self, player, game):
        """
        Interagir avec le personnage.
        
        Args:
            player (Player): Le joueur qui interagit
            game (Game): Instance du jeu
            
        Returns:
            bool: True si l'interaction a réussi
        """
        print(f"\n=== {self.name} ===")
        print(self.description)
        
        # Bloquer temporairement le mouvement du PNJ
        self.can_move_now = False
        self.waiting_for_player_move = True
        
        # Si le personnage a une quête
        if self.quest:
            if not self.quest.is_active:
                # Activer la quête sans lancer le mini-jeu
                self.quest.activate()
                if game and hasattr(game, 'quest_manager'):
                    game.quest_manager.active_quests.append(self.quest)
                print(f"\n📜 NOUVELLE QUÊTE: {self.quest.name}")
                print(f"   {self.quest.description}")
                print("\n« Reviens me voir quand tu seras prêt à relever le défi ! »")
                self.interacted = True
                return True
            
            elif self.quest.is_active and not self.quest.is_completed:
                # Lancer le mini-jeu
                print(f"\n📜 QUÊTE EN COURS: {self.quest.name}")
                
                # Quête simple de dialogue
                if self.quest.challenge_type == 'talk':
                    print("« Parfait, discutons ! »")
                    print(f"✅ Quête '{self.quest.name}' complétée par la discussion !")
                    
                    self.quest.complete(success=True)
                    if game and hasattr(game, 'quest_manager'):
                        game.quest_manager.complete_quest(self.name, success=True)
                    return True
                
                # Mini-jeu spécifique au personnage
                if self.name in self.minigame_mapping:
                    print(f"« Tu es prêt pour le défi ? »")
                    minigame_func = self.minigame_mapping[self.name]
                    success = minigame_func(player, game)
                    
                    if success:
                        self.quest.complete(success=True)
                        if game and hasattr(game, 'quest_manager'):
                            game.quest_manager.complete_quest(self.name, success=True)
                        print(f"\n✅ Quête '{self.quest.name}' complétée !")
                        return True
                    else:
                        print(f"\n❌ Échec. Vous pouvez réessayer plus tard !")
                        return False
                else:
                    print(f"\n❌ Ce personnage n'a pas de mini-jeu défini.")
                    return False
            
            elif self.quest.is_completed:
                print(f"\n« Merci pour ton aide ! La quête '{self.quest.name}' est terminée. »")
                return True
        
        # Interaction standard (sans quête principale)
        if not self.interacted:
            self.interacted = True
            print(f"\n« Bonjour {player.name}. »")
            
            # Le Garde propose la quête d'exploration
            if self.name == "Garde" and not hasattr(player, 'explorer_quest_given'):
                print("« Tu as l'air d'un explorateur. »")
                print("« Si tu veux prouver ta valeur, visite les 4 coins extrêmes du campus. »")
                print("« La Cave (sous la cuisine), l'Observatoire (au-dessus du bureau), »")
                print("« le Sauna (sous la salle de sport) et la Terrasse (au-dessus du bar). »")
                print("« Reviens me voir quand tu auras tout visité ! »")
                player.explorer_quest_given = True
                return True
            
            # L'Ivre propose la quête de collection
            elif self.name == "Ivre" and not hasattr(player, 'collector_quest_given'):
                print("« Hips... Tu cherches des trucs à boire et manger ? »")
                print("« Rassemble un RedBull, une part de pizza et une bonne bouteille de vin. »")
                print("« Ça fait un bon festin ! Les trouve où tu peux... hips ! »")
                player.collector_quest_given = True
                return True
            else:
                print("« Je n'ai pas de mission pour toi pour le moment. »")
                return True
        else:
            print("\n« Nous avons déjà discuté. »")
            return True

    def move(self):
        """
        Déplacer le personnage vers une salle adjacente aléatoire.
        
        Returns:
            bool: True si le déplacement a réussi
        """
        # Vérifications
        if not self.movement_enabled:
            return False
        if not self.can_move_now:
            return False
        if self.current_room is None:
            return False

        # Choisir une direction aléatoire
        all_directions = ["N", "E", "S", "O", "U", "D"]
        direction = random.choice(all_directions)
        
        # Vérifier si la direction existe
        if direction not in self.current_room.exits:
            return False
        
        next_room = self.current_room.exits[direction]
        if next_room is None:
            return False
        
        # Les PNJ ne peuvent pas entrer dans le bureau du président
        if next_room.name == "Bureau du Président":
            return False
        
        # Effectuer le déplacement
        if self in self.current_room.characters:
            self.current_room.characters.remove(self)
        
        next_room.add_character(self)
        self.current_room = next_room
        
        return True
    
    def reset_movement_flags(self):
        """
        Réactiver le mouvement après un déplacement du joueur.
        """
        self.can_move_now = True
        self.waiting_for_player_move = False
    
    def reset_position(self):
        """
        Ramener le personnage à son point de spawn initial.
        """
        if self.current_room != self.initial_room and self.initial_room:
            if self.current_room and self in self.current_room.characters:
                self.current_room.characters.remove(self)
            self.initial_room.add_character(self)
            self.current_room = self.initial_room