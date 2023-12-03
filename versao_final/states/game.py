import pygame as pg
import constants as c
import json

from button import Button
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

        self.hud_image = pg.image.load(
            'assets/imagens/hud.jpg').convert_alpha()
        self.health_bar_image = pg.image.load(
            'assets/imagens/componentes/health_bar.png').convert_alpha()
        self.coin_bar_image = pg.image.load(
            'assets/imagens/componentes/coin_bar.png').convert_alpha()
        self.help_image = pg.image.load(
            'assets/imagens/help.png').convert_alpha()

        buy_turret_image = pg.image.load(
            'assets/imagens/botoes/buy_turret.png').convert_alpha()
        cancel_image = pg.image.load(
            'assets/imagens/botoes/cancel.png').convert_alpha()
        upgrade_turret_image = pg.image.load(
            'assets/imagens/botoes/upgrade_turret.png').convert_alpha()
        begin_round_image = pg.image.load(
            'assets/imagens/botoes/begin.png').convert_alpha()
        acelerar_image = pg.image.load(
            'assets/imagens/botoes/fast_forward.png').convert_alpha()

        self.turret_button = Button(
            c.SCREEN_WIDTH + 40, 350, buy_turret_image, True)
        self.cancel_button = Button(
            c.SCREEN_WIDTH + 40, 350, cancel_image, True)
        self.upgrade_button = Button(
            c.SCREEN_WIDTH + 40, 400, upgrade_turret_image, True)
        self.begin_round_button = Button(
            c.SCREEN_WIDTH + 40, 300, begin_round_image, True)
        self.acelerar_button = Button(
            c.SCREEN_WIDTH + 40, 300, acelerar_image, False)

        self.ultimo_spawn_inimigo = pg.time.get_ticks()
        self.world = game.world  # Adicione esta linha
        self.ControladorLevel = game.ControladorLevel
        self.fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.cursor_turret = pg.image.load(
            'assets/imagens/torres/cursor_turret.png').convert_alpha()
        self.turret_sheet1 = pg.image.load(
            'assets/imagens/torres/turret_1.png').convert_alpha()
        self.turret_sheet2 = pg.image.load(
            'assets/imagens/torres/turret_2.png').convert_alpha()
        self.turret_sheet3 = pg.image.load(
            'assets/imagens/torres/turret_3.png').convert_alpha()

    def create_turret(self, mouse_pos):
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
                    new_turret = TurretLevel1(
                        self.turret_sheet1, mouse_tile_x, mouse_tile_y)
                    self.game.turret_group.add(new_turret)

    def upgrade_turret(self, turret, turret_sheet2, turret_sheet3):
        # teria como concatenar o numero +1 mas deu preguica
        if turret.nivel == 1:
            newturret = TurretLevel2(
                turret_sheet2, turret.tile_x, turret.tile_y)
            return newturret

        else:
            newturret = TurretLevel3(
                turret_sheet3, turret.tile_x, turret.tile_y)
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

        self.screen.blit(self.hud_image, (c.SCREEN_WIDTH, 0))
        self.screen.blit(self.health_bar_image, (c.SCREEN_WIDTH + 40, 80))
        self.screen.blit(self.coin_bar_image, (c.SCREEN_WIDTH + 40, 130))
        self.screen.blit(self.help_image, (c.SCREEN_WIDTH+30, 490))

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

        if self.selected_turret and self.selected_turret.nivel < 3:
            if self.upgrade_button.draw(self.screen):
                if self.ControladorLevel.player.tentar_upgradear():
                    self.selected_turret.kill()
                    self.game.turret_group.add(self.upgrade_turret(
                        self.selected_turret, self.turret_sheet2, self.turret_sheet3))
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
