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

    go <direction> : se déplacer dans une direction cardinale (N, E, S, O, U=Up, D=Down)

    back : revenir à la salle précédente

    look : observer attentivement la salle actuelle

Gestion des Objets

    take <nom_objet> : prendre un objet dans la salle (ex: take Clé USB, take Documents)

    drop <nom_objet> : déposer un objet de votre inventaire dans la salle

    check : vérifier le contenu de votre inventaire avec le poids actuel

    Astuce : Les noms composés sont acceptés (ex: take Clé USB, drop Bouteille de vin)

Interactions Sociales

    talk <nom_personnage> : parler à un personnage présent dans la salle

    Personnages disponibles : Garde, Ivre, Champion, Coach, Vieux

Information et Aide

    status : afficher votre état de santé et vos statistiques

    history : afficher l'historique des salles visitées

    help : afficher la liste des commandes disponibles

    quit : quitter le jeu

Nouvelles Salles

    Observatoire : Au-dessus du bureau du président, avec le Vieux

    Terrasse : Au-dessus du bar, avec vue panoramique

    Sauna : En-dessous de la salle de sport, endroit relaxant

Mécaniques de Jeu
Système d'Inventaire

    Capacité : 5 kg maximum

    Poids des objets : Chaque objet a un poids différent

    Affichage : check montre le poids actuel/5 kg

    Messages : Confirmations claires quand vous prenez/déposez des objets

Points de Vie

    Démarrage : 100 points de vie

    Perte de vie : Certaines interactions vous font perdre des points

    Game Over : Si vos points tombent à 0

    Soins : Certains objets/choix restaurent de la vie

Personnages Interactifs

Chaque personnage propose des défis différents :

    Garde (Porte d'entrée) : contrôle l'accès à la fraternité

    Ivre (Bar) : défis alcoolisés dans le bar

    Champion (Salle de jeux) : jeux vidéo et quiz

    Coach (Salle de sport) : combat de boxe et réflexes

    Vieux (Observatoire) : histoires et secrets dans l'observatoire

Objets à Collecter

    Preuves : Documents, Clé USB, Réponses aux examens

    Utilitaires : GPS (trouve les PNJ), Chien (sent les objets)

    Consommables : RedBull, Part de pizza

Conseils de Jeu

    Utilisez U (Up) et D (Down) pour naviguer entre les étages

    Parlez à tous les personnages pour découvrir des objets cachés

    Utilisez look dans chaque salle pour ne rien manquer

    Surveillez votre poids avec check (limite 5 kg)

    Collectez au moins 4 objets spéciaux pour gagner

    Faites attention à votre santé avec status

Carte du jeu :

                           [Observatoire]     [Terrasse]
                                   |              |
                                   D              D
                           [Bureau]---[Dortoir]---[Bar]
                                   |      |       |
                                   |      U       U
                                   |      |       |
                         [Salle sport]--[Hall]--[Cuisine]
                                   |      |       |
                                   D      S       D
                                   |      |       |
                            [Sauna]   [Entrée] [Cave]

Légende des étages :
- Rez-de-chaussée : Entrée, Hall, Cuisine, Cave, Salle sport, Sauna
- Étage 1 : Dortoir, Bar, Bureau
- Étage 2 : Salle de jeux, Terrasse, Observatoire

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

Nouvelles Fonctionnalités

1. Directions verticales :
   - U (Up) : Monter d'un étage
   - D (Down) : Descendre d'un étage

2. Nouvelles salles :
   - Observatoire : Salle thématique pour le Vieux
   - Terrasse : Point de vue élevé
   - Sauna : Zone de détente sous la salle de sport

3. Réorganisation logique :
   - PNJ placés dans des salles cohérentes avec leur rôle
   - Objets spéciaux dans des lieux pertinents
   - Architecture à 3 niveaux (rez-de-chaussée, étage 1, étage 2)

Diagrammes de Classes
<img width="950" height="998" alt="Diagramme de Classe Room" src="https://github.com/user-attachments/assets/925710a0-4013-4dc9-a7e1-066d88d1ff52" /><img width="1009" height="1147" alt="Diagramme de Classe Player" src="https://github.com/user-attachments/assets/6ca39591-4deb-48e4-9938-0515e09d7