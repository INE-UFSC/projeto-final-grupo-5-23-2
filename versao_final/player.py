import constants as c

class Player():
    def __init__(self):
        self.money = c.MONEY
        self.health = c.HEALTH
        self.nome = None
    
    def recompensa_level(self, level):
        self.money += c.RECOMPENSA_LEVEL_PADRAO * (level/2)
    
    def tentar_upgradear(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True
    
    def tentar_comprar(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True

