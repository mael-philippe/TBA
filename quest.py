class Quest:
    """
    Represents a quest in the game.
    
    Attributes:
        name (str): The name of the quest
        description (str): The description of the quest
        objectives (list): List of objectives to complete
        rewards (list): List of rewards for completing the quest
        is_active (bool): Whether the quest is currently active
        is_completed (bool): Whether the quest has been completed
    """
    
    def __init__(self, name, description, objectives=None, rewards=None):
        self.name = name
        self.description = description
        self.objectives = objectives if objectives else []
        self.rewards = rewards if rewards else []
        self.is_active = False
        self.is_completed = False
        self.completed_objectives = []
    
    def activate(self):
        """Activate the quest."""
        self.is_active = True
    
    def add_objective(self, objective_type, target, description):
        """Add an objective to the quest."""
        self.objectives.append({
            'type': objective_type,
            'target': target,
            'description': description,
            'completed': False
        })
    
    def add_reward(self, reward_type, value, description):
        """Add a reward for completing the quest."""
        self.rewards.append({
            'type': reward_type,
            'value': value,
            'description': description
        })
    
    def complete_objective(self, objective_type, target):
        """Mark an objective as completed."""
        for objective in self.objectives:
            if (objective['type'] == objective_type and 
                objective['target'].lower() == target.lower() and 
                not objective['completed']):
                objective['completed'] = True
                self.completed_objectives.append(objective)
                return True
        return False
    
    def check_completion(self):
        """Check if all objectives are completed."""
        if not self.objectives:
            return False
        
        self.is_completed = all(obj['completed'] for obj in self.objectives)
        return self.is_completed
    
    def get_progress(self):
        """Get quest progress as a string."""
        if not self.objectives:
            return "Aucun objectif défini"
        
        completed = sum(1 for obj in self.objectives if obj['completed'])
        return f"{completed}/{len(self.objectives)} objectifs complétés"
    
    def __str__(self):
        status = "✓" if self.is_completed else "→" if self.is_active else "○"
        result = f"{status} {self.name}: {self.description}\n"
        
        if self.is_active and self.objectives:
            result += "  Objectifs:\n"
            for i, obj in enumerate(self.objectives, 1):
                status = "✓" if obj['completed'] else "○"
                result += f"    {status} {obj['description']}\n"
        
        return result


class QuestManager:
    """
    Manages all quests in the game.
    
    Attributes:
        quests (list): List of all quests
        active_quests (list): List of currently active quests
        completed_quests (list): List of completed quests
    """
    
    def __init__(self):
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
    
    def add_quest(self, quest):
        """Add a quest to the manager."""
        self.quests.append(quest)
    
    def activate_quest(self, quest_name):
        """Activate a quest by name."""
        for quest in self.quests:
            if quest.name.lower() == quest_name.lower() and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False
    
    def complete_quest(self, quest):
        """Mark a quest as completed and move it to completed quests."""
        if quest in self.active_quests:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            quest.is_completed = True
            return True
        return False
    
    def check_quest_triggers(self, player, action_type, target=None):
        """Check if any quest objectives are triggered by player actions."""
        for quest in self.active_quests:
            for objective in quest.objectives:
                if not objective['completed']:
                    if (objective['type'] == 'item' and action_type == 'take' and 
                        target and objective['target'].lower() == target.lower()):
                        if quest.complete_objective('item', target):
                            print(f"\n✓ Objectif de quête atteint: {objective['description']}")
                    
                    elif (objective['type'] == 'room' and action_type == 'enter' and 
                          target and objective['target'].lower() == target.lower()):
                        if quest.complete_objective('room', target):
                            print(f"\n✓ Objectif de quête atteint: {objective['description']}")
                    
                    elif (objective['type'] == 'talk' and action_type == 'talk' and 
                          target and objective['target'].lower() == target.lower()):
                        if quest.complete_objective('talk', target):
                            print(f"\n✓ Objectif de quête atteint: {objective['description']}")
            
            if quest.check_completion():
                self.complete_quest(quest)
                print(f"\n🎉 QUÊTE COMPLÉTÉE: {quest.name}!")
                print(f"   {quest.description}")
                self.give_rewards(quest, player)
    
    def give_rewards(self, quest, player):
        """Give rewards to player for completing a quest."""
        if quest.rewards:
            print("\n🎁 RÉCOMPENSES:")
            for reward in quest.rewards:
                if reward['type'] == 'health':
                    player.heal(reward['value'])
                    print(f"   +{reward['value']} points de santé")
                elif reward['type'] == 'item':
                    print(f"   {reward['description']}")
                else:
                    print(f"   {reward['description']}")
    
    def get_active_quests_string(self):
        """Get string representation of active quests."""
        if not self.active_quests:
            return "\nAucune quête active.\n"
        
        result = "\n=== QUÊTES ACTIVES ===\n"
        for quest in self.active_quests:
            result += str(quest)
            result += f"   Progression: {quest.get_progress()}\n"
        return result
    
    def get_completed_quests_string(self):
        """Get string representation of completed quests."""
        if not self.completed_quests:
            return "\nAucune quête complétée.\n"
        
        result = "\n=== QUÊTES COMPLÉTÉES ===\n"
        for quest in self.completed_quests:
            result += f"✓ {quest.name}: {quest.description}\n"
        return result