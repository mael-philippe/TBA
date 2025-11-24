class Player():
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.health = 100
        self.max_health = 100
        self.inventory = []
    
    def move(self, direction):
        next_room = self.current_room.exits[direction]
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        self.current_room = next_room
        print(self.current_room.get_long_description())
        
        # Déclencher les événements de la salle
        if hasattr(self.current_room, 'event'):
            self.current_room.event(self)
        return True
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print(f"\n💀 {self.name} est K.O.! Mission échouée...\n")
            return True  # Le joueur est mort
        return False
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        print(f"\n❤️  Santé restaurée de {amount} points! Santé actuelle: {self.health}/{self.max_health}\n")
    
    def add_item(self, item):
        self.inventory.append(item)
        print(f"\n🎒 {item} ajouté à l'inventaire!\n")