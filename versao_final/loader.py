#carrega imagens, arquivos, ect
import constants as c
import pygame as pg
from pygame import mixer
from button import Button

class Loader():
    def __init__(self, screen, clock, game):
        self.load_principal(game)

    def load_principal(self, game):
        self.placing_turrets = False
        self.placing_attack_turret = False
        self.placing_farming_turret = False
        self.selected_turret = None
        self.level_comecou = False
        self.game_over = False
        self.choosing_turret = False
        self.tips_flag = False

        self.hud_image = pg.image.load(
            'assets/imagens/hud.jpg').convert_alpha()
        self.health_bar_image = pg.image.load(
            'assets/imagens/componentes/health_bar.png').convert_alpha()
        self.coin_bar_image = pg.image.load(
            'assets/imagens/componentes/coin_bar.png').convert_alpha()
        self.help_image = pg.image.load(
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
        self.fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.cursor_turret = None
        self.turret_sheet1 = pg.image.load(
            'assets/imagens/torres/turret_1.png').convert_alpha()
        self.turret_sheet2 = pg.image.load(
            'assets/imagens/torres/turret_2.png').convert_alpha()
        self.turret_sheet3 = pg.image.load(
            'assets/imagens/torres/turret_3.png').convert_alpha()
        self.farm_turret_sheet = pg.image.load(
            'assets/imagens/torres/farming_turret.png').convert_alpha()
        self.farm_turret_sheet = pg.transform.scale_by(self.farm_turret_sheet, 1/6)