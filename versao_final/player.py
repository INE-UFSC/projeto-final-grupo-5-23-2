import constants as c

class Player():
    def __init__(self):
        self.money = c.MONEY
        self.health = c.HEALTH
        self.nome = None
    
    def recompensa_level(self, level):
        self.money += c.RECOMPENSA_LEVEL_PADRAO * (level/2)
    
    def tentar_upgradear(self):
        if self.money >= c.UPGRADE_COST:
            self.money -= c.UPGRADE_COST
            return True
        return False
    
    def tentar_comprar(self):
        if self.money >= c.BUY_COST:
            self.money -= c.BUY_COST
            return True
        return False
    #serão duas funções diferentes mesmo, pq no futuro o upgrade cost será multiplicado pelo nivel da torre 
    #além disso, a mensagem que aparece quando vc tenta comprar algo ou upgradear algo sem dinheiro é diferente
    #por enquanto tá assim msm
