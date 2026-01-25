"""
Module de gestion des quêtes.
"""


class Quest:
    """
    Représente une quête dans le jeu.
    
    Attributes:
        name (str): Nom de la quête
        description (str): Description de la quête
        character (str): Personnage associé
        challenge_type (str): Type de défi ('combat', 'game', 'drink', 'talk', 'steal')
        objective (str): Objectif à accomplir
        reward_item (Item): Récompense pour la quête
        is_active (bool): Si la quête est active
        is_completed (bool): Si la quête est complétée
        failed (bool): Si la quête a échoué
    """
    
    def __init__(self, name, description, character, challenge_type, objective, reward_item=None):
        """
        Initialise une nouvelle quête.
        
        Args:
            name (str): Nom de la quête
            description (str): Description de la quête
            character (str): Personnage associé
            challenge_type (str): Type de défi
            objective (str): Objectif à accomplir
            reward_item (Item, optional): Récompense. Defaults to None.
        """
        self.name = name
        self.description = description
        self.character = character
        self.challenge_type = challenge_type
        self.objective = objective
        self.reward_item = reward_item
        self.is_active = False
        self.is_completed = False
        self.failed = False
    
    def activate(self):
        """Active la quête."""
        self.is_active = True
    
    def complete(self, success=True):
        """
        Marque la quête comme complétée ou échouée.
        
        Args:
            success (bool, optional): True si réussite. Defaults to True.
        """
        if success:
            self.is_completed = True
        else:
            self.failed = True
    
    def get_progress(self):
        """
        Retourne le statut de progression de la quête.
        
        Returns:
            str: Statut formaté
        """
        if self.is_completed:
            return "✓ Complétée"
        elif self.failed:
            return "✗ Échouée"
        elif self.is_active:
            return "→ En cours"
        else:
            return "○ Inactive"
    
    def __str__(self):
        """
        Représentation textuelle de la quête.
        
        Returns:
            str: Quête formatée
        """
        status = "✓" if self.is_completed else "✗" if self.failed else "→" if self.is_active else "○"
        result = f"{status} {self.name}\n"
        result += f"   Personnage: {self.character}\n"
        result += f"   Défi: {self.challenge_type}\n"
        result += f"   Objectif: {self.objective}\n"
        return result


class QuestManager:
    """
    Gère toutes les quêtes du jeu.
    
    Attributes:
        quests (list): Liste de toutes les quêtes
        active_quests (list): Quêtes actives
        completed_quests (list): Quêtes complétées
        failed_quests (list): Quêtes échouées
    """
    
    def __init__(self):
        """Initialise un nouveau gestionnaire de quêtes."""
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
    
    def add_quest(self, quest):
        """
        Ajoute une quête au gestionnaire.
        
        Args:
            quest (Quest): Quête à ajouter
        """
        self.quests.append(quest)
    
    def activate_quest_by_character(self, character_name):
        """
        Active une quête en parlant à un personnage.
        
        Args:
            character_name (str): Nom du personnage
            
        Returns:
            Quest or None: La quête activée, ou None
        """
        for quest in self.quests:
            if quest.character.lower() == character_name.lower() and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return quest
        return None
    
    def get_quest_by_character(self, character_name):
        """
        Récupère une quête associée à un personnage.
        
        Args:
            character_name (str): Nom du personnage
            
        Returns:
            Quest or None: La quête trouvée, ou None
        """
        for quest in self.quests:
            if quest.character.lower() == character_name.lower():
                return quest
        return None
    
    def complete_quest(self, character_name, success=True):
        """
        Complète une quête associée à un personnage.
        
        Args:
            character_name (str): Nom du personnage
            success (bool, optional): True si réussite. Defaults to True.
            
        Returns:
            bool: True si la quête a été complétée
        """
        quest = self.get_quest_by_character(character_name)
        if quest and quest.is_active:
            quest.complete(success)
            # S'assurer que la quête est dans la liste avant de la retirer
            if quest in self.active_quests:
                self.active_quests.remove(quest)
                if success:
                    self.completed_quests.append(quest)
                else:
                    self.failed_quests.append(quest)
            return True
        return False
    
    def check_victory_condition(self):
        """
        Vérifie si le joueur a gagné (complété assez de quêtes).
        
        Returns:
            bool: True si le joueur a gagné
        """
        return len(self.completed_quests) >= 4  # 4 quêtes sur 5 pour gagner
    
    def get_active_quests_string(self):
        """
        Retourne une représentation des quêtes actives.
        
        Returns:
            str: Quêtes actives formatées
        """
        if not self.active_quests:
            return "\nAucune quête active. Parlez à des personnages pour en obtenir.\n"
        
        result = "\n=== QUÊTES ACTIVES ===\n"
        for quest in self.active_quests:
            result += str(quest)
        return result
    
    def get_all_quests_string(self):
        """
        Retourne une représentation de toutes les quêtes.
        
        Returns:
            str: Toutes les quêtes formatées
        """
        result = "\n=== TOUTES LES QUÊTES ===\n"
        for quest in self.quests:
            result += f"{quest.get_progress()} - {quest.name} (avec {quest.character})\n"
        return result
    
    def get_completed_quests_string(self):
        """
        Retourne une représentation des quêtes complétées.
        
        Returns:
            str: Quêtes complétées formatées
        """
        if not self.completed_quests:
            return "\nAucune quête complétée.\n"
        
        result = "\n=== QUÊTES COMPLÉTÉES ===\n"
        for quest in self.completed_quests:
            result += f"✓ {quest.name} - {quest.objective}\n"
        return result