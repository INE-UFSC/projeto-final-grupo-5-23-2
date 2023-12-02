import pygame as pg
import constants as c
import json

from button import Button
from world import World
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3

from states.state import State


class WinState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.win = True
        self.win_image = pg.image.load(
            'assets/imagens/win.jpeg').convert_alpha()
        self.congratulations_image = pg.image.load(
            'assets/imagens/congratulations.png').convert_alpha()
        self.credits_image = pg.image.load(
            'assets/imagens/credits.png').convert_alpha()
        self.continue_button_image = pg.image.load(
            'assets/imagens/botoes/continuar.png').convert_alpha()
        self.click_sound = pg.mixer.Sound('assets/effects/click.wav')

        self.continue_button = Button(
            370, 350, self.continue_button_image, True)

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
                    self.game.set_init_state()

        pg.display.update()

    def update(self):
        self.screen.blit(self.win_image, (0, 0))
        self.screen.blit(self.congratulations_image, (150, 220))
        self.screen.blit(self.credits_image, (50, 600))
        self.continue_button.draw(self.screen)
