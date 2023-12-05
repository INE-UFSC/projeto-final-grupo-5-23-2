import pygame as pg
import constants as c
import json

from button import Button
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import Turret

from states.state import State


class WinState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.win = True
        self.click_sound = pg.mixer.Sound('assets/effects/click.wav')
        self.continue_button = Button(
            370, 350, pg.image.load(
            'assets/imagens/botoes/continuar.png').convert_alpha(), True)

    def handle_escape(self):
        pass

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.continue_button.draw(self.screen) == 1:
                    self.click_sound.play()
                    self.win = False
                    self.game.restart()

        pg.display.update()

    def update(self):
        self.screen.blit(pg.image.load(
            'assets/imagens/win.jpeg').convert_alpha(), (0, 0))
        self.screen.blit(pg.image.load(
            'assets/imagens/congratulations.png').convert_alpha(), (150, 220))
        self.screen.blit(pg.image.load(
            'assets/imagens/credits.png').convert_alpha(), (50, 600))
        self.continue_button.draw(self.screen)
