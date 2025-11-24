import random

# Événements pour chaque salle
def porte_entree_event(player):
    if not hasattr(porte_entree_event, 'triggered'):
        print("\n🎵 La musique assourdissante de la fête résonne. Des membres de Mystik scrutent les nouveaux venus.")
        print("Un garde vous arrête: 'Hé, tu as l'air perdu, première année?'")
        print("Choix: 1) Faire le fier 2) Jouer l'innocent")
        
        choix = input("Votre choix (1/2): ")
        if choix == "1":
            print("\n💥 Mauvaise idée! Le garde vous pousse violemment.")
            player.take_damage(20)
        else:
            print("\n✓ 'Désolé, je cherche les toilettes...' Le garde ricane et vous laissez passer.")
        porte_entree_event.triggered = True

def bar_event(player):
    if not hasattr(bar_event, 'triggered'):
        print("\n🍻 Le bar est bondé. Un membre ivre vous défie de finir un 'Mystik on the Beach'.")
        print("Choix: 1) Accepter le défi 2) Refuser poliment")
        
        choix = input("Votre choix (1/2): ")
        if choix == "1":
            print("\n🥴 Vous réussissez le shot mais votre estomac prend un choc...")
            player.take_damage(15)
            print("✓ Les membres vous respectent maintenant!")
        else:
            print("\n👎 'T'es pas un vrai frère!' - Vous perdez du respect mais sauvez votre santé.")
        bar_event.triggered = True

def cuisine_event(player):
    if not hasattr(cuisine_event, 'triggered'):
        print("\n🍕 La cuisine est vide. Vous trouvez une pizza à moitié mangée et des RedBulls.")
        print("Choix: 1) Manger la pizza 2) Prendre une RedBull")
        
        choix = input("Votre choix (1/2): ")
        if choix == "1":
            print("\n🤢 La pizza avait 3 jours... Vous tombez malade!")
            player.take_damage(25)
        else:
            print("\n⚡ La RedBull vous redonne de l'énergie!")
            player.heal(20)
        cuisine_event.triggered = True

def salle_jeux_event(player):
    if not hasattr(salle_jeux_event, 'triggered'):
        print("\n🎮 Des membres jouent à un jeu vidéo. Le champion vous défie.")
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
        salle_jeux_event.triggered = True

def bureau_president_event(player):
    if not hasattr(bureau_president_event, 'triggered'):
        print("\n🚨 Vous entrez dans le bureau interdit du président! Des documents compromettants sont sur le bureau.")
        print("Choix: 1) Prendre les documents 2) Prendre une photo discrètement")
        
        choix = input("Votre choix (1/2): ")
        if choix == "1":
            print("\n📁 Vous prenez les documents! C'est la preuve ultime!")
            player.add_item("Documents compromettants")
        else:
            print("\n📸 Photo prise! Preuve obtenue mais moins convaincante.")
            player.add_item("Photo compromettante")
        bureau_president_event.triggered = True

def dortoir_event(player):
    if not hasattr(dortoir_event, 'triggered'):
        print("\n🛏️ Le dortoir est silencieux. Sous un lit, vous trouvez une trousse de secours.")
        player.heal(30)
        print("✓ Santé restaurée! Les membres dorment profondément.")
        dortoir_event.triggered = True

def salle_sport_event(player):
    if not hasattr(salle_sport_event, 'triggered'):
        print("\n💪 Le capitaine de l'équipe vous défie à un combat de boxe.")
        print("Choix: 1) Se battre 2) Inventer une excuse")
        
        choix = input("Votre choix (1/2): ")
        if choix == "1":
            print("\n🥊 Le combat est intense! Vous tenez bon mais prenez des coups.")
            player.take_damage(35)
            print("✓ Vous gagnez le respect du capitaine!")
        else:
            print("\n🏃 'Désolé, j'ai cours à rattraper!' - Vous évitez le combat mais semblez lâche.")
        salle_sport_event.triggered = True

def cave_event(player):
    if not hasattr(cave_event, 'triggered'):
        print("\n🍷 La cave sent le moisi. Un vieux membre vous raconte des histoires du passé.")
        print("Il vous offre une bouteille de vin rare.")
        player.add_item("Bouteille de vin rare")
        print("✓ Objet de valeur obtenu!")
        cave_event.triggered = True

def toit_event(player):
    if not hasattr(toit_event, 'triggered'):
        print("\n🌃 Sur le toit, vous trouvez le livre des secrets des Mystik")
        print("C'est la preuve finale dont vous avez besoin!")
        player.add_item("Livre des secrets")
        
        # Vérifier si le joueur a collecté suffisamment de preuves
        preuves = [item for item in player.inventory if "compromettant" in item.lower() or "secret" in item.lower() or "clé" in item.lower()]
        if len(preuves) >= 2:
            print("\n🎉 FÉLICITATIONS! Vous avez assez de preuves pour faire tomber Mystik!")
            print("Mission accomplie! Les Banditos vous remercieront éternellement!")
        else:
            print("\n⚠️ Vous avez le livre, mais il vous faut plus de preuves. Continuez à chercher!")
        toit_event.triggered = True
    