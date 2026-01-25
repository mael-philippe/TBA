# Campus Crawler - Jeu d'Aventure Textuel

## Contexte du Jeu

Vous êtes étudiant(e) dans une nouvelle université et vous avez un objectif ambitieux : réussir l'année. Pour y parvenir, vous devez accomplir diverses quêtes, résoudre des énigmes, et démontrer en relevant des défis.

Votre mission : compléter au moins **4 quêtes** sur les 7 disponibles, collecter des objets trophées, et vous présenter devant le président de la fraternité pour revendiquer votre place.


## Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- Terminal/console de commande

### Lancement du jeu
1. Assurez-vous que tous les fichiers Python sont dans le même dossier :
actions.py, character.py, command.py, events.py, game.py, item.py, player.py, quest.py, room.py

2. Exécutez le jeu depuis votre terminal :
>>> python game.py

3. Suivez les instructions à l'écran et commencez votre aventure !


## Le jeu

### Objectifs du Jeu

#### Objectif principal

Compléter au moins 4 quêtes sur 7 pour prouver votre valeur et réussir votre année scolaire.

#### Quêtes disponibles

1. "Le Juste Prix" (Garde) : Devinez le code de sécurité

2. "Le Ring" (Coach) : Combat de boxe contre le coach

3. "Quiz du Gamer" (Champion) : Quiz sur les jeux vidéo

4. "Pari aux Dés" (Ivre) : Lancer de dés contre l'ivrogne

5. "Pierre-Feuille-Ciseaux" (Vieux) : Chifoumi contre le sage

6. "L'Explorateur Intrépide" (Garde) : Explorer les 4 coins du campus

7. "Le Collectionneur" (Ivre) : Collectionner 3 objets spécifiques

### Commandes disponibles

Déplacement et navigation :

    go <direction>      : Se déplacer (N, E, S, O, U=Up, D=Down)
    back                : Revenir à la salle précédente
    look                : Observer la salle actuelle (objets + PNJ)

Gestion des objets :

    take <objet>        : Prendre un objet dans la salle
    drop <objet>        : Déposer un objet de votre inventaire
    check               : Vérifier votre inventaire
    use <objet>         : Utiliser un objet spécial (GPS, Chien, consommables)

Intéractions sociales :

    talk <PNJ>          : Parler à un personnage non-joueur

(PNJ disponibles : Garde, Ivre, Champion, Coach, Vieux)

Informations et aide :

    status              : Afficher votre état (santé, inventaire, poids)
    history             : Voir l'historique des salles visitées
    quests              : Voir toutes les quêtes disponibles
    progress            : Suivre votre progression sur les quêtes spéciales
    help                : Afficher cette aide
    quit                : Quitter le jeu


### Mécaniques de jeu

#### Système de Santé

    Santé initiale : 100 points de vie

    Santé critique : < 30 points (affichage d'avertissement)

    Game Over : Si la santé atteint 0

    Soins : Via objets consommables (RedBull, Part de pizza)

#### Inventaire et Poids

    Capacité maximum : 5 kg (améliorable via quêtes)

    Poids des objets : Varies selon l'objet (0.1 à 2.7 kg)

    Vérification : check affiche le poids actuel/maximum

    Limites : Impossible de prendre un objet si trop lourd

#### Personnages (PNJ) et Quêtes

  Garde (Porte d'entrée)

    Quête principale : "Le Juste Prix"

    Mini-jeu : Deviner un nombre entre 1 et 100

    Récompense : Clé USB

  Coach (Salle de sport)

    Quête principale : "Le Ring"

    Mini-jeu : Combat de boxe (QTE)

    Récompense : Documents compromettants

  Champion (Salle de jeux)

    Quête principale : "Quiz du Gamer"

    Mini-jeu : Quiz sur les jeux vidéo

    Récompense : Manette dorée

  Ivre (Bar)

    Quête principale : "Pari aux Dés"

    Mini-jeu : Lancer de dés

    Récompense : Bouteille de vin

  Vieux (Observatoire)

    Quête principale : "Pierre-Feuille-Ciseaux"

    Mini-jeu : Chifoumi avec triche optionnelle

    Récompense : Réponses aux examens


#### Objets Spéciaux

🏆 Trophées (nécessaires pour gagner)

    Manette dorée, Bouteille de vin, Clé USB, Documents, Réponses aux examens

    Chaque trophée complété = +1 quête réussie

    Nécessite 4+ trophées pour gagner

🔧 Outils Utilitaires

    GPS : Localise tous les PNJ sur la carte

    Chien : Détecte les objets dans les salles adjacentes

🍖 Consommables

    RedBull : Restaure 30 points de vie

    Part de pizza : Restaure 50 points de vie


🎁 Récompenses de Quêtes

    Carte du campus (Explorateur) : Améliore les descriptions

    Coffre de rangement (Collectionneur) : +2 kg de capacité


#### Carte du jeu :

                         [Observatoire]  [Salle de Jeux]  [Terrasse]
                               |               |               |
                               |               |               |
                           [Bureau]---------[Dortoir]--------[Bar]
                               |               |               |
                               |               |               |
                               |               |               |
                         [Salle sport]-------[Hall]--------[Cuisine]
                               |               |               |
                               |               |               |
                               |               |               |
                            [Sauna]         [Entrée]        [Cave]

Légende des étages :

    Rez-de-chaussée : Entrée, Hall, Cuisine, Salle sport, Dortoir, Bar, Bureau

    Sous-sol : Sauna, Cave

    Étage supérieur : Salle de jeux, Terrasse, Observatoire


## Conseil de stratégie

1. Commencez par explorer : Utilisez look dans chaque salle et faites la quête du garde dès le début du jeu.

2. Gérez votre inventaire : Les trophées sont légers, conservez-les ! Les outils GPS/Chien sont très utiles mais peuvent être trop lourds, surtout en fin de partie.

3. Séquences recommandées :

- Parlez au Garde

- Récupérez le GPS dans la Cave et le Chien dans le Sauna

- Utilisez use GPS pour localiser facilement les PNJ

- Santé : Conservez toujours un consommable de soin pour les mini-jeux difficiles


## Guide développeur

### Architecture du Projet

TBA-project/

    ├── actions.py          # Toutes les actions/commandes du jeu
    ├── character.py        # Classe Character (PNJ avec mouvements)
    ├── command.py          # Système de commandes et parsing
    ├── events.py           # Mini-jeux et interactions spéciales
    ├── game.py             # Point d'entrée principal et boucle de jeu
    ├── item.py             # Classe Item (objets avec poids)
    ├── player.py           # Classe Player (inventaire, santé, historique)
    ├── quest.py            # Système de quêtes (Quest, QuestManager)
    ├── room.py             # Classe Room (salles avec inventaire)
    └── README.md           # Documentation


### Diagramme de classes







Diagrammes de Classes
<img width="950" height="998" alt="Diagramme de Classe Room" src="https://github.com/user-attachments/assets/925710a0-4013-4dc9-a7e1-066d88d1ff52" /><img width="1009" height="1147" alt="Diagramme de Classe Player" src="https://github.com/user-attachments/assets/6ca39591-4deb-48e4-9938-0515e09d7
