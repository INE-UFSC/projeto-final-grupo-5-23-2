import pygame as pg
import constants as c
import json

from button import Button
from world import World
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3

from states.state import State


class PauseState(State):

    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.paused = True
        self.pause_image = pg.image.load('assets/imagens/componentes/pause.png').convert_alpha()
        self.close_button_image = pg.image.load('assets/imagens/botoes/close.png').convert_alpha()
        self.back_button_image = pg.image.load('assets/imagens/botoes/back.png').convert_alpha()
        self.click_sound = pg.mixer.Sound('assets/effects/click.wav')

        self.close_button = Button(300, 370, self.close_button_image, True)
        self.back_button = Button(500, 370, self.back_button_image, True)

    def handle_escape(self):
        self.game.set_game_state()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.draw(self.screen):
                    self.click_sound.play()
                    self.game.set_game_state()
                    self.paused = False
                elif self.close_button.draw(self.screen):
                    self.click_sound.play()
                    pg.quit()
                    quit()
        pg.display.update()

    def update(self):
        self.screen.blit(self.pause_image, (170, 100))
        self.back_button.draw(self.screen)
        self.close_button.draw(self.screen)
        