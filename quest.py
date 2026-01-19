class Quest:
    """
    Represents a quest in the game.
    
    Attributes:
        name (str): The name of the quest
        description (str): The description of the quest
        character (str): The character to interact with
        challenge_type (str): Type of challenge ('combat', 'game', 'drink', 'talk', 'steal')
        objective (str): What needs to be done
        reward (dict): Reward for completing
        is_active (bool): Whether the quest is currently active
        is_completed (bool): Whether the quest has been completed
    """
    
    def __init__(self, name, description, character, challenge_type, objective, reward=None):
        self.name = name
        self.description = description
        self.character = character
        self.challenge_type = challenge_type
        self.objective = objective
        self.reward = reward if reward else {}
        self.is_active = False
        self.is_completed = False
        self.failed = False
    
    def activate(self):
        """Activate the quest."""
        self.is_active = True
    
    def complete(self, success=True):
        """Mark the quest as completed or failed."""
        if success:
            self.is_completed = True
        else:
            self.failed = True
    
    def get_progress(self):
        """Get quest progress status."""
        if self.is_completed:
            return "✓ Complétée"
        elif self.failed:
            return "✗ Échouée"
        elif self.is_active:
            return "→ En cours"
        else:
            return "○ Inactive"
    
    def __str__(self):
        status = "✓" if self.is_completed else "✗" if self.failed else "→" if self.is_active else "○"
        result = f"{status} {self.name}\n"
        result += f"   Personnage: {self.character}\n"
        result += f"   Objectif: {self.objective}\n"
        return result


class QuestManager:
    """
    Manages all quests in the game.
    """
    
    def __init__(self):
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
    
    def add_quest(self, quest):
        """Add a quest to the manager."""
        self.quests.append(quest)
    
    def activate_quest_by_character(self, character_name):
        """Activate a quest when talking to a character."""
        for quest in self.quests:
            if quest.character.lower() == character_name.lower() and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return quest
        return None
    
    def get_quest_by_character(self, character_name):
        """Get quest associated with a character."""
        for quest in self.quests:
            if quest.character.lower() == character_name.lower():
                return quest
        return None
    
    def complete_quest(self, character_name, success=True):
        """Complete a quest associated with a character."""
        quest = self.get_quest_by_character(character_name)
        if quest and quest.is_active:
            quest.complete(success)
            if success:
                self.active_quests.remove(quest)
                self.completed_quests.append(quest)
            else:
                self.active_quests.remove(quest)
                self.failed_quests.append(quest)
            return True
        return False
    
    def give_rewards(self, quest, player):
        """Give rewards to player for completing a quest."""
        if quest.reward:
            print(f"\n🎁 RÉCOMPENSE: {quest.reward.get('description', '')}")
            if quest.reward.get('type') == 'health':
                player.heal(quest.reward['value'])
    
    def check_victory_condition(self):
        """Check if player has won (completed enough quests)."""
        return len(self.completed_quests) >= 3
    
    def get_active_quests_string(self):
        """Get string representation of active quests."""
        if not self.active_quests:
            return "\nAucune quête active. Parlez à des personnages pour en obtenir.\n"
        
        result = "\n=== QUÊTES ACTIVES ===\n"
        for quest in self.active_quests:
            result += str(quest)
        return result
    
    def get_all_quests_string(self):
        """Get string representation of all quests."""
        result = "\n=== TOUTES LES QUÊTES ===\n"
        for quest in self.quests:
            result += f"{quest.get_progress()} - {quest.name} (avec {quest.character})\n"
        return result
    
    def get_completed_quests_string(self):
        """Get string representation of completed quests."""
        if not self.completed_quests:
            return "\nAucune quête complétée.\n"
        
        result = "\n=== QUÊTES COMPLÉTÉES ===\n"
        for quest in self.completed_quests:
            result += f"✓ {quest.name} - {quest.objective}\n"
        return result