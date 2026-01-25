"""
Module des salles du jeu.
"""


class Room:
    """
    Représente un lieu (salle) dans le jeu.
    
    Une salle est un emplacement dans le monde du jeu où le joueur peut se trouver.
    Elle contient une description, des sorties vers d'autres salles, des objets
    et des personnages non-joueurs.
    
    Attributes:
        name (str): Nom de la salle
        description (str): Description textuelle de la salle
        exits (dict): Sorties disponibles sous forme de dictionnaire {direction: salle}
        visited (bool): Si la salle a déjà été visitée par le joueur
        characters (list): Liste des personnages non-joueurs présents dans la salle
        inventory (list): Liste des objets présents dans la salle
    
    Methods:
        __init__(name, description): Initialise une nouvelle salle
        add_character(character): Ajoute un personnage à la salle
        remove_character(character): Retire un personnage de la salle
        get_character(character_name): Recherche un personnage par son nom
        get_long_description(): Retourne une description complète de la salle
        get_exit_string(): Retourne les sorties disponibles sous forme de chaîne
        get_inventory_string(): Retourne les objets présents sous forme de chaîne
        add_item(item): Ajoute un objet à la salle
        remove_item(item_name): Retire un objet de la salle par son nom
        get_item(item_name): Recherche un objet par son nom
    
    Examples:
        >>> from room import Room
        >>> salle = Room("Cuisine", "Une cuisine bien équipée.")
        >>> print(salle.name)
        Cuisine
        >>> print(salle.description)
        Une cuisine bien équipée.
        >>> print(salle.exits)
        {}
    """
    
    def __init__(self, name, description):
        """
        Initialise une nouvelle salle.
        
        Args:
            name (str): Nom de la salle
            description (str): Description de la salle
        """
        self.name = name
        self.description = description
        self.exits = {}
        self.visited = False
        self.characters = []
        self.inventory = []
    
    def add_character(self, character):
        """
        Ajoute un personnage à la salle.
        
        Args:
            character (Character): Personnage à ajouter
        """
        if character not in self.characters:
            self.characters.append(character)
    
    def remove_character(self, character):
        """
        Retire un personnage de la salle.
        
        Args:
            character (Character): Personnage à retirer
        """
        if character in self.characters:
            self.characters.remove(character)
    
    def get_character(self, character_name):
        """
        Recherche un personnage dans la salle.
        
        Args:
            character_name (str): Nom du personnage (insensible à la casse)
            
        Returns:
            Character or None: Le personnage trouvé, ou None s'il n'existe pas
        """
        character_name_lower = character_name.lower()
        for character in self.characters:
            if character.name.lower() == character_name_lower:
                return character
        return None
    
    def get_long_description(self):
        """
        Retourne une description complète de la salle.
        
        Inclut le nom, la description et les sorties disponibles.
        Marque également la salle comme visitée.
        
        Returns:
            str: Description formatée de la salle
        """
        description = f"\n📍 {self.name}\n"
        description += f"{self.description}\n"
        description += self.get_exit_string() + "\n"
        if not self.visited:
            self.visited = True
        
        return description
    
    def get_exit_string(self):
        """
        Retourne les sorties disponibles sous forme de chaîne lisible.
        
        Returns:
            str: Sorties disponibles formatées (ex: "Sorties disponibles: N, E, S")
        """
        available_exits = [exit for exit, room in self.exits.items() 
                          if room is not None]
        
        if not available_exits:
            return "Aucune sortie visible."
        
        exit_string = "Sorties disponibles: "
        exit_string += ", ".join(available_exits)
        return exit_string
    
    def get_inventory_string(self):
        """
        Retourne les objets présents dans la salle.
        
        Returns:
            str: Objets formatés
        """
        if not self.inventory:
            return "\nIl n'y a rien d'intéressant ici.\n"
        
        inventory_str = "\nObjets visibles:\n"
        for i, item in enumerate(self.inventory, 1):
            inventory_str += f"    {i}. {item.name} : {item.description} ({item.weight:.1f} kg)\n"
        return inventory_str
    
    def add_item(self, item):
        """
        Ajoute un objet à la salle.
        
        Args:
            item (Item): Objet à ajouter
        """
        self.inventory.append(item)
    
    def remove_item(self, item_name):
        """
        Retire un objet de la salle.
        
        Args:
            item_name (str): Nom de l'objet
            
        Returns:
            Item or None: L'objet retiré, ou None
        """
        item_name_lower = item_name.lower()
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name_lower:
                return self.inventory.pop(i)
        return None
    
    def get_item(self, item_name):
        """
        Recherche un objet dans la salle.
        
        Args:
            item_name (str): Nom de l'objet
            
        Returns:
            Item or None: L'objet trouvé, ou None
        """
        item_name_lower = item_name.lower()
        for item in self.inventory:
            if item.name.lower() == item_name_lower:
                return item
        return None
    
    def __str__(self):
        """
        Représentation textuelle de la salle.
        
        Returns:
            str: Nom de la salle
        """
        return self.name