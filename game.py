from room import Room
from player import Player
from command import Command
from actions import Actions
from events import *

class Game:
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    def setup(self):
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        status = Command("status", " : afficher votre état", Actions.status, 0)
        self.commands["status"] = status
        inventory = Command("inventory", " : afficher votre inventaire", Actions.inventory, 0)
        self.commands["inventory"] = inventory

        # 9 salles avec leurs événements
        porte_entree = Room("Porte d'entrée", "devant l'entrée principale de la fraternité Mystik. La musique tonne de l'intérieur.", porte_entree_event)
        self.rooms.append(porte_entree)
        
        bar = Room("Bar", "dans le bar principal. Des bouteilles vides traînent partout.", bar_event)
        self.rooms.append(bar)
        
        cuisine = Room("Cuisine", "dans la cuisine dégoûtante. De la nourriture pourrie traîne partout.", cuisine_event)
        self.rooms.append(cuisine)
        
        salle_jeux = Room("Salle de jeux", "dans la salle de jeux. Des consoles et écrans géants remplissent la pièce.", salle_jeux_event)
        self.rooms.append(salle_jeux)
        
        bureau_president = Room("Bureau du président", "dans le bureau luxueux du président. Des trophées et diplômes ornent les murs.", bureau_president_event)
        self.rooms.append(bureau_president)
        
        dortoir = Room("Dortoir", "dans le dortoir commun. Des vêtements sales traînent sur le sol.", dortoir_event)
        self.rooms.append(dortoir)
        
        salle_sport = Room("Salle de sport", "dans la salle de sport privée. Des équipements dernier cri sont alignés.", salle_sport_event)
        self.rooms.append(salle_sport)
        
        cave = Room("Cave", "dans la cave sombre et humide. Des rangées de bouteilles de vin s'alignent.", cave_event)
        self.rooms.append(cave)
        
        toit = Room("Toit", "sur le toit de la fraternité. La vue sur le campus est magnifique.", toit_event)
        self.rooms.append(toit)

        # Configuration des sorties
        porte_entree.exits = {"N": bar, "E": None, "S": None, "O": None}
        bar.exits = {"N": salle_jeux, "E": cuisine, "S": porte_entree, "O": salle_sport}
        cuisine.exits = {"N": bureau_president, "E": None, "S": None, "O": bar}
        salle_jeux.exits = {"N": toit, "E": bureau_president, "S": bar, "O": dortoir}
        bureau_president.exits = {"N": None, "E": None, "S": cuisine, "O": salle_jeux}
        dortoir.exits = {"N": None, "E": salle_jeux, "S": salle_sport, "O": None}
        salle_sport.exits = {"N": dortoir, "E": bar, "S": cave, "O": None}
        cave.exits = {"N": salle_sport, "E": None, "S": None, "O": None}
        toit.exits = {"N": None, "E": None, "S": salle_jeux, "O": None}

        # Configuration du joueur
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = porte_entree

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            # Vérifier si le joueur est mort
            if self.player.health <= 0:
                print("💀 GAME OVER - Mission échouée!")
                self.finished = True
                break
            self.process_command(input("> "))
        return None

    def process_command(self, command_string) -> None:
        # Si la commande est vide, ne rien faire
        if not command_string.strip():
            return
        
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            # Ajout: Vérification spécifique pour la commande "go"
            if command_word == "go" and len(list_of_words) > 1:
                direction = list_of_words[1].upper()
                # Vérifier si la direction est valide (N, E, S, O)
                if direction not in ["N", "E", "S", "O"]:
                    print(f"\nDirection '{direction}' non valide. Les directions possibles sont: N (Nord), E (Est), S (Sud), O (Ouest).\n")
                    return
            
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans 'Infiltration Mystik'!")
        print("Votre mission: Infiltrer la fraternité Mystik et collecter des preuves compromettantes.")
        print("Utilisez 'help' pour voir les commandes disponibles.")
        print("Santé: 100/100")
        print(self.player.current_room.get_long_description())

def main():
    try:
        Game().play()
    except Exception as e:
        pass
    

if __name__ == "__main__":
    main()
