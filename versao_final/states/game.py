import pygame as pg
import constants as c
import json

from button import Button
from world import World
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3
from states.state import State


class GameState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        # Inicialize suas variáveis e grupos aqui, conforme necessário
        self.placing_turrets = False
        self.selected_turret = None
        self.level_comecou = False
        self.game_over = False
        buy_turret_image = pg.image.load('assets/imagens/botoes/buy_turret.png').convert_alpha()
        cancel_image = pg.image.load('assets/imagens/botoes/cancel.png').convert_alpha()
        upgrade_turret_image = pg.image.load('assets/imagens/botoes/upgrade_turret.png').convert_alpha()
        begin_round_image = pg.image.load('assets/imagens/botoes/begin.png').convert_alpha()
        acelerar_image = pg.image.load('assets/imagens/botoes/fast_forward.png').convert_alpha()
        self.turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
        self.upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
        self.begin_round_button = Button(c.SCREEN_WIDTH + 60, 300, begin_round_image, True)
        self.acelerar_button = Button(c.SCREEN_WIDTH + 50, 300, acelerar_image, False)
        self.ultimo_spawn_inimigo = pg.time.get_ticks()
        self.world = game.world  # Adicione esta linha
        self.fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.cursor_turret = pg.image.load('assets/imagens/torres/cursor_turret.png').convert_alpha()
        self.turret_sheet1 = pg.image.load('assets/imagens/torres/turret_1.png').convert_alpha()
        self.turret_sheet2 = pg.image.load('assets/imagens/torres/turret_2.png').convert_alpha()
        self.turret_sheet3 = pg.image.load('assets/imagens/torres/turret_3.png').convert_alpha()

    def create_turret(self, mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        #checar se a tile eh valida para torre
        if self.world.tile_map[mouse_tile_num] == 38:
            #checar se ja nao tem uma torre la
            space_is_free = True
            for turret in self.game.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    print(mouse_tile_x, mouse_tile_y, turret.tile_x, turret.tile_y)
                    space_is_free = False
                    break
                #ver se tem dinheiro rs
            if space_is_free:
                if self.world.money >= c.BUY_COST:
                    new_turret = TurretLevel1(self.turret_sheet1, mouse_tile_x, mouse_tile_y)
                    self.game.turret_group.add(new_turret)
                    self.world.money -= c.BUY_COST

    def upgrade_turret(self, turret, turret_sheet2, turret_sheet3):
        #teria como concatenar o numero +1 mas deu preguica
        if turret.nivel == 1:
            newturret = TurretLevel2(turret_sheet2, turret.tile_x, turret.tile_y)
            return newturret

        else:
            newturret = TurretLevel3(turret_sheet3, turret.tile_x, turret.tile_y)
            return newturret

    def handle_escape(self):
        self.game.set_pause_state()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    self.selected_turret = None
                    self.game.clear_selection()
                    if self.placing_turrets:
                        self.create_turret(mouse_pos)
                    else:
                        self.selected_turret = self.game.select_turret(mouse_pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.handle_escape()

    def update(self):
        
        if not self.game_over:
            if self.world.health <= 0:
                self.game_over = True
                self.game.set_game_over_state()

            if self.world.level > 2:
                self.game_over = True
                self.game.set_win_state()

        self.game.enemy_group.update(self.world)
        self.game.turret_group.update(self.game.enemy_group, self.world)

        if self.selected_turret:
            self.selected_turret.selected = True

        self.screen.fill("grey100")
        self.world.draw(self.screen)
        self.game.enemy_group.draw(self.screen)
        self.game.turret_group.draw(self.screen)
        for turret in self.game.turret_group:
            turret.draw(self.screen)
        self.printar_texto_na_tela((str(self.world.health)), self.fonte1, "grey100", 0, 0) 
        self.printar_texto_na_tela((str(int(self.world.money))), self.fonte1, "grey100", 0, 30)
        self.printar_texto_na_tela((f"level {str(self.world.level)}"), self.fonte1, "grey100", 0, 60)

        if not self.game_over:
            if not self.level_comecou:
                if self.begin_round_button.draw(self.screen):
                    self.click_sound.play()
                    self.level_comecou = True
            else:
                self.world.velocidade_jogo = 1
                if self.acelerar_button.draw(self.screen):
                    self.world.velocidade_jogo = 3
                if (pg.time.get_ticks() - self.ultimo_spawn_inimigo >= c.SPAWN_COOLDOWN / self.world.velocidade_jogo and self.world.inimigos_spawnados < len(self.world.lista_inimigos)):
                    self.game.enemy_group.add(self.game.decidir_tipo_inimigo())
                    self.ultimo_spawn_inimigo = pg.time.get_ticks()
            
        if self.world.checar_round_acabou():
            self.level_comecou = False
        
        if self.selected_turret and self.selected_turret.nivel < 3:
            if self.upgrade_button.draw(self.screen):
                if self.world.money >= c.UPGRADE_COST:
                    self.world.money -= c.UPGRADE_COST
                    self.selected_turret.kill()
                    self.game.turret_group.add(self.upgrade_turret(self.selected_turret, self.turret_sheet2, self.turret_sheet3))
                    selected_turret = None

        if self.turret_button.draw(self.screen):
            self.click_sound.play()
            self.placing_turrets = True
        if self.placing_turrets == True:
            cursor_rect = self.cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDTH:
                self.screen.blit(self.cursor_turret, cursor_rect)
            if self.cancel_button.draw(self.screen):
                self.click_sound.play()
                self.placing_turrets = False

    def printar_texto_na_tela(self, text, fonte, text_col, x, y):
        img = fonte.render(text, True, text_col)
        self.screen.blit(img, (x, y))
    