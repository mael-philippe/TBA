import random
import time
import string
from item import Item

def guard_interaction(player, game):
    """Mini-jeu pour le Garde (Le Juste Prix / Code de Sécurité)"""
    nom_objet = "Clé USB"
    
    print("\n=== LE GARDE DE LA PORTE ===")
    print("Le colosse croise les bras et bloque le passage.")
    print("« Hé toi ! C'est une zone restreinte. »")
    print("« Seuls ceux qui connaissent le code de sécurité du jour peuvent passer. »")
    print(f"« Si tu me le donnes, je te laisse entrer et je te file ma {nom_objet} de secours. »")
    print("« Sinon... je vais devoir t'apprendre les bonnes manières. »")
    
    # Vérif si déjà gagné
    deja_gagne = any(i.name == nom_objet for i in player.inventory)

    choix = input("\nEssayez-vous de deviner le code ? (O/N) > ").upper()
    if choix != "O":
        print("\n« C'est ça, circule avant que je m'énerve. »")
        return False

    # Génération du code
    code_secret = random.randint(1, 100)
    essais_max = 6
    print(f"\n🔐 Le Garde attend un nombre entre 1 et 100.")
    print(f"Vous avez {essais_max} tentatives.")

    for i in range(1, essais_max + 1):
        try:
            guess = int(input(f"\nEssai {i}/{essais_max} > "))
        except ValueError:
            print("« Des chiffres, imbécile ! Pas des lettres ! » (Essai gâché)")
            continue

        if guess < code_secret:
            print("Garde : « Plus grand ! »")
        elif guess > code_secret:
            print("Garde : « Plus petit ! »")
        else:
            # VICTOIRE
            print(f"\n🔓 « {guess} »... C'est exact.")
            print("Le Garde semble impressionné (et un peu déçu de ne pas pouvoir taper).")
            print("« Ok, t'es clean. Tiens, prends ça au cas où. »")
            
            if not deja_gagne:
                recompense = Item(nom_objet, "les codes de sécurité", 0.1)
                # VÉRIFIER si le joueur peut prendre l'objet
                if player.can_take_item(recompense):
                    player.inventory.append(recompense)
                    print(f"\n🎁 Vous recevez : {nom_objet} !")
                else:
                    print(f"\n💔 Le garde vous tend {nom_objet}, mais vous n'avez plus de place !")
                    print("   L'objet tombe au sol.")
                    # Ajouter l'objet à la salle actuelle
                    player.current_room.add_item(recompense)
            else:
                print("« Attends, tu as déjà un pass ! Passe ton chemin. »")
            return True

    # DÉFAITE (Boucle finie sans trouver)
    print(f"\n🚨 « FAUX ! Le code était {code_secret} ! »")
    print("« Intrus détecté ! Suppression immédiate ! »")
    print("Le Garde vous attrape par le col et vous jette contre le mur.")
    player.take_damage(25)
    return False

def captain_interaction(player, game):
    """Mini-jeu pour le Coach de Boxe (QTE / Réflexes)"""
    nom_objet = "Documents"
    
    print("\n=== LE RING DU COACH ===")
    print("Le Coach vous regarde de haut en bas en enfilant ses gants.")
    print("« Tu veux te frotter au meilleur coach de boxe de l'école ? »")
    print(f"« Si tu tiens 3 rounds, je te file les {nom_objet} compromettants. »")
    
    deja_gagne = any(i.name == nom_objet for i in player.inventory)

    if input("\nAcceptez-vous le défi ? (O/N) > ").upper() != "O":
        print("\n« C'est bien ce que je pensais. File, gringalet. »")
        return False

    # Explication des règles
    print("\n🔔 --- RÈGLES DU COMBAT --- 🔔")
    print("Le Coach va annoncer un coup. Vous devez esquiver !")
    print("Une lettre aléatoire (ex: 'a', 'm', 'z') va s'afficher.")
    print("1. Regardez la lettre.")
    print("2. Tapez-la et appuyez sur ENTRÉE le plus vite possible.")
    print("\nAttention aux délais :")
    print(" - DIRECT   : Très rapide (2.0 sec) | -20 PV")
    print(" - CROCHET  : Moyen       (2.5 sec) | -40 PV")
    print(" - UPPERCUT : Lent        (3.0 sec) | -75 PV")
    print("\nConditions : Esquivez 3 coups. Si vous en prenez 2, c'est PERDU.")

    input("\nAppuyez sur ENTRÉE pour monter sur le ring...")

    # Configuration des coups
    coups_possibles = [
        {"nom": "DIRECT",   "temps": 2.0, "degats": 20},
        {"nom": "CROCHET",  "temps": 2.5, "degats": 40},
        {"nom": "UPPERCUT", "temps": 3.0, "degats": 75}
    ]

    esquives_reussies = 0
    coups_recus = 0
    
    # Boucle de jeu (3 rounds max, arrêt si 2 coups reçus)
    while esquives_reussies < 3 and coups_recus < 2:
        print(f"\n🥊 ROUND {esquives_reussies + coups_recus + 1}")
        
        # Choisir un coup et une lettre
        coup = random.choice(coups_possibles)
        lettre_cible = random.choice(string.ascii_lowercase) # Une lettre de a à z
        
        print("Le Coach prépare son coup...")
        time.sleep(random.uniform(1.0, 2.0)) # Petit temps de suspense
        
        print(f"\n🔥 {coup['nom']} !!! Tapez '{lettre_cible}' !")
        
        # Chronomètre
        start_time = time.time()
        reponse = input("> ").strip().lower()
        end_time = time.time()
        
        duree = end_time - start_time
        
        # Vérification
        if reponse == lettre_cible and duree <= coup['temps']:
            print(f"✅ ESQUIVE RÉUSSIE ! ({duree:.2f}s / {coup['temps']}s)")
            esquives_reussies += 1
        else:
            if reponse != lettre_cible:
                print(f"❌ MAUVAISE TOUCHE ! (Vous avez tapé '{reponse}' au lieu de '{lettre_cible}')")
            else:
                print(f"❌ TROP LENT ! ({duree:.2f}s > {coup['temps']}s)")
            
            print(f"💥 BIM ! Vous prenez un {coup['nom']} en pleine face !")
            coups_recus += 1
            if player.take_damage(coup['degats']): # Si le joueur meurt
                return False

    # Résultat final
    if coups_recus >= 2:
        print("\n🤕 DÉFAITE PAR K.O. TECHNIQUE")
        print("Le Coach vous jette une serviette humide au visage.")
        print("« T'as encore du boulot, gamin. »")
        return False
    else:
        print("\n👑 VICTOIRE SUR LE RING !")
        print("Le Coach, essoufflé, baisse sa garde.")
        print("« Pas mal... T'as des réflexes de chat. Chose promise, chose due. »")
        
        if not deja_gagne:
            recompense = Item(nom_objet, "des preuves de matchs truqués", 0.5)
            # VÉRIFIER si le joueur peut prendre l'objet
            if player.can_take_item(recompense):
                player.inventory.append(recompense)
                print(f"\n🎁 Vous recevez : {nom_objet} !")
            else:
                print(f"\n💔 Le coach vous tend {nom_objet}, mais vous n'avez plus de place !")
                print("   L'objet tombe au sol.")
                # Ajouter l'objet à la salle actuelle
                player.current_room.add_item(recompense)
        else:
            print("« Mais tu as déjà les papiers ! Fiche le camp maintenant. »")
        return True

def champion_interaction(player, game):
    """Mini-jeu pour le Champion (Quiz)"""
    nom_objet = "Manette dorée"
    print("\n=== LE DÉFI DU CHAMPION ===")
    print(f"« Si tu réponds correctement, je te donnerai ma {nom_objet} ! »")
    
    deja_gagne = any(i.name == nom_objet for i in player.inventory)
    if input("\n(O/N) > ").upper() != "O": return False

    questions = [
        {"text": "Lequel est un battle royale ?", "correct": "Fortnite", "others": ["Star Fox", "Luigi's Mansion"]},
        {"text": "Lequel est un Souls ?", "correct": "Elden Ring", "others": ["Monster Hunter", "Stardew Valley"]},
        {"text": "Nom d'un adversaire RPG ?", "correct": "Un mob", "others": ["Un noob", "Un adversaire"]}
    ]
    random.shuffle(questions)

    for q in questions:
        print(f"\n❓ {q['text']}")
        options = [q['correct']] + q['others']
        random.shuffle(options)
        for idx, opt in enumerate(options, 1): print(f"   {idx}) {opt}")
        
        try:
            rep = int(input("Choix > "))
            if options[rep-1] != q['correct']: raise ValueError
            print("✅ Correct !")
        except:
            print(f"❌ Faux ! C'était {q['correct']}.")
            player.take_damage(35)
            return False

    print("\n🏆 « GG ! Tu gères. »")
    if not deja_gagne:
        recompense = Item(nom_objet, "le trophée du gamer", 0.5)
        # VÉRIFIER si le joueur peut prendre l'objet
        if player.can_take_item(recompense):
            player.inventory.append(recompense)
            print(f"\n🎁 Vous recevez : {nom_objet} !")
        else:
            print(f"\n💔 Le Geek vous tend {nom_objet}, mais vous n'avez plus de place !")
            print("   L'objet tombe au sol.")
            # Ajouter l'objet à la salle actuelle
            player.current_room.add_item(recompense)
    else:
        print("(Il cherche sa manette...) « Ah mince, je te l'ai déjà donnée ! »")
    return True

def drunk_interaction(player, game):
    """Mini-jeu pour l'Ivre (Dés)"""
    nom_objet = "Bouteille de vin"
    print("\n=== LE DÉFI DE L'IVROGNE ===")
    print("« Je te parie ma meilleure bouteille aux dés ! »")
    
    deja_gagne = any(i.name == nom_objet for i in player.inventory)
    if input("\n(O/N) > ").upper() != "O": return False

    score_ivre = random.randint(1, 6)
    print(f"\n🎲 Ivre : {score_ivre}")
    input("Entrée pour lancer...")
    score_joueur = random.randint(1, 6)
    print(f"🎲 Vous : {score_joueur}")

    if score_joueur > score_ivre:
        print("✨ GAGNÉ !")
        if not deja_gagne:
            recompense = Item(nom_objet, "un grand cru convoité", 1.2)
            # VÉRIFIER si le joueur peut prendre l'objet
            if player.can_take_item(recompense):
                player.inventory.append(recompense)
                print(f"\n🎁 Vous recevez : {nom_objet} !")
            else:
                print(f"\n💔 L'ivrogne vous tend {nom_objet}, mais vous n'avez plus de place !")
                print("   L'objet tombe au sol.")
                # Ajouter l'objet à la salle actuelle
                player.current_room.add_item(recompense)
        else:
            print("« Hips... Je t'ai déjà tout donné je crois... »")
        return True
    elif score_joueur < score_ivre:
        print("💀 PERDU ! Vous buvez.")
        player.take_damage(30)
        return False
    else:
        print("😐 ÉGALITÉ.")
        return False

def old_member_interaction(player, game):
    """Mini-jeu du Vieux (PFC)"""
    nom_objet = "Réponses aux examens"
    print("\n=== LE VIEUX SAGE ===")
    print("« Jouons ! Je parie les réponses aux examens. »")
    
    deja_gagne = any(i.name == nom_objet for i in player.inventory)
    if input("\n(O/N) > ").upper() != "O": return False

    print("\n1. Se boucher les oreilles\n2. Écouter (Tricher, -95 PV)")
    triche = input("> ") == "2"
    if triche:
        print("💥 La culpabilité vous ronge : -95 PV !")
        if player.take_damage(95): return False

    vic_j, vic_v = 0, 0
    coups = ["Pierre", "Feuille", "Ciseaux"]
    
    while vic_j < 2 and vic_v < 2:
        coup_v = random.choice(coups)
        if triche: print(f"(Il va jouer {coup_v}...)")
        
        print("\n1.Pierre 2.Feuille 3.Ciseaux")
        try:
            c = int(input("> "))
            coup_j = coups[c-1]
        except: coup_j = "Rien"

        print(f"Vous: {coup_j} vs Vieux: {coup_v}")
        if coup_j == coup_v: continue
        
        win = (coup_j=="Pierre" and coup_v=="Ciseaux") or \
              (coup_j=="Feuille" and coup_v=="Pierre") or \
              (coup_j=="Ciseaux" and coup_v=="Feuille")
        
        if win: vic_j += 1
        else: 
            vic_v += 1
            print("Aïe ! Coup de canne !")
            if player.take_damage(35): return False

    if vic_j >= 2:
        print("\n🎉 VICTOIRE !")
        if not deja_gagne:
            recompense = Item(nom_objet, "la clé de la réussite", 0.1)
            # VÉRIFIER si le joueur peut prendre l'objet
            if player.can_take_item(recompense):
                player.inventory.append(recompense)
                print(f"\n🎁 Vous recevez : {nom_objet} !")
            else:
                print(f"\n💔 Le Vieux vous tend {nom_objet}, mais vous n'avez plus de place !")
                print("   L'objet tombe au sol.")
                # Ajouter l'objet à la salle actuelle
                player.current_room.add_item(recompense)
        else:
            print("« Je n'ai plus rien pour toi, garnement ! »")
        return True
    
    print("\n💀 DÉFAITE.")
    return False