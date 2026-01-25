"""
Module principal du jeu - Contient la classe Game.
"""

import traceback
import random
from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item
import events
from quest import Quest, QuestManager


class Game:
    """
    Classe principale du jeu. Gère l'initialisation et la boucle de jeu.
    
    Attributes:
        DEBUG (bool): Mode débogage
        finished (bool): Si le jeu est terminé
        rooms (list): Liste de toutes les salles
        commands (dict): Dictionnaire des commandes disponibles
        player (Player): Le joueur
        characters (list): Liste des personnages
        quest_manager (QuestManager): Gestionnaire de quêtes
        turn_count (int): Compteur de tours
        spawn_timer (int): Timer pour l'apparition d'objets
        next_spawn_turn (int): Tour pour la prochaine apparition
        spawnable_items (dict): Configuration des objets apparaissables
    """
    
    DEBUG = True  # Mode débogage activé
    
    def __init__(self):
        """Initialise une nouvelle partie."""
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.characters = []
        self.quest_manager = QuestManager()
        
        # Gestion du temps et des apparitions
        self.turn_count = 0
        self.spawn_timer = 0
        self.next_spawn_turn = random.randint(1, 5)
        self.spawnable_items = {
            "RedBull": {"max": 3, "desc": "boisson énergisante", "weight": 0.3},
            "Part de pizza": {"max": 2, "desc": "reste de la veille", "weight": 0.2}
        }
    
    def setup(self):
        """
        Configure le jeu : commandes, salles, objets, quêtes, personnages.
        """
        # Définir les commandes disponibles
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer (N,E,S,O,U,D)", Actions.go, 1)
        self.commands["status"] = Command("status", " : afficher votre état", Actions.status, 0)
        self.commands["check"] = Command("check", " : inventaire", Actions.check, 0)
        self.commands["history"] = Command("history", " : historique", Actions.history, 0)
        self.commands["back"] = Command("back", " : retour arrière", Actions.back, 0)
        self.commands["talk"] = Command("talk", " <nom> : parler", Actions.talk, 1)
        self.commands["look"] = Command("look", " : observer", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : déposer", Actions.drop, 1)
        self.commands["use"] = Command("use", " <objet> : utiliser un objet spécial", Actions.use, 1)
        self.commands["quests"] = Command("quests", " : afficher les quêtes", Actions.quests, 0)
        self.commands["progress"] = Command("progress", " : progression des quêtes spéciales", Actions.progress, 0)
        
        # Créer les éléments du jeu
        self._create_rooms()
        self._create_items()
        self._create_quests()
        self._create_characters()

    def _create_rooms(self):
        """Crée toutes les salles du jeu et leurs connexions."""
        # Création des salles
        entree = Room("Porte d'entrée", "devant l'entrée principale de la fraternité Mystik.")
        hall = Room("Hall principal", "dans le grand hall d'entrée. Des portraits anciens décorent les murs.")
        cuisine = Room("Cuisine", "dans une cuisine équipée. Des odeurs de nourriture flottent dans l'air.")
        cave = Room("Cave", "dans une cave sombre et humide. Des bouteilles de vin alignées sur des étagères.")
        salle_sport = Room("Salle de sport", "dans une salle de sport bien équipée avec des poids et machines.")
        sauna = Room("Sauna", "dans un sauna chaud et vaporeux. La chaleur est intense et relaxante.")
        dortoir = Room("Dortoir", "dans le dortoir des membres. Des lits superposés et des affaires personnelles.")
        bar = Room("Bar", "dans un bar bien approvisionné. Le comptoir brille sous la lumière tamisée.")
        terrasse = Room("Terrasse", "sur une terrasse avec vue panoramique sur le campus. L'air est frais.")
        bureau = Room("Bureau du Président", "dans le bureau luxueux du chef. Un grand bureau en acajou trône au centre.")
        observatoire = Room("Observatoire", "dans un observatoire équipé d'un télescope professionnel.")
        salle_jeux = Room("Salle de jeux", "dans une salle de jeux moderne avec consoles et jeux de société.")
        
        # Configuration des sorties (connexions entre salles)
        entree.exits = {"N": hall}
        hall.exits = {"S": entree, "E": cuisine, "O": salle_sport, "N": dortoir}
        cuisine.exits = {"O": hall, "D": cave, "N": bar}
        cave.exits = {"U": cuisine}
        salle_sport.exits = {"E": hall, "D": sauna, "N": bureau}
        sauna.exits = {"U": salle_sport}
        dortoir.exits = {"S": hall, "E": bar, "O": bureau, "U": salle_jeux}
        bar.exits = {"O": dortoir, "U": terrasse, "S": cuisine}
        terrasse.exits = {"D": bar, "O": salle_jeux}
        bureau.exits = {"E": dortoir, "U": observatoire}
        observatoire.exits = {"D": bureau, "E": salle_jeux}
        salle_jeux.exits = {"D": dortoir, "O": observatoire, "E": terrasse}
        
        # Stocker toutes les salles
        self.rooms = [
            entree, hall, cuisine, cave, salle_sport, sauna,
            dortoir, bar, terrasse, bureau, observatoire, salle_jeux
        ]
        
        # Créer le joueur
        self.player = Player(input("\nEntrez votre nom: "), self)
        self.player.current_room = entree

    def _create_items(self):
        """Crée les objets uniques du jeu."""
        # GPS - Outil de localisation des PNJ
        gps = Item("GPS", "un traqueur de PNJ haute technologie", 1.5)
        self.rooms[3].add_item(gps)  # Dans la cave
        
        # Chien - Compagnon qui trouve des objets
        chien = Item("Chien", "un fidèle compagnon au flair infaillible", 2.7)
        self.rooms[5].add_item(chien)  # Dans le sauna

    def _create_quests(self):
        """Crée toutes les quêtes du jeu."""
        from item import Item
        
        # Quête du Garde - Juste Prix
        quest_garde = Quest(
            name="Le Juste Prix",
            description="Deviner le code de sécurité du Garde pour obtenir la Clé USB.",
            character="Garde",
            challenge_type="combat",
            objective="Gagner au jeu du Juste Prix",
            reward_item=Item("Clé USB", "les codes de sécurité", 0.1)
        )
        self.quest_manager.add_quest(quest_garde)
        
        # Quête du Coach - Boxe
        quest_coach = Quest(
            name="Le Ring",
            description="Tenir 3 rounds contre le Coach de boxe pour obtenir ses Documents.",
            character="Coach",
            challenge_type="combat",
            objective="Gagner le combat de boxe",
            reward_item=Item("Documents", "des preuves de matchs truqués", 0.5)
        )
        self.quest_manager.add_quest(quest_coach)
        
        # Quête du Champion - Quiz
        quest_champion = Quest(
            name="Quiz du Gamer",
            description="Répondre correctement au quiz du Champion pour gagner sa Manette dorée.",
            character="Champion",
            challenge_type="game",
            objective="Répondre correctement aux questions",
            reward_item=Item("Manette dorée", "le trophée du gamer", 0.5)
        )
        self.quest_manager.add_quest(quest_champion)
        
        # Quête de l'Ivre - Dés
        quest_ivre = Quest(
            name="Pari aux Dés",
            description="Battre l'ivrogne aux dés pour gagner sa Bouteille de vin.",
            character="Ivre",
            challenge_type="drink",
            objective="Gagner aux dés contre l'ivrogne",
            reward_item=Item("Bouteille de vin", "un grand cru convoité", 1.2)
        )
        self.quest_manager.add_quest(quest_ivre)
        
        # Quête du Vieux - Chifoumi
        quest_vieux = Quest(
            name="Pierre-Feuille-Ciseaux",
            description="Battre le vieux sage au chifoumi pour obtenir les Réponses aux examens.",
            character="Vieux",
            challenge_type="game",
            objective="Gagner au pierre-feuille-ciseaux",
            reward_item=Item("Réponses aux examens", "la clé de la réussite", 0.1)
        )
        self.quest_manager.add_quest(quest_vieux)
        
        # Quête d'exploration
        quest_explorateur = Quest(
            name="L'Explorateur Intrépide",
            description="Atteindre les 4 coins extrêmes du campus: Cave, Observatoire, Sauna et Terrasse.",
            character="Garde",
            challenge_type="location_multi",
            objective="Visiter: Cave, Observatoire, Sauna, Terrasse",
            reward_item=Item("Carte du campus", "révèle toutes les sorties avec descriptions", 0.1)
        )
        self.quest_manager.add_quest(quest_explorateur)
        
        # Quête de collection
        quest_collectionneur = Quest(
            name="Le Collectionneur",
            description="Rassembler les 3 objets de confort: RedBull, Part de pizza et Bouteille de vin.",
            character="Ivre",
            challenge_type="items_multi",
            objective="Posséder: RedBull, Part de pizza, Bouteille de vin",
            reward_item=Item("Coffre de rangement", "+2kg de capacité d'inventaire", 1.0)
        )
        self.quest_manager.add_quest(quest_collectionneur)

    def _create_characters(self):
        """Crée les personnages non-joueurs."""
        # Récupérer les quêtes
        quest_garde = self.quest_manager.get_quest_by_character("Garde")
        quest_coach = self.quest_manager.get_quest_by_character("Coach")
        quest_champion = self.quest_manager.get_quest_by_character("Champion")
        quest_ivre = self.quest_manager.get_quest_by_character("Ivre")
        quest_vieux = self.quest_manager.get_quest_by_character("Vieux")
        
        # Garde - À l'entrée
        garde = Character("Garde", "un colosse intimidant", self.rooms[0], quest_garde)
        self.characters.append(garde)
        
        # Ivre - Au bar
        ivre = Character("Ivre", "un membre éméché qui titube", self.rooms[7], quest_ivre)
        self.characters.append(ivre)
        
        # Champion - Salle de jeux
        champion = Character("Champion", "le geek ultime aux réflexes éclairs", self.rooms[11], quest_champion)
        self.characters.append(champion)
        
        # Coach - Salle de sport
        coach = Character("Coach", "le coach de boxe musclé", self.rooms[4], quest_coach)
        self.characters.append(coach)
        
        # Vieux - Observatoire (ne bouge pas)
        vieux = Character("Vieux", "l'ancien sage à la barbe blanche", self.rooms[10], quest_vieux)
        vieux.movement_enabled = False
        self.characters.append(vieux)

    def _handle_item_spawning(self):
        """Gère l'apparition aléatoire d'objets de décor."""
        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn_turn:
            self._spawn_random_item()
            self.spawn_timer = 0
            self.next_spawn_turn = random.randint(1, 5)

    def _spawn_random_item(self):
        """Fait apparaître un objet aléatoire dans une salle."""
        item_name = random.choice(list(self.spawnable_items.keys()))
        config = self.spawnable_items[item_name]
        
        # Compter combien de cet objet existent déjà
        current_count = 0
        for item in self.player.inventory:
            if item.name == item_name: 
                current_count += 1
        for room in self.rooms:
            for item in room.inventory:
                if item.name == item_name: 
                    current_count += 1
        
        # Ne pas dépasser le maximum
        if current_count < config['max']:
            random_room = random.choice(self.rooms)
            new_item = Item(item_name, config['desc'], config['weight'])
            random_room.add_item(new_item)
            if self.DEBUG:
                print(f"\n[INFO MONDE] Un {item_name} est apparu dans : {random_room.name} !")

    def win(self):
        """
        Vérifie si le joueur a gagné.
        
        Returns:
            bool: True si le joueur a gagné
        """
        # La victoire se déclenche uniquement dans le Bureau du Président
        return False
    
    def loose(self):
        """
        Vérifie si le joueur a perdu.
        
        Returns:
            bool: True si le joueur a perdu
        """
        if self.player.health <= 0:
            print("\n💀 Vous êtes K.O.")
            return True
        return False

    def play(self):
        """Boucle principale du jeu."""
        self.setup()
        self.print_welcome()
        
        while not self.finished:
            try:
                # Demander une commande
                command = input(f"\n{self.player.current_room.name} > ")
                should_move = self.process_command(command)
                
                # Mettre à jour l'état du jeu si nécessaire
                if should_move:
                    self.update_game_state()
                
                # Vérifier les conditions de fin
                if self.win() or self.loose():
                    self.finished = True
                    
            except KeyboardInterrupt:
                self.finished = True
            except Exception as e:
                print(f"Erreur: {e}")
                if self.DEBUG: 
                    traceback.print_exc()
        
        print("\nFin du jeu.")

    def update_game_state(self):
        """Met à jour l'état du jeu après un déplacement."""
        # Faire bouger les PNJ
        for character in self.characters:
            character.move()
        
        # Gérer l'apparition d'objets
        self._handle_item_spawning()

    def process_command(self, command_string):
        """
        Traite une commande entrée par le joueur.
        
        Args:
            command_string (str): La commande entrée
            
        Returns:
            bool: True si la commande déclenche un déplacement
        """
        if not command_string.strip(): 
            return False
        
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]
        
        if command_word in self.commands:
            command = self.commands[command_word]
            
            # Gestion spéciale pour "look" (ne déclenche pas de déplacement)
            if command_word == "look":
                command.action(self, list_of_words, command.number_of_parameters)
                return False
            
            # Exécuter l'action de la commande
            result = command.action(self, list_of_words, command.number_of_parameters)
            
            # Seul "go" réussi déclenche un déplacement
            if command_word == "go" and result:
                self.turn_count += 1
                
                # Réactiver le mouvement des PNJ
                for character in self.characters:
                    if hasattr(character, 'waiting_for_player_move'):
                        character.reset_movement_flags()
                
                return True
            
            # Les autres commandes font passer le temps sans déplacement
            elif command_word in ["talk", "use", "quests", "progress", "status", 
                                "check", "history", "back", "take", "drop"]:
                self.turn_count += 1
                return False
            
            return False
        
        else:
            print(f"\nCommande '{command_word}' inconnue.")
            return False

    def print_welcome(self):
        """Affiche le message de bienvenue et les instructions."""
        print(f"\n{'='*50}\nBIENVENUE DANS 'CAMPUS CRAWLER'\n{'='*50}")
        print(f"Bienvenue {self.player.name}.")
        print("Commandes utiles: go, talk, take, drop, use, status, quests, progress...")
        print("\n📜 Votre mission: Compléter des quêtes pour impressionner le président !")
        print("   Tapez 'quests' pour voir toutes les quêtes.")
        print("   Tapez 'progress' pour voir vos progrès sur les quêtes spéciales.")
        print(self.player.current_room.get_long_description())


if __name__ == "__main__":
    # Lancer le jeu
    Game().play()