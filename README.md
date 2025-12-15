Infiltration Mystik - Jeu d'Aventure Textuel
Guide Utilisateur
Installation et Lancement

Le jeu se joue dans le terminal et utilise les 8 fichiers .py (actions, character, command, events, game, item, player & room). Pour initier la partie, exécutez le programme game.py.
Contexte du Jeu

Le jeu se déroule dans une université. Le but du jeu est de s'infiltrer dans la fraternité Mystik, collecter des preuves compromettantes et la faire capituler. Vous êtes membre de la fraternité Banditos.
Objectif

Collecter suffisamment de preuves (au moins 2) sur les Mystik tout en restant en vie. Certaines interactions peuvent vous faire perdre des points de vie.
Commandes Disponibles
Déplacement et Navigation

    go <direction> : se déplacer dans une direction cardinale (N, E, S, O)

    back : revenir à la salle précédente

    look : observer attentivement la salle actuelle

Gestion des Objets

    take <nom_objet> : prendre un objet dans la salle (ex: take Clé USB, take Documents)

    drop <nom_objet> : déposer un objet de votre inventaire dans la salle

    check : vérifier le contenu de votre inventaire avec le poids actuel

    Astuce : Les noms composés sont acceptés (ex: take Clé USB, drop Bouteille de vin)

Interactions Sociales

    talk <nom_personnage> : parler à un personnage présent dans la salle

    Personnages disponibles : Garde, Ivre, Champion, Capitaine, Vieux

Information et Aide

    status : afficher votre état de santé et vos statistiques

    history : afficher l'historique des salles visitées

    help : afficher la liste des commandes disponibles

    quit : quitter le jeu

Mécaniques de Jeu
Système d'Inventaire

    Capacité : 20 kg maximum

    Poids des objets : Chaque objet a un poids différent

    Affichage : check montre le poids actuel/20 kg

    Messages : Confirmations claires quand vous prenez/déposez des objets

Points de Vie

    Démarrage : 100 points de vie

    Perte de vie : Certaines interactions vous font perdre des points

    Game Over : Si vos points tombent à 0

    Soins : Certains objets/choix restaurent de la vie

Personnages Interactifs

Chaque personnage propose des défis différents :

    Garde (Porte d'entrée) : contrôle l'accès

    Ivre (Bar) : défis alcoolisés

    Champion (Salle de jeux) : jeux vidéo

    Capitaine (Salle de sport) : combat de boxe

    Vieux (Cave) : histoires et secrets

Objets à Collecter

    Preuves : Documents, Photos, Livre des secrets, Clé USB

    Utilitaires : RedBull, Trousse de secours, Pizza

    Spéciaux : Beamer (téléportation), Bouteille de vin rare

Conseils de Jeu

    Parlez à tous les personnages pour découvrir des objets cachés

    Utilisez look dans chaque salle pour ne rien manquer

    Surveillez votre poids avec check (limite 20 kg)

    Collectez au moins 2 preuves pour gagner

    Faites attention à votre santé avec status

Guide Développeur
Architecture du Projet
text

TBA-main/
├── actions.py          # Implémentation des commandes
├── character.py        # Classe Character pour les PNJ
├── command.py          # Système de commandes
├── events.py           # Événements d'interaction
├── game.py             # Point d'entrée principal
├── item.py             # Classe Item pour les objets
├── player.py           # Classe Player avec inventaire
├── room.py             # Classe Room avec inventaire
└── README.md           # Documentation

Diagrammes de Classes
<img width="950" height="998" alt="Diagramme de Classe Room" src="https://github.com/user-attachments/assets/925710a0-4013-4dc9-a7e1-066d88d1ff52" /><img width="1009" height="1147" alt="Diagramme de Classe Player" src="https://github.com/user-attachments/assets/6ca39591-4deb-48e4-9938-0515e09d7a22" /><img width="1755" height="844" alt="Diagramme de Classe Command" src="https://github.com/user-attachments/assets/70279d1d-614e-4071-879a-1447cdc63d9a" /><img width="1735" height="924" alt="Diagramme de Classe Actions" src="https://github.com/user-attachments/assets/96c05ce0-90f0-4d57-8823-b194d08ff618" />
Système d'Inventaire - Conception
1. Classe Item (item.py)
python

class Item:
    def __init__(self, name, description, weight):
        self.name = name          # Nom de l'objet
        self.description = description  # Description
        self.weight = weight      # Poids en kg
    
    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

2. Inventaire du Joueur (player.py)

Structure de données choisie : Liste

    self.inventory = [] : Liste d'objets Item

    self.max_weight = 20.0 : Limite de poids

    self.current_weight : Calcul dynamique

Fonctions clés :

    add_item(item) : Ajoute avec vérification de poids

    remove_item(item_name) : Retire (insensible à la casse)

    get_current_weight() : Calcule le poids total

    can_take_item(item) : Vérifie la capacité

    get_inventory_string() : Formatage d'affichage

3. Inventaire des Salles (room.py)

Même structure pour cohérence :

    self.inventory = [] : Liste d'objets Item

    Méthodes similaires à Player pour l'interface

Gestion des Commandes
Validation des Paramètres
python

def take(game, list_of_words, number_of_parameters):
    l = len(list_of_words)
    if l < 2:  # Vérifie qu'il y a au moins commande + paramètre
        print(f"La commande '{list_of_words[0]}' prend 1 paramètre.")
        return False

Gestion des Noms Composés
python

# "take Clé USB spéciale" → ["take", "Clé", "USB", "spéciale"]
item_name_parts = list_of_words[1:]  # ["Clé", "USB", "spéciale"]
item_name = " ".join(item_name_parts)  # "Clé USB spéciale"

Recherche Insensible à la Casse
python

def remove_item(self, item_name):
    item_name_lower = item_name.lower()  # "clé usb"
    for item in self.inventory:
        if item.name.lower() == item_name_lower:  # Compare en minuscules
            return self.inventory.pop(i)

Flux de Données
text

┌─────────┐    take    ┌─────────┐
│  Salle  │───────────▶│ Joueur  │
│inventory│◀───────────│inventory│
└─────────┘    drop    └─────────┘
     │                       │
     │ add_item()            │ get_inventory_string()
     │ remove_item()         │ check command
     ▼                       ▼
┌─────────────────┐   ┌──────────────────┐
│ Room.get_item() │   │ Player.check()   │
└─────────────────┘   └──────────────────┘

Caractéristiques Techniques
1. Séparation des responsabilités

    Item : Définition des objets

    Player : Gestion de l'inventaire personnel

    Room : Gestion des objets dans l'environnement

    Actions : Implémentation des commandes

2. Validation robuste

    Vérification du poids maximum

    Messages d'erreur explicites

    Gestion des cas limites (objet non trouvé, inventaire plein)

3. Interface utilisateur avancée

    Noms composés acceptés (take Clé USB)

    Insensibilité à la casse (take clé usb, take CLÉ USB)

    Messages de confirmation avec emojis

    Affichage formaté du poids

4. Extensibilité

    Ajout facile de nouveaux objets

    Structure prête pour objets spéciaux (clés, potions, etc.)

    Séparation claire entre données et logique

Exemple d'Exécution
text

> look
Vous êtes dans la salle de jeux...
Objets dans la salle:
    1. Clé USB : clé USB avec des données sensibles (0.1 kg)

> take Clé USB
🎒 Vous avez pris 'Clé USB'.

> check
🎒 Inventaire (0.1/20 kg):
    1. Clé USB : clé USB avec des données sensibles (0.1 kg)

> drop clé usb  
📦 Vous avez déposé 'Clé USB'.

Fonctionnalités Implémentées

- Système d'objets complet avec poids et descriptions
- Double inventaire (joueur + salles) avec transfert
- Limite de poids (20 kg maximum)
- Commandes avancées avec noms composés
- Recherche insensible à la casse
- Messages d'erreur et de confirmation
- Historique des déplacements
- Système de santé avec soins et dégâts
- Personnages interactifs avec dialogues
- Sauvegarde automatique de l'historique
- Perspectives d'Amélioration

    Objets spéciaux :

        Beamer (téléportation)

        Clés pour portes verrouillées

        Potions de soin instantané

        Cartes pour navigation

    Améliorations techniques :

        Système de sauvegarde/chargement

        Interface graphique simple

        Effets sonores

        Journal de quêtes

    Contenu additionnel :

        Plus de salles et d'étages

        Dialogues branches avec conséquences

        Quêtes secondaires

        Système de réputation

    Gameplay avancé :

        Combats tour par tour

        Compétences et sorts

        Crafting d'objets

        Événements aléatoires

Notes de Conception
Choix de la liste pour l'inventaire

    Avantages : Conservation de l'ordre d'acquisition, parcours simple

    Alternative envisagée : Dictionnaire pour accès rapide par nom

    Décision : Liste pour simplicité et cohérence avec l'affichage numéroté

Gestion du poids

    Calcul dynamique à chaque ajout/suppression

    Vérification avant transfert pour éviter les états invalides

    Affichage clair du poids restant

Messages utilisateur

    Emojis pour améliorer l'expérience visuelle

    Messages différents pour succès/échec

    Formatage cohérent pour toutes les commandes

Carte du jeu :
                               [TOIT]                                              N
                                 |                                                 ↑                                
                                 |                                            O ←  0  → E                                                            
                [DORTOIR]--[SALLE DE JEUX]--[BUREAU DU PRÉSIDENT]                  ↓
                    |            |                     |                           S
                    |            |                     | 
            [SALLE DE SPORT]---[BAR]---------------[CUISINE]
                    |            |
                    |            | 
                [CAVE]     [PORTE D'ENTRÉE]
