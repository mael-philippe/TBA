import random

# Événements déclenchés en parlant aux personnages
def porte_entree_event(player):
    print("\n🎵 La musique assourdissante de la fête résonne.")
    print("Le garde vous arrête: 'Hé, tu as l'air perdu, première année?'")
    print("Choix: 1) Faire le fier 2) Jouer l'innocent")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n💥 Mauvaise idée! Le garde vous pousse violemment.")
        player.take_damage(20)
    else:
        print("\n✓ 'Désolé, je cherche les toilettes...' Le garde ricane et vous laisse passer.")
    return True

def bar_event(player):
    print("\n🍻 Le membre ivre vous défie de finir un 'Mystik on the Beach'.")
    print("Choix: 1) Accepter le défi 2) Refuser poliment")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n🥴 Vous réussissez le shot mais votre estomac prend un choc...")
        player.take_damage(15)
        print("✓ Les membres vous respectent maintenant!")
    else:
        print("\n👎 'T'es pas un vrai frère!' - Vous perdez du respect mais sauvez votre santé.")
    return True

def salle_jeux_event(player):
    print("\n🎮 Le champion vous défie à un jeu vidéo.")
    print("Choix: 1) Accepter le duel 2) Observer seulement")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        if random.random() > 0.5:
            print("\n🎉 Vous gagnez! Les membres sont impressionnés.")
            player.add_item("Clé USB mysterieuse")
        else:
            print("\n💥 Vous perdez honteusement. Le champion vous humilie.")
            player.take_damage(10)
    else:
        print("\n👀 Vous apprenez leurs techniques secrètes.")
    return True

def salle_sport_event(player):
    print("\n💪 Le capitaine vous défie à un combat de boxe.")
    print("Choix: 1) Se battre 2) Inventer une excuse")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n🥊 Le combat est intense! Vous tenez bon mais prenez des coups.")
        player.take_damage(35)
        print("✓ Vous gagnez le respect du capitaine!")
    else:
        print("\n🏃 'Désolé, j'ai cours à rattraper!' - Vous évitez le combat.")
    return True

def cave_event(player):
    print("\n🍷 Le vieux membre vous raconte des histoires du passé.")
    print("Il vous offre une bouteille de vin rare.")
    player.add_item("Bouteille de vin rare")
    print("✓ Objet de valeur obtenu!")
    return True

# Événements déclenchés par la commande "look"
def cuisine_look_event(player):
    print("\n🍕 Vous regardez autour de la cuisine...")
    print("Vous trouvez une pizza à moitié mangée et des RedBulls.")
    print("Choix: 1) Manger la pizza 2) Prendre une RedBull")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n🤢 La pizza avait 3 jours... Vous tombez malade!")
        player.take_damage(25)
    else:
        print("\n⚡ La RedBull vous redonne de l'énergie!")
        player.heal(20)
    return True

def dortoir_look_event(player):
    print("\n🛏️ Vous regardez sous les lits...")
    print("Sous un lit, vous trouvez une trousse de secours.")
    player.heal(30)
    print("✓ Santé restaurée! Les membres dorment profondément.")
    return True

def bureau_president_look_event(player):
    print("\n🚨 Vous regardez sur le bureau...")
    print("Des documents compromettants sont éparpillés!")
    print("Choix: 1) Prendre les documents 2) Prendre une photo discrètement")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n📁 Vous prenez les documents! C'est la preuve ultime!")
        player.add_item("Documents compromettants")
    else:
        print("\n📸 Photo prise! Preuve obtenue mais moins convaincante.")
        player.add_item("Photo compromettante")
    return True

def toit_look_event(player):
    print("\n🌃 Vous explorez le toit...")
    print("Vous trouvez le livre des secrets des Mystik!")
    player.add_item("Livre des secrets")
    
    # Vérifier si le joueur a collecté suffisamment de preuves
    preuves = [item for item in player.inventory if "compromettant" in item.lower() or "secret" in item.lower() or "clé" in item.lower()]
    if len(preuves) >= 2:
        print("\n🎉 FÉLICITATIONS! Vous avez assez de preuves pour faire tomber Mystik!")
        print("Mission accomplie! Les Banditos vous remercieront éternellement!")
    else:
        print("\n⚠️ Vous avez le livre, mais il vous faut plus de preuves. Continuez à chercher!")
    return True