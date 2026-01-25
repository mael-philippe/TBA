"""
Module des objets du jeu.
"""


class Item:
    """
    Représente un objet que le joueur peut ramasser et utiliser.
    
    Attributes:
        name (str): Nom de l'objet
        description (str): Description de l'objet
        weight (float): Poids de l'objet en kilogrammes
    """
    
    def __init__(self, name, description, weight):
        """
        Initialise un nouvel objet.
        
        Args:
            name (str): Nom de l'objet
            description (str): Description de l'objet
            weight (float): Poids de l'objet
        """
        self.name = name
        self.description = description
        self.weight = weight
    
    def __str__(self):
        """
        Représentation textuelle de l'objet.
        
        Returns:
            str: Format "nom : description (poids kg)"
        """
        return f"{self.name} : {self.description} ({self.weight:.1f} kg)"