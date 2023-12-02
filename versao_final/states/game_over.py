import pygame as pg
import constants as c
import json

from button import Button
from world import World
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3

from states.state import State


class GameOverState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.game_over = True
        self.game_over_image = pg.image.load(
            'assets/imagens/fundo_gameover.jpeg').convert_alpha()
        self.game_over_text_image = pg.image.load(
            'assets/imagens/componentes/gameover_text.png').convert_alpha()
        self.new_game_button_image = pg.image.load(
            'assets/imagens/botoes/novojogo_gameover.png').convert_alpha()
        self.tela_inicial_button_image = pg.image.load(
            'assets/imagens/botoes/tela_inicial.png').convert_alpha()
        self.click_sound = pg.mixer.Sound('assets/effects/click.wav')

        self.new_game_button = Button(
            250, 370, self.new_game_button_image, True)
        self.tela_inicial_button = Button(
            490, 370, self.tela_inicial_button_image, True)
        self.text_font = pg.font.SysFont("Arial", 30)

    def handle_escape(self):
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.new_game_button.draw(self.screen):
                    self.click_sound.play()
                    self.game_over = False
                    self.game.restart()
                elif self.tela_inicial_button.draw(self.screen):
                    self.click_sound.play()
                    self.game_over = False
                    self.game.set_init_state()

        pg.display.update()

    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def update(self):
        self.screen.blit(self.game_over_image, (0, 0))
        self.screen.blit(self.game_over_text_image, (180, 220))
        self.new_game_button.draw(self.screen)
        self.tela_inicial_button.draw(self.screen)
        self.draw_text(
            f'Fase alcançada: {self.game.world.level}', self.text_font, "white", 325, 315)
