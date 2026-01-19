import traceback
import random
from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item
import events

class Game:
    DEBUG = True 
    
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.characters = []
        self.required_items = ["Clé USB", "Documents", "Livre des secrets"]
        
        # Gestion du temps
        self.turn_count = 0
        self.consecutive_look_count = 0
        
        # Gestion du spawn (objets aléatoires)
        self.spawn_timer = 0
        self.next_spawn_turn = random.randint(1, 5)
        self.spawnable_items = {
            "RedBull": {"max": 3, "desc": "boisson énergisante", "weight": 0.3},
            "Part de pizza": {"max": 2, "desc": "reste de la veille", "weight": 0.2}
        }
    
    def setup(self):
        # Ajout de la commande USE
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer", Actions.go, 1)
        self.commands["status"] = Command("status", " : afficher votre état", Actions.status, 0)
        self.commands["check"] = Command("check", " : inventaire", Actions.check, 0)
        self.commands["history"] = Command("history", " : historique", Actions.history, 0)
        self.commands["back"] = Command("back", " : retour arrière", Actions.back, 0)
        self.commands["talk"] = Command("talk", " <nom> : parler", Actions.talk, 1)
        self.commands["look"] = Command("look", " : observer", Actions.look, 0)
        self.commands["take"] = Command("take", " <objet> : prendre", Actions.take, 1)
        self.commands["drop"] = Command("drop", " <objet> : déposer", Actions.drop, 1)
        
        # NOUVELLE COMMANDE
        self.commands["use"] = Command("use", " <objet> : utiliser un objet spécial", Actions.use, 1)
        
        self._create_rooms()
        self._create_items() # On place les objets uniques ici
        self._create_characters()

    def _create_rooms(self):
        # (Tes salles restent identiques)
        entree = Room("Porte d'entrée", "devant l'entrée principale.")
        bar = Room("Bar", "dans le bar principal.")
        salon = Room("Salon VIP", "dans un salon luxueux.")
        cuisine = Room("Cuisine", "dans la cuisine.")
        salle_jeux = Room("Salle de jeux", "dans la salle de jeux.")
        jardin = Room("Jardin secret", "dans un jardin caché.")
        bureau = Room("Bureau du Président", "dans le bureau du chef.")
        cave = Room("Cave", "dans une cave sombre.")
        
        entree.exits = {"N": bar}
        bar.exits = {"S": entree, "E": salon, "O": cuisine, "N": salle_jeux}
        salon.exits = {"O": bar, "N": bureau}
        cuisine.exits = {"E": bar, "S": cave}
        salle_jeux.exits = {"S": bar, "N": jardin}
        jardin.exits = {"S": salle_jeux}
        bureau.exits = {"S": salon}
        cave.exits = {"N": cuisine}
        
        self.rooms = [entree, bar, salon, cuisine, salle_jeux, jardin, bureau, cave]
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = entree

    def _create_items(self):
        """Création des objets uniques (GPS, Chien)"""
        
        # 1. Le GPS (1.5 kg) - On le place dans la Cave (Zone technique)
        gps = Item("GPS", "un traqueur de PNJ haute technologie", 1.5)
        self.rooms[7].add_item(gps) # Cave
        
        # 2. Le Chien (2.7 kg) - On le place dans le Jardin
        chien = Item("Chien", "un fidèle compagnon au flair infaillible", 2.7)
        self.rooms[5].add_item(chien) # Jardin

        # Note: Les pizzas et redbulls sont gérés par le spawner automatique

    def _create_characters(self):
        garde = Character("Garde", "un colosse", self.rooms[0])
        garde.interaction_behavior = events.guard_interaction
        self.characters.append(garde)
        
        ivre = Character("Ivre", "un membre éméché", self.rooms[1])
        ivre.interaction_behavior = events.drunk_interaction
        self.characters.append(ivre)
        
        champion = Character("Champion", "le geek ultime", self.rooms[4])
        champion.interaction_behavior = events.champion_interaction
        self.characters.append(champion)
        
        coach = Character("Coach", "le coach de boxe", self.rooms[2])
        coach.interaction_behavior = events.captain_interaction 
        self.characters.append(coach)
        
        vieux = Character("Vieux", "l'ancien", self.rooms[5])
        vieux.interaction_behavior = events.old_member_interaction
        vieux.movement_enabled = False
        self.characters.append(vieux)

    def _handle_item_spawning(self):
        """Gère l'apparition aléatoire d'objets de décor"""
        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn_turn:
            self._spawn_random_item()
            self.spawn_timer = 0
            self.next_spawn_turn = random.randint(1, 5)

    def _spawn_random_item(self):
        item_name = random.choice(list(self.spawnable_items.keys()))
        config = self.spawnable_items[item_name]
        
        current_count = 0
        for item in self.player.inventory:
            if item.name == item_name: current_count += 1
        for room in self.rooms:
            for item in room.inventory:
                if item.name == item_name: current_count += 1
        
        if current_count < config['max']:
            random_room = random.choice(self.rooms)
            new_item = Item(item_name, config['desc'], config['weight'])
            random_room.add_item(new_item)
            if self.DEBUG:
                print(f"\n[INFO MONDE] Un {item_name} est apparu dans : {random_room.name} !")

    def win(self):
        required_trophies = ["Manette dorée", "Bouteille de vin", "Clé USB", "Documents", "Réponses aux examens"]
        trophies_count = sum(1 for item in self.player.inventory if item.name in required_trophies)
        if trophies_count >= 4:
            print("\n🏆 VICTOIRE ABSOLUE ! 🏆")
            print("Vous avez vaincu la fraternité Mystik !")
            return True
        return False
    
    def loose(self):
        if self.player.health <= 0:
            print("\n💀 Vous êtes K.O.")
            return True
        if self.player.current_room.name == "Bureau du Président":
            boss_items = sum(1 for item in self.player.inventory if item.weight in [0.5, 1.2, 0.1])
            if boss_items < 2:
                print("\n⛔ Le Président vous vire du bureau !")
                return True
        return False

    def play(self):
        self.setup()
        self.print_welcome()
        
        while not self.finished:
            try:
                command = input(f"\n{self.player.current_room.name} > ")
                should_move = self.process_command(command)
                
                if should_move:
                    self.update_game_state()
                
                if self.win() or self.loose():
                    self.finished = True
                    
            except KeyboardInterrupt:
                self.finished = True
            except Exception as e:
                print(f"Erreur: {e}")
                if self.DEBUG: traceback.print_exc()
        
        print("\nFin du jeu.")

    def update_game_state(self):
        for character in self.characters:
            character.move()
        self._handle_item_spawning()

    def process_command(self, command_string):
        if not command_string.strip(): return False
        
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]
        
        if command_word in self.commands:
            command = self.commands[command_word]
            
            # Gestion LOOK (temps)
            if command_word == "look":
                command.action(self, list_of_words, command.number_of_parameters)
                self.consecutive_look_count += 1
                if self.consecutive_look_count >= 3:
                    print("\n(Le temps passe...)")
                    self.consecutive_look_count = 0
                    return True
                return False

            self.consecutive_look_count = 0
            
            result = command.action(self, list_of_words, command.number_of_parameters)
            
            # Actions qui font passer le temps
            action_takes_time = (command_word == "go" and result) or \
                                (command_word == "talk") or \
                                (command_word == "use") # Utiliser un objet prend du temps aussi !
            
            if action_takes_time:
                self.turn_count += 1
                if self.turn_count <= 3: return False
                elif self.turn_count % 2 == 0: return True
                else: return True # Le temps passe pour le spawn, même si PNJ bougent pas
            
            return False
        else:
            print(f"\nCommande '{command_word}' inconnue.")
            return False

    def print_welcome(self):
        print(f"\n{'='*50}\nBIENVENUE DANS 'INFILTRATION MYSTIK'\n{'='*50}")
        print(f"Bienvenue {self.player.name}.")
        print("Commandes utiles: go, talk, take, drop, use, status...")
        print(self.player.current_room.get_long_description())

if __name__ == "__main__":
    Game().play()