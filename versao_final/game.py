import pygame as pg
import constants as c
import json

from button import Button
from world import World
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3

from states.game_over import GameOverState
from states.game import GameState
from states.pause import PauseState
from states.init import InitState
from states.win import WinState


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.PANEL_SIZE, c.SCREEN_HEIGHT))
        pg.display.set_caption("Tower Defense")
        self.icon_image = pg.image.load('assets/imagens/componentes/icon1.jpeg').convert_alpha()
        map_image = pg.image.load('levels/default.png').convert_alpha()
        pg.display.set_icon(self.icon_image)
        self.font = pg.font.SysFont("Arial", 30)
        self.running = True
        self.state = None
        with open('levels/default.tmj') as file:
            world_data = json.load(file)
        self.world = World(world_data, map_image)
        self.world.process_data()
        self.world.process_inimigos()
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()

    def decidir_tipo_inimigo(self):
        enemy_image1 = pg.image.load('assets/imagens/inimigos/enemy_1.png').convert_alpha()
        enemy_image2 = pg.image.load('assets/imagens/inimigos/enemy_2.png').convert_alpha()
        enemy_image3 = pg.image.load('assets/imagens/inimigos/enemy_3.png').convert_alpha()

        tipo = self.world.lista_inimigos[self.world.inimigos_spawnados]
        self.world.inimigos_spawnados += 1
        if tipo == "fraco":
            return InimigoFraco(self.world.waypoints, enemy_image1)
        elif tipo == "normal":
            return InimigoNormal(self.world.waypoints, enemy_image2)
        else:
            return InimigoForte(self.world.waypoints, enemy_image3)
        #por enquanto o inimigo elite ta gerando o inimigo forte mesmo

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False

    def select_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        for turret in self.turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret  

    def change_state(self, new_state):
        self.state = new_state(self.screen, self.clock, self)

    def set_init_state(self):
        self.change_state(InitState)

    def set_game_over_state(self):
        self.change_state(GameOverState)

    def set_game_state(self):
        self.change_state(GameState)
    
    def set_pause_state(self):
        self.change_state(PauseState)

    def set_win_state(self):
        self.change_state(WinState)

    def run(self):
        while self.running:
            self.state.handle_events()
            self.state.update()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()