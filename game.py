from room import Room
from player import Player
from command import Command
from actions import Actions
from events import *
from character import Character
from item import Item

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
        # Commande check (remplace inventory)
        check = Command("check", " : vérifier votre inventaire", Actions.check, 0)
        self.commands["check"] = check
        # Ajout de la commande history
        history = Command("history", " : afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["history"] = history
        # Ajout de la commande back
        back = Command("back", " : revenir à la salle précédente", Actions.back, 0)
        self.commands["back"] = back
        # Ajout de la commande talk
        talk = Command("talk", " <nom_personnage> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        # Ajout de la commande look
        look = Command("look", " : regarder autour de vous", Actions.look, 0)
        self.commands["look"] = look
        # NOUVELLES COMMANDES
        take = Command("take", " <nom_objet> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <nom_objet> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        # Ajout de la commande map
        map_cmd = Command("map", " : afficher la carte de la fraternité", Actions.map, 0)
        self.commands["map"] = map_cmd

        # Création des objets
        # Objets de preuve
        documents = Item("Documents", "documents compromettants sur les Mystik", 0.5)
        photo = Item("Photo", "photo compromettante du président", 0.2)
        livre_secrets = Item("Livre", "livre des secrets des Mystik", 1.0)
        cle_usb = Item("Clé USB", "clé USB avec des données sensibles", 0.1)
        
        # Objets utiles
        redbull = Item("RedBull", "boisson énergisante", 0.3)
        trousse_secours = Item("Trousse", "trousse de premiers secours", 0.8)
        bouteille_vin = Item("Bouteille", "bouteille de vin rare", 1.5)
        pizza = Item("Pizza", "pizza à moitié mangée", 0.7)
        
        # Objet spécial : Beamer
        beamer = Item("Beamer", "appareil de téléportation magique", 2.0)

        # 9 salles sans événements d'entrée
        porte_entree = Room("Porte d'entrée", "devant l'entrée principale de la fraternité Mystik. La musique tonne de l'intérieur.")
        self.rooms.append(porte_entree)
        
        bar = Room("Bar", "dans le bar principal. Des bouteilles vides traînent partout.")
        self.rooms.append(bar)
        
        cuisine = Room("Cuisine", "dans la cuisine dégoûtante. De la nourriture pourrie traîne partout.")
        self.rooms.append(cuisine)
        
        salle_jeux = Room("Salle de jeux", "dans la salle de jeux. Des consoles et écrans géants remplissent la pièce.")
        self.rooms.append(salle_jeux)
        
        bureau_president = Room("Bureau du président", "dans le bureau luxueux du président. Des trophées et diplômes ornent les murs.")
        self.rooms.append(bureau_president)
        
        dortoir = Room("Dortoir", "dans le dortoir commun. Des vêtements sales traînent sur le sol.")
        self.rooms.append(dortoir)
        
        salle_sport = Room("Salle de sport", "dans la salle de sport privée. Des équipements dernier cri sont alignés.")
        self.rooms.append(salle_sport)
        
        cave = Room("Cave", "dans la cave sombre et humide. Des rangées de bouteilles de vin s'alignent.")
        self.rooms.append(cave)
        
        toit = Room("Toit", "sur le toit de la fraternité. La vue sur le campus est magnifique.")
        self.rooms.append(toit)

        # Ajouter des objets aux salles
        porte_entree.add_item(redbull)
        bar.add_item(bouteille_vin)
        cuisine.add_item(pizza)
        salle_jeux.add_item(cle_usb)
        bureau_president.add_item(documents)
        bureau_president.add_item(photo)
        dortoir.add_item(trousse_secours)
        cave.add_item(beamer)  # Beamer dans la cave
        toit.add_item(livre_secrets)

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

        # Ajout des personnages avec leurs événements
        # Porte d'entrée
        garde = Character("Garde", "un membre de Mystik qui surveille l'entrée", porte_entree_event)
        porte_entree.add_character(garde)
        
        # Bar
        membre_ivre = Character("Ivre", "un membre de Mystik visiblement éméché", bar_event)
        bar.add_character(membre_ivre)
        
        # Cuisine (pas de personnage, mais événement spécial sur "look")
        # Salle de jeux
        champion = Character("Champion", "le champion de jeux vidéo de Mystik", salle_jeux_event)
        salle_jeux.add_character(champion)
        
        # Bureau du président (pas de personnage visible immédiatement)
        # Dortoir (pas de personnage, événement spécial)
        # Salle de sport
        capitaine = Character("Capitaine", "le capitaine de l'équipe de boxe", salle_sport_event)
        salle_sport.add_character(capitaine)
        
        # Cave
        vieux_membre = Character("Vieux", "un ancien membre qui raconte des histoires", cave_event)
        cave.add_character(vieux_membre)
        
        # Toit (pas de personnage, événement spécial)

        # Configuration du joueur
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = porte_entree
        self.player.history.append(porte_entree)

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
        print("Capacité d'inventaire: 20 kg")
        print(self.player.current_room.get_long_description())
    
    def show_map(self):
        """Affiche la carte ASCII de la fraternité"""
        print("\n" + "="*60)
        print("CARTE DE LA FRATERNITÉ MYSTIK")
        print("="*60)
        
        # Déterminer où se trouve le joueur
        player_room = self.player.current_room.name if self.player.current_room else "Inconnu"
        
        # Carte ASCII de la fraternité
        map_ascii = """
                               [TOIT]                                              
                                 |                                                 
                                 |                                              
                [DORTOIR]--[SALLE DE JEUX]--[BUREAU DU PRÉSIDENT]                   
                    |            |                     |                           
                    |            |                     | 
            [SALLE DE SPORT]---[BAR]---------------[CUISINE]
                    |            |
                    |            | 
                [CAVE]     [PORTE D'ENTRÉE]
        """
        
        # Remplacer la salle actuelle par [X]
        room_replacements = {
            "Toit": "[TOIT]",
            "Dortoir": "[DORTOIR]",
            "Salle de jeux": "[SALLE DE JEUX]",
            "Bureau du président": "[BUREAU DU PRÉSIDENT]",
            "Salle de sport": "[SALLE DE SPORT]",
            "Bar": "[BAR]",
            "Cuisine": "[CUISINE]",
            "Cave": "[CAVE]",
            "Porte d'entrée": "[PORTE D'ENTRÉE]"
        }
        
        # Trouver et marquer la position du joueur
        for room_name, ascii_name in room_replacements.items():
            if room_name == player_room:
                # Remplacer par [X] pour indiquer la position du joueur
                map_ascii = map_ascii.replace(ascii_name, f"[{room_name[0]}]")
                # Ajouter une explication
                map_ascii = map_ascii.replace("CARTE DE LA FRATERNITÉ MYSTIK", 
                                             f"CARTE DE LA FRATERNITÉ MYSTIK - Vous êtes dans: {player_room}")
        
        print(map_ascii)
        print("\nLégende:")
        print("  [X] = Vous êtes ici")
        print("  [L] = Première lettre du nom de la salle")
        print("  |    = Passage vertical")
        print("  --   = Passage horizontal")
        print()
        
        # Afficher les connexions détaillées de la salle actuelle
        if self.player.current_room:
            current = self.player.current_room
            print(f"Connexions depuis {current.name}:")
            directions = {"N": "Nord", "E": "Est", "S": "Sud", "O": "Ouest"}
            for dir_code, dir_name in directions.items():
                if current.exits.get(dir_code):
                    print(f"  {dir_name} → {current.exits[dir_code].name}")
                else:
                    print(f"  {dir_name} → Aucune sortie")
            print()


def main():
    try:
        Game().play()
    except Exception as e:
        pass
    

if __name__ == "__main__":
    main()
