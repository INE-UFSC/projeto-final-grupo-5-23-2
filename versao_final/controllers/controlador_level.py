import pygame as pg
from levels.level1 import spawn_por_round as spr
import random
import constants as c
from pygame import mixer

from player import Player
from world import World

class ControladorLevel():
    def __init__(self):

        self.level = 1

        self.lista_inimigos = []
        self.inimigos_spawnados = 0
        self.inimigos_killados = 0
        self.inimigos_missados = 0
        self.velocidade_jogo = 1

        self.player = Player()
        
        self.level_comecou = False

        self.process_inimigos()

    def process_inimigos(self):
        inimigos = spr.SPAWN_POR_ROUND[self.level-1]
        for tipo_inimigo in inimigos:
            # retorna o numero de enemies
            for inimigo in range(inimigos[tipo_inimigo]):
                self.lista_inimigos.append(tipo_inimigo)
        # deixar aleatorio o spawn
        random.shuffle(self.lista_inimigos)

    def inimigo_chegou(self, inimigo):
        self.player.health -= inimigo.forca
        self.inimigos_missados += 1
    
    def inimigo_morreu(self, inimigo):
        self.player.money += inimigo.reward
        self.iniigos_killados += 1

    def checar_round_acabou(self):
        if (self.inimigos_killados + self.inimigos_missados) == len(self.lista_inimigos):
            self.reset_round()
            self.level_comecou = False
            level_complete = mixer.Sound('assets/effects/levelcomplete.wav')
            level_complete.play()
            return True

    def reset_round(self):
        self.player.recompensa_level(self.level)

        self.inimigos_killados = 0
        self.inimigos_missados = 0
        self.inimigos_spawnados = 0
        self.lista_inimigos = []

        self.level += 1
        self.process_inimigos()
