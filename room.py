class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.visited = False
        self.characters = []
        self.inventory = []
    
    def add_character(self, character):
        if character not in self.characters:
            self.characters.append(character)
    
    def remove_character(self, character):
        if character in self.characters:
            self.characters.remove(character)
    
    def get_character(self, character_name):
        character_name_lower = character_name.lower()
        for character in self.characters:
            if character.name.lower() == character_name_lower:
                return character
        return None
    
    def get_long_description(self):
        description = f"\n📍 {self.name}\n"
        description += f"{self.description}\n"
        description += self.get_exit_string() + "\n"
        if not self.visited:
            self.visited = True
        
        return description
    
    def get_exit_string(self):
        available_exits = [exit for exit, room in self.exits.items() 
                          if room is not None]
        
        if not available_exits:
            return "Aucune sortie visible."
        
        exit_string = "Sorties disponibles: "
        exit_string += ", ".join(available_exits)
        return exit_string
    
    def get_inventory_string(self):
        if not self.inventory:
            return "\nIl n'y a rien d'intéressant ici.\n"
        
        inventory_str = "\nObjets visibles:\n"
        for i, item in enumerate(self.inventory, 1):
            # CORRECTION : Formater avec 1 décimale
            inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        return inventory_str
    
    def add_item(self, item):
        self.inventory.append(item)
    
    def remove_item(self, item_name):
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                return self.inventory.pop(i)
        return None
    
    def get_item(self, item_name):
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None
    
    def __str__(self):
        return self.name