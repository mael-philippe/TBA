Infiltration Mystik - Jeu d'Aventure Textuel
Guide Utilisateur
Installation et Lancement

La première version du jeu se joue dans le terminal et utilise les 7 fichiers .py (actions, character, command, events, game, player & room). Pour initier la partie, il faut ouvrir ces fichiers et exécuter le programme game.py.
Contexte du Jeu

Le jeu se déroule dans une université. Le but du jeu est de s'infiltrer dans une fraternité adverse à celle du joueur et la faire capituler à travers de nombreuses interactions et épreuves. Le joueur fait partie de la fraternité Banditos et la fraternité ennemie est Mystik.
Objectif

Pour gagner, il faut collecter suffisamment de preuves compromettantes sur les Mystik tout en restant en vie, car certaines interactions peuvent faire perdre au joueur des points de vie.
Commandes Disponibles
Déplacement et Navigation

    go <direction> : se déplacer dans une direction cardinale (N, E, S, O)

    back : revenir à la salle précédente

    look : observer attentivement la salle actuelle (déclenche parfois des événements)

Interactions Sociales

    talk <nom_personnage> : parler à un personnage présent dans la salle

    Exemples : talk Garde, talk Champion, talk Vieux Membre

Gestion du Personnage

    status : afficher votre état de santé et vos statistiques

    inventory : afficher votre inventaire

    history : afficher l'historique des salles visitées

Commandes Système

    help : afficher la liste des commandes disponibles

    quit : quitter le jeu

Mécaniques de Jeu
Points de Vie

    Démarrez avec 100 points de vie

    Certaines interactions peuvent vous faire perdre des points de vie

    Si vos points de vie tombent à 0, c'est Game Over

    Vous pouvez récupérer de la vie en trouvant des objets ou en faisant les bons choix

Inventaire

    Collectez des preuves compromettantes pour faire tomber les Mystik

    Certains objets sont essentiels pour gagner la partie

    Utilisez inventory pour vérifier ce que vous avez collecté

Personnages Interactifs

Chaque salle peut contenir des personnages avec lesquels vous pouvez interagir :

    Garde à l'entrée : contrôle l'accès à la fraternité

    Membre Ivre au bar : propose des défis alcoolisés

    Champion en salle de jeux : maître des jeux vidéo

    Capitaine en salle de sport : expert en combat

    Vieux Membre dans la cave : détenteur de secrets

Exploration

Utilisez look pour explorer les salles sans personnage :

    Cuisine : cherchez de la nourriture et des boissons

    Dortoir : trouvez des objets utiles

    Bureau du président : recherchez des preuves compromettantes

    Toit : découvrez le livre des secrets

Conseils de Jeu

    Parlez à tous les personnages que vous rencontrez

    Explorez chaque salle avec look pour ne rien manquer

    Faites attention à vos points de vie

    Collectez au moins 2 preuves compromettantes pour gagner

    Utilisez back pour revenir sur vos pas si nécessaire

Guide Développeur
Architecture du Jeu

Le jeu suit une architecture orientée objet avec les classes suivantes :
Diagrammes de Classes
<img width="950" height="998" alt="Diagramme de Classe Room" src="https://github.com/user-attachments/assets/925710a0-4013-4dc9-a7e1-066d88d1ff52" />

<img width="1009" height="1147" alt="Diagramme de Classe Player" src="https://github.com/user-attachments/assets/6ca39591-4deb-48e4-9938-0515e09d7a22" />

<img width="1755" height="844" alt="Diagramme de Classe Command" src="https://github.com/user-attachments/assets/70279d1d-614e-4071-879a-1447cdc63d9a" />

<img width="1735" height="924" alt="Diagramme de Classe Actions" src="https://github.com/user-attachments/assets/96c05ce0-90f0-4d57-8823-b194d08ff618" />

    name : nom du personnage

    description : description du personnage

    interaction_event : fonction d'interaction

    already_interacted : état de l'interaction

Classe Room (modifiée)

    characters : liste des personnages présents

    event_triggered : pour les événements de type "look"

    Méthodes ajoutées :

        add_character() : ajouter un personnage

        interact_with_character() : interagir avec un personnage spécifique

Classe Player (modifiée)

    history : historique des salles visitées

    Méthode move() : affiche maintenant les personnages présents

Système d'Événements

    Événements sociaux : déclenchés par talk <nom>

    Événements d'exploration : déclenchés par look

Fichiers du Projet

    game.py : Point d'entrée principal, gestion du jeu

    player.py : Classe du joueur et gestion des déplacements

    room.py : Classe des salles avec personnages

    character.py : Nouvelle classe pour les personnages interactifs

    command.py : Système de commandes

    actions.py : Implémentation des actions

    events.py : Événements d'interaction et d'exploration

Flux du Programme

    Initialisation du jeu dans Game.setup()

    Création des salles et ajout des personnages

    Boucle principale de traitement des commandes

    Gestion des interactions via le système de commandes

Ajout de Nouveaux Contenus
Pour ajouter un nouveau personnage :

    Créer une fonction d'événement dans events.py

    Créer une instance de Character dans game.py

    L'ajouter à une salle avec add_character()

Pour ajouter une nouvelle salle :

    Créer une instance de Room dans game.py

    Configurer ses sorties

    Ajouter des personnages si nécessaire

Pour ajouter une nouvelle commande :

    Ajouter la méthode dans Actions (actions.py)

    Créer la Command correspondante dans Game.setup()

    Mettre à jour le message d'aide

Perspectives de Développement

Pour améliorer notre jeu, nous pourrions :

    Contenu additionnel :

        Ajouter plus de salles/étages

        Créer plus de personnages avec des dialogues variés

        Ajouter des objets interactifs supplémentaires

    Améliorations techniques :

        Système de sauvegarde/chargement

        Interface graphique simple

        Effets sonores

    Gameplay avancé :

        Système de compétences ou de sorts

        Quêtes secondaires

        Système de réputation avec les Mystik

        Événements aléatoires

    Expérience utilisateur :

        Système de hints/intelligence artificielle

        Journal de quêtes

        Carte du monde accessible

        Difficultés ajustables

    Contenu narratif :

        Histoire plus développée

        Dialogues branches avec conséquences

        Personnages récurrents avec développements

        Plusieurs fins possibles

Notes Techniques

    Le jeu utilise un système de commandes modulaire

    Les interactions sont gérées par des fonctions d'événement

    L'historique des salles est implémenté avec une pile

    Le système de santé et d'inventaire est simple mais extensible

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
