"""
Module de définition des commandes.
"""


class Command:
    """
    Représente une commande du jeu.
    
    Une commande est composée d'un mot-clé, d'une aide, d'une action
    et d'un nombre de paramètres attendus.
    
    Attributes:
        command_word (str): Le mot-clé de la commande
        help_string (str): La description de la commande
        action (function): La fonction à exécuter
        number_of_parameters (int): Nombre de paramètres attendus
    """
    
    def __init__(self, command_word, help_string, action, number_of_parameters):
        """
        Initialise une nouvelle commande.
        
        Args:
            command_word (str): Mot-clé de la commande
            help_string (str): Description de la commande
            action (function): Fonction à exécuter
            number_of_parameters (int): Nombre de paramètres attendus
        """
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    def __str__(self):
        """
        Représentation textuelle de la commande.
        
        Returns:
            str: Format "commande : description"
        """
        return f"{self.command_word}{self.help_string}"