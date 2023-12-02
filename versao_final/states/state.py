import pygame as pg


class State:

    def __init__(self, screen, clock, game):
        self.screen = screen
        self.clock = clock
        self.game = game

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.handle_escape()

    def handle_escape(self):
        pass

    def update(self):
        pass
