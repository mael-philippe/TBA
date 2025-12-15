import random
from item import Item

# ============================================
# ÉVÉNEMENTS POUR LA COMMANDE "TALK" (personnages)
# ============================================

def porte_entree_event(player):
    """Événement déclenché par 'talk Garde'"""
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
    """Événement déclenché par 'talk Ivre'"""
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
    """Événement déclenché par 'talk Champion'"""
    print("\n🎮 Le champion vous défie à un jeu vidéo.")
    print("Choix: 1) Accepter le duel 2) Observer seulement")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        if random.random() > 0.5:
            print("\n🎉 Vous gagnez! Les membres sont impressionnés.")
            # Ajouter la clé USB à la salle
            cle_usb = Item("Clé USB", "clé USB avec des données sensibles des Mystik", 0.1)
            player.current_room.add_item(cle_usb)
            print(f"✓ {cle_usb.name} a été ajoutée à la salle!")
        else:
            print("\n💥 Vous perdez honteusement. Le champion vous humilie.")
            player.take_damage(10)
    else:
        print("\n👀 Vous apprenez leurs techniques secrètes.")
    return True

def salle_sport_event(player):
    """Événement déclenché par 'talk Capitaine'"""
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
    """Événement déclenché par 'talk Vieux'"""
    print("\n🍷 Le vieux membre vous raconte des histoires du passé.")
    print("Il vous offre une bouteille de vin rare.")
    
    # Ajouter la bouteille de vin à la salle
    bouteille_vin = Item("Bouteille de vin", "bouteille de vin rare des Mystik", 1.5)
    player.current_room.add_item(bouteille_vin)
    print(f"✓ {bouteille_vin.name} a été ajoutée à la salle!")
    
    # Le vieux membre donne aussi un indice
    print("\n🤫 Le vieux membre vous murmure: 'Cherche sur le toit... les secrets y sont cachés.'")
    return True

# ============================================
# ÉVÉNEMENTS POUR LA COMMANDE "LOOK" (exploration)
# ============================================
# NOTE: Ces événements ne sont PAS utilisés dans la version actuelle
# Ils sont gardés pour référence future

def cuisine_look_event(player):
    """Événement spécial pour 'look' dans la cuisine"""
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
    """Événement spécial pour 'look' dans le dortoir"""
    print("\n🛏️ Vous regardez sous les lits...")
    print("Sous un lit, vous trouvez une trousse de secours.")
    player.heal(30)
    print("✓ Santé restaurée! Les membres dorment profondément.")
    return True

def bureau_president_look_event(player):
    """Événement spécial pour 'look' dans le bureau"""
    print("\n🚨 Vous regardez sur le bureau...")
    print("Des documents compromettants sont éparpillés!")
    print("Choix: 1) Prendre les documents 2) Prendre une photo discrètement")
    
    choix = input("Votre choix (1/2): ")
    if choix == "1":
        print("\n📁 Vous prenez les documents! C'est la preuve ultime!")
        # Ajouter les documents à la salle
        documents = Item("Documents", "documents compromettants sur les Mystik", 0.5)
        player.current_room.add_item(documents)
        print(f"✓ {documents.name} ont été ajoutés à la salle!")
    else:
        print("\n📸 Photo prise! Preuve obtenue mais moins convaincante.")
        # Ajouter une photo à la salle
        photo = Item("Photo", "photo compromettante du président", 0.2)
        player.current_room.add_item(photo)
        print(f"✓ Une {photo.name} a été ajoutée à la salle!")
    return True

def toit_look_event(player):
    """Événement spécial pour 'look' sur le toit"""
    print("\n🌃 Vous explorez le toit...")
    print("Vous trouvez le livre des secrets des Mystik!")
    
    # Ajouter le livre à la salle
    livre_secrets = Item("Livre", "livre des secrets des Mystik", 1.0)
    player.current_room.add_item(livre_secrets)
    print(f"✓ Le {livre_secrets.name} a été ajouté à la salle!")
    
    print("\n⚠️ Prenez ce livre comme preuve! Vous aurez besoin d'au moins 2 preuves.")
    return True