import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
  def __init__(self, waypoints, image):
    pg.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0]) + Vector2(32, 0)
    self.target_waypoint = 1
    self.angle = 0
    self.original_image = image
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self):
    self.move()
    self.rotate()

  def move(self):
    #define o target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #ja chegou, n ha mais waypoint
      self.kill()

    #calcula distancia
    dist = self.movement.length()
    #checa se distancia n seria menor que o speed  para o inimigo nao andar " demais"
    if dist >= self.speed:
      self.pos += self.movement.normalize() * self.speed
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #calculate distancia
    dist = self.target - self.pos
    #usa distance para calcular angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotatciona imagem e re-atualiza o retangulo
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  
class InimigoFraco(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 0.5
        self.health = 10
        super().__init__(waypoints, image)

class InimigoNormal(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 1
        self.health = 20
        super().__init__(waypoints, image)
  
class InimigoForte(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 2
        self.health = 50
        super().__init__(waypoints, image)

class InimigoElite(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 1
        self.health = 500
        super().__init__(waypoints, image)