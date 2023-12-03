import pygame as pg
import constants as c
import json

from button import Button

from pygame import mixer
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from turret import TurretLevel1, TurretLevel2, TurretLevel3

from states.state import State


class InitState(State):
    def __init__(self, screen, clock, game):
        super().__init__(screen, clock, game)
        self.new_game_button = Button(230, 280, pg.image.load(
            'assets/imagens/botoes/newgame.png').convert_alpha(), True)
        self.leave_button = Button(230, 380, pg.image.load(
            'assets/imagens/botoes/leave.png').convert_alpha(), True)
        self.records_button = Button(230, 480, pg.image.load(
            'assets/imagens/botoes/records.png').convert_alpha(), True)
        self.click_sound = mixer.Sound('assets/effects/click.wav')
        self.wallpaper_image = pg.image.load(
            'assets/imagens/wallpaper.jpeg').convert_alpha()
        self.title_image = pg.image.load(
            'assets/imagens/componentes/title.png').convert_alpha()
        self.music = mixer.Sound('assets/musics/music1.mp3')
        self.music.play(-1)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.new_game_button.draw(self.screen):
                    self.click_sound.play()
                    self.music.stop()
                    self.game.set_game_state()
                elif self.leave_button.draw(self.screen):
                    self.click_sound.play()
                    self.game.running = False
                    pg.quit()
                    quit()
                elif self.records_button.draw(self.screen):
                    self.click_sound.play()
                    pass

    def update(self):
        self.screen.blit(self.wallpaper_image, (-40, 0))
        self.screen.blit(self.title_image, (35, 130))
        self.new_game_button.draw(self.screen)
        self.leave_button.draw(self.screen)
        self.records_button.draw(self.screen)
