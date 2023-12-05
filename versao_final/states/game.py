import pygame as pg
import constants as c
import json

from button import Button
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import Turret, FarmingTurret
from states.state import State
from loader import Loader


class GameState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        #controlador de level, world e game referentes
        self.ControladorLevel = game.ControladorLevel
        self.loader = Loader(screen, clock, game)
        self.world = game.world
        self.variaveis()

    def create_turret(self, mouse_pos, placing_attack_turret, placing_farming_turret):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        # checar se a tile eh valida para torre
        if self.world.tile_map[mouse_tile_num] == 38:
            # checar se ja nao tem uma torre la
            space_is_free = True
            for turret in self.game.turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    print(mouse_tile_x, mouse_tile_y,
                          turret.tile_x, turret.tile_y)
                    space_is_free = False
                    break

            if space_is_free:
                    if placing_attack_turret and self.ControladorLevel.player.tentar_comprar(c.BUY_COST["attack"]):
                        new_attack_turret = Turret([self.loader.turret_sheet1, self.loader.turret_sheet2, self.loader.turret_sheet3] , mouse_tile_x, mouse_tile_y, 90, 600, 6)
                        self.game.turret_group.add(new_attack_turret)
                        placing_attack_turret = False

                    elif placing_farming_turret and self.ControladorLevel.player.tentar_comprar(c.BUY_COST["farm"]):
                        new_farming_turret = FarmingTurret(self.loader.farm_turret_sheet, mouse_tile_x, mouse_tile_y)
                        self.game.turret_group.add(new_farming_turret)
                        placing_farming_turret = False

    def upgrade_turret(self, turret):
        turret.upgrade()

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
                        self.create_turret(mouse_pos, self.placing_attack_turret, self.placing_farming_turret)
                    else:
                        self.selected_turret = self.game.select_turret(
                            mouse_pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.handle_escape()
                if event.key == pg.K_SPACE:
                    if not self.tips_flag:
                        self.tips_flag = True
                    else:
                        self.tips_flag = False

    def update(self):
        if not self.game_over:
            if self.ControladorLevel.player.health <= 0:
                self.game_over = True
                self.game.set_game_over_state()

            if self.ControladorLevel.level > 10:
                self.game_over = True
                self.game.set_win_state()

        self.game.enemy_group.update(self.ControladorLevel)
        self.game.turret_group.update(self.game.enemy_group, self.ControladorLevel)

        if self.selected_turret:
            self.selected_turret.selected = True

        self.screen.fill("grey100")
        self.world.draw(self.screen)
        self.game.enemy_group.draw(self.screen)
        self.game.turret_group.draw(self.screen)

        self.screen.blit(self.loader.hud_image, (c.SCREEN_WIDTH, 0))
        self.screen.blit(self.loader.health_bar_image, (c.SCREEN_WIDTH + 40, 80))
        self.screen.blit(self.loader.coin_bar_image, (c.SCREEN_WIDTH + 40, 130))
        self.screen.blit(self.loader.help_image, (c.SCREEN_WIDTH+30, 500))

        for turret in self.game.turret_group:
            turret.draw(self.screen)
        self.printar_texto_na_tela(
            (str(self.ControladorLevel.player.health)), self.fonte1, "grey100", c.SCREEN_WIDTH+125, 90)
        self.printar_texto_na_tela(
            (str(int(self.ControladorLevel.player.money))), self.fonte1, "grey100", c.SCREEN_WIDTH+125, 140)
        self.printar_texto_na_tela(
            (f"Level {str(self.ControladorLevel.level)}"), self.fonte1, "grey100", c.SCREEN_WIDTH+45, 40)

        if not self.game_over:
            if not self.ControladorLevel.level_comecou:
                if self.loader.begin_round_button.draw(self.screen):
                    self.click_sound.play()
                    self.ControladorLevel.level_comecou = True
            else:
                self.ControladorLevel.velocidade_jogo = 1
                if self.loader.acelerar_button.draw(self.screen):
                    self.ControladorLevel.velocidade_jogo = 3
                if (pg.time.get_ticks() - self.ultimo_spawn_inimigo >= c.SPAWN_COOLDOWN / self.ControladorLevel.velocidade_jogo and self.ControladorLevel.inimigos_spawnados < len(self.ControladorLevel.lista_inimigos)):
                    self.game.enemy_group.add(self.game.decidir_tipo_inimigo())
                    self.ultimo_spawn_inimigo = pg.time.get_ticks()

        if self.ControladorLevel.checar_round_acabou():
            for turret in self.game.turret_group:
                turret.ativar(self.ControladorLevel.player)

        if self.selected_turret and self.selected_turret.level < self.selected_turret.max_level:
            print(c.UPGRADE_COST[self.selected_turret.level])
            if self.loader.upgrade_button.draw(self.screen) and self.ControladorLevel.player.tentar_upgradear(c.UPGRADE_COST[self.selected_turret.level]):
                    self.upgrade_turret(self.selected_turret)
                    self.selected_turret = None

        if self.loader.turret_button.draw(self.screen):
            self.click_sound.play()
            self.choosing_turret = True            
        
        if self.choosing_turret == True:
            if self.loader.cancel_button.draw(self.screen):
                self.click_sound.play()
                self.placing_turrets = False
                self.choosing_turret = False

            if self.loader.attack_turret_button.draw(self.screen):
                self.placing_turrets = True
                self.placing_farming_turret = False
                self.placing_attack_turret = True
                self.cursor_turret = pg.image.load(
                            'assets/imagens/torres/cursor_turret.png').convert_alpha()
            elif self.loader.farm_turret_button.draw(self.screen):
                self.placing_turrets = True
                self.placing_attack_turret = False
                self.placing_farming_turret = True
                self.cursor_turret = pg.image.load(
                            'assets/imagens/torres/cursor_farming_turret.png').convert_alpha()

        if self.placing_turrets == True:
            cursor_rect = self.cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= c.SCREEN_WIDTH:
                self.screen.blit(self.cursor_turret, cursor_rect)

        if self.tips_flag == True:
            self.screen.blit(pg.image.load(
                            'assets/imagens/tips.png').convert_alpha(), (200, 130))

    def printar_texto_na_tela(self, text, fonte, text_col, x, y):
        img = fonte.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def variaveis(self):
        self.placing_turrets = False
        self.placing_attack_turret = False
        self.placing_farming_turret = False
        self.selected_turret = None
        self.game_over = False
        self.choosing_turret = False
        self.tips_flag = False

        self.ultimo_spawn_inimigo = pg.time.get_ticks() 
        self.fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.cursor_turret = None