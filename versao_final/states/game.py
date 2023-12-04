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
        # Inicialize suas variáveis e grupos aqui, conforme necessário
        self.loader = Loader(screen, clock, game)
        self.placing_turrets = False
        self.placing_attack_turret = False
        self.placing_farming_turret = False
        self.selected_turret = None
        self.level_comecou = False
        self.game_over = False
        self.choosing_turret = False

        self.loader.hud_image = pg.image.load(
            'assets/imagens/hud.jpg').convert_alpha()
        self.loader.health_bar_image = pg.image.load(
            'assets/imagens/componentes/health_bar.png').convert_alpha()
        self.loader.coin_bar_image = pg.image.load(
            'assets/imagens/componentes/coin_bar.png').convert_alpha()
        self.loader.help_image = pg.image.load(
            'assets/imagens/help.png').convert_alpha()


        self.turret_button = Button(
            c.SCREEN_WIDTH + 40, 350, pg.image.load(
            'assets/imagens/botoes/buy_turret.png').convert_alpha(), True)
        
        self.farm_turret_button = Button(
            c.SCREEN_WIDTH +40, 450, pg.image.load(
                'assets/imagens/botoes/farm_turret.png').convert_alpha(), True)
        self.attack_turret_button = Button(
            c.SCREEN_WIDTH +40, 400, pg.image.load(
                'assets/imagens/botoes/attack_turret.png').convert_alpha(), True)

        self.cancel_button = Button(
            c.SCREEN_WIDTH + 40, 350, pg.image.load(
            'assets/imagens/botoes/cancel.png').convert_alpha(), True)
        self.upgrade_button = Button(
            c.SCREEN_WIDTH + 40, 400, pg.image.load(
            'assets/imagens/botoes/upgrade_turret.png').convert_alpha(), True)
        self.begin_round_button = Button(
            c.SCREEN_WIDTH + 40, 300, pg.image.load(
            'assets/imagens/botoes/begin.png').convert_alpha(), True)
        self.acelerar_button = Button(
            c.SCREEN_WIDTH + 40, 300, pg.image.load(
            'assets/imagens/botoes/fast_forward.png').convert_alpha(), False)

        self.ultimo_spawn_inimigo = pg.time.get_ticks()
        self.world = game.world  # Adicione esta linha
        self.ControladorLevel = game.ControladorLevel
        self.fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.cursor_turret = None
        #self.cursor_turret = pg.image.load(
            #'assets/imagens/torres/cursor_turret.png').convert_alpha()
        self.turret_sheet1 = pg.image.load(
            'assets/imagens/torres/turret_1.png').convert_alpha()
        self.turret_sheet2 = pg.image.load(
            'assets/imagens/torres/turret_2.png').convert_alpha()
        self.turret_sheet3 = pg.image.load(
            'assets/imagens/torres/turret_3.png').convert_alpha()
        self.farm_turret_sheet = pg.image.load(
            'assets/imagens/torres/farming_turret.png').convert_alpha()
        self.farm_turret_sheet = pg.transform.scale_by(self.farm_turret_sheet, 1/6)
        
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
                # ver se tem dinheiro rs
            if space_is_free:
                if self.ControladorLevel.player.tentar_comprar():
                    if placing_attack_turret == True:
                        new_attack_turret = Turret([self.turret_sheet1, self.turret_sheet2, self.turret_sheet3] , mouse_tile_x, mouse_tile_y, 90, 600, 6)
                        self.game.turret_group.add(new_attack_turret)
                        placing_attack_turret = False

                    if placing_farming_turret == True:
                        new_farming_turret = FarmingTurret(self.farm_turret_sheet, mouse_tile_x, mouse_tile_y)
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

    def update(self):

        if not self.game_over:
            if self.ControladorLevel.player.health <= 0:
                self.game_over = True
                self.game.set_game_over_state()

            if self.ControladorLevel.level > 2:
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
            if not self.level_comecou:
                if self.begin_round_button.draw(self.screen):
                    self.click_sound.play()
                    self.level_comecou = True
            else:
                self.ControladorLevel.velocidade_jogo = 1
                if self.acelerar_button.draw(self.screen):
                    self.ControladorLevel.velocidade_jogo = 3
                if (pg.time.get_ticks() - self.ultimo_spawn_inimigo >= c.SPAWN_COOLDOWN / self.ControladorLevel.velocidade_jogo and self.ControladorLevel.inimigos_spawnados < len(self.ControladorLevel.lista_inimigos)):
                    self.game.enemy_group.add(self.game.decidir_tipo_inimigo())
                    self.ultimo_spawn_inimigo = pg.time.get_ticks()

        if self.ControladorLevel.checar_round_acabou():
            self.level_comecou = False
            for turret in self.game.turret_group:
                turret.ativar(self.ControladorLevel.player)

        if self.selected_turret and self.selected_turret.level < self.selected_turret.max_level:
            if self.upgrade_button.draw(self.screen):
                if self.ControladorLevel.player.tentar_upgradear():
                    self.upgrade_turret(self.selected_turret)
                    self.selected_turret = None

        if self.turret_button.draw(self.screen):
            self.click_sound.play()
            self.choosing_turret = True            
        
        if self.choosing_turret == True:
            if self.cancel_button.draw(self.screen):
                self.click_sound.play()
                self.placing_turrets = False
                self.choosing_turret = False

            if self.attack_turret_button.draw(self.screen):
                self.placing_turrets = True
                self.placing_farming_turret = False
                self.placing_attack_turret = True
                self.cursor_turret = pg.image.load(
                            'assets/imagens/torres/cursor_turret.png').convert_alpha()
            elif self.farm_turret_button.draw(self.screen):
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


    def printar_texto_na_tela(self, text, fonte, text_col, x, y):
        img = fonte.render(text, True, text_col)
        self.screen.blit(img, (x, y))
