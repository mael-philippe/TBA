from room import Room
from player import Player
from command import Command
from actions import Actions
from events import *
from character import Character
from item import Item
from quest import Quest, QuestManager  # Import ajouté

class Game:
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.quest_manager = QuestManager()  # Ajout du gestionnaire de quêtes
    
    def setup(self):
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        status = Command("status", " : afficher votre état", Actions.status, 0)
        self.commands["status"] = status
        check = Command("check", " : vérifier votre inventaire", Actions.check, 0)
        self.commands["check"] = check
        history = Command("history", " : afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir à la salle précédente", Actions.back, 0)
        self.commands["back"] = back
        talk = Command("talk", " <nom_personnage> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        look = Command("look", " : regarder autour de vous", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <nom_objet> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <nom_objet> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        
        # Commandes pour les quêtes (ajoutées)
        quests = Command("quests", " : lister toutes les quêtes", Actions.quests, 0)
        self.commands["quests"] = quests
        quest = Command("quest", " <nom_quête> : afficher les détails d'une quête", Actions.quest, 1)
        self.commands["quest"] = quest
        activate = Command("activate", " <nom_quête> : activer une quête", Actions.activate, 1)
        self.commands["activate"] = activate
        rewards = Command("rewards", " : afficher les récompenses gagnées", Actions.rewards, 0)
        self.commands["rewards"] = rewards

        # Création des objets
        documents = Item("Documents", "documents compromettants sur les Mystik", 0.5)
        photo = Item("Photo", "photo compromettante du président", 0.2)
        livre_secrets = Item("Livre", "livre des secrets des Mystik", 1.0)
        cle_usb = Item("Clé USB", "clé USB avec des données sensibles", 0.1)
        redbull = Item("RedBull", "boisson énergisante", 0.3)
        trousse_secours = Item("Trousse", "trousse de premiers secours", 0.8)
        bouteille_vin = Item("Bouteille", "bouteille de vin rare", 1.5)
        pizza = Item("Pizza", "pizza à moitié mangée", 0.7)
        beamer = Item("Beamer", "appareil de téléportation magique", 2.0)

        # 9 salles
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
        cave.add_item(beamer)
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

        # Ajout des personnages
        garde = Character("Garde", "un membre de Mystik qui surveille l'entrée", porte_entree_event)
        porte_entree.add_character(garde)
        membre_ivre = Character("Ivre", "un membre de Mystik visiblement éméché", bar_event)
        bar.add_character(membre_ivre)
        champion = Character("Champion", "le champion de jeux vidéo de Mystik", salle_jeux_event)
        salle_jeux.add_character(champion)
        capitaine = Character("Capitaine", "le capitaine de l'équipe de boxe", salle_sport_event)
        salle_sport.add_character(capitaine)
        vieux_membre = Character("Vieux", "un ancien membre qui raconte des histoires", cave_event)
        cave.add_character(vieux_membre)

        # Configuration du joueur
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = porte_entree
        self.player.history.append(porte_entree)

        # Configuration des quêtes
        self.setup_quests()
    
    def setup_quests(self):
        """Configure les quêtes du jeu."""
        
        # Quête 1: Récupérer un objet spécifique
        quest1 = Quest(
            "Infiltration initiatique",
            "Récupérez la clé USB dans la salle de jeux"
        )
        quest1.add_objective('item', 'Clé USB', 'Trouver la clé USB dans la salle de jeux')
        quest1.add_reward('health', 30, "Confiance accrue: +30 santé")
        self.quest_manager.add_quest(quest1)
        
        # Quête 2: Atteindre une pièce spécifique
        quest2 = Quest(
            "Exploration secrète",
            "Atteignez le toit de la fraternité"
        )
        quest2.add_objective('room', 'Toit', 'Accéder au toit de la fraternité')
        quest2.add_reward('health', 20, "Vue imprenable: +20 santé")
        self.quest_manager.add_quest(quest2)
        
        # Quête 3: Interagir avec un PNJ spécifique
        quest3 = Quest(
            "Négociation dangereuse",
            "Parlez au vieux membre dans la cave"
        )
        quest3.add_objective('talk', 'Vieux', 'Discuter avec le vieux membre dans la cave')
        quest3.add_reward('health', 25, "Sagesse acquise: +25 santé")
        self.quest_manager.add_quest(quest3)
        
        # Activer la première quête au début du jeu
        self.quest_manager.activate_quest("Infiltration initiatique")
    
    def win(self):
        """Vérifie si le joueur a gagné (toutes les quêtes complétées)."""
        return len(self.quest_manager.completed_quests) >= 3
    
    def loose(self):
        """Vérifie si le joueur a perdu."""
        if (self.player.current_room.name == "Bureau du président" and 
            not any(item.name == "Clé USB" for item in self.player.inventory)):
            print("\n🚨 ALERTE! Vous avez été découvert!")
            print("Le président vous a surpris sans autorisation!")
            return True
        
        if self.player.health <= 0:
            return True
            
        return False
    
    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            if self.player.health <= 0:
                print("💀 GAME OVER - Mission échouée!")
                self.finished = True
                break
            
            if self.win():
                print("\n🎉 FÉLICITATIONS! Mission accomplie!")
                print("Vous avez infiltré la fraternité Mystik avec succès!")
                print("Toutes les quêtes sont complétées!")
                self.finished = True
                break
            
            if self.loose():
                self.finished = True
                break
            
            self.process_command(input("> "))
        return None

    def process_command(self, command_string) -> None:
        if not command_string.strip():
            return
        
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        else:
            command = self.commands[command_word]
            if command_word == "go" and len(list_of_words) > 1:
                direction = list_of_words[1].upper()
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
        print(self.quest_manager.get_active_quests_string())


def main():
    try:
        Game().play()
    except Exception as e:
        pass
    

if __name__ == "__main__":
    main()