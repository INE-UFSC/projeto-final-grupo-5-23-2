import pygame as pg
from pygame.math import Vector2
import math


class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image, speed, health, reward, forca):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0]) + Vector2(32, 0)
        self.target_waypoint = 1
        self.angle = 0
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.speed = speed
        self.health = health
        self.reward = reward
        self.forca = forca


    def update(self, ControladorLevel):
        self.move(ControladorLevel)
        self.rotate()
        self.checar_vivo(ControladorLevel)
    # checa todos os "ciclos"de clock

    def move(self, ControladorLevel):
        # define o target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # ja chegou, n ha mais waypoint
            ControladorLevel.inimigo_chegou(self)
            self.kill()

        # calcula distancia
        dist = self.movement.length()
        # checa se distancia n seria menor que o speed  para o inimigo nao andar " demais"
        if dist >= (self.speed*ControladorLevel.velocidade_jogo):
            self.pos += self.movement.normalize() * (self.speed*ControladorLevel.velocidade_jogo)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        # calculate distancia
        dist = self.target - self.pos
        # usa distance para calcular angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotatciona imagem e re-atualiza o retangulo
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def checar_vivo(self, ControladorLevel):
        if self.health <= 0:
            ControladorLevel.player.money += self.reward
            ControladorLevel.inimigos_killados += 1
            self.kill()


class InimigoFraco(Enemy):
    def __init__(self, waypoints, image):
        super().__init__(waypoints, image, 1.2, 30, 10, 1)


class InimigoNormal(Enemy):
    def __init__(self, waypoints, image):
        super().__init__(waypoints, image, 1, 90, 40, 5)


class InimigoForte(Enemy):
    def __init__(self, waypoints, image):
        super().__init__(waypoints, image, 1.5, 200, 80, 20)


class InimigoElite(Enemy):
    def __init__(self, waypoints, image):
        super().__init__(waypoints, image, 1, 500, 300, 30)
