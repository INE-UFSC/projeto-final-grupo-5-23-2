import pygame as pg
import constants as c
import json

from button import Button
from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import Turret

from states.state import State


class PauseState(State):

    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.paused = True
        self.click_sound = pg.mixer.Sound('assets/effects/click.wav')
        self.close_button = Button(300, 370, pg.image.load(
            'assets/imagens/botoes/close.png').convert_alpha(), True)
        self.back_button = Button(500, 370, pg.image.load(
            'assets/imagens/botoes/back.png').convert_alpha(), True)

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
                    self.paused = False
                    self.game.set_game_state()                  
                elif self.close_button.draw(self.screen):
                    self.click_sound.play()
                    pg.quit()
                    quit()
        pg.display.update()

    def update(self):
        self.screen.blit(pg.image.load(
            'assets/imagens/componentes/pause.png').convert_alpha(), (180, 130))
        self.back_button.draw(self.screen)
        self.close_button.draw(self.screen)
