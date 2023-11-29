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
  #para mim(murta): world so esta para adicionar dinheiro, pode mudar para player e como atributo de inicializacao depois
  def update(self, world):
    self.move(world)
    self.rotate()
    self.checar_vivo(world)
  #checa todos os "ciclos"de clock

  def move(self, world):
    #define o target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #ja chegou, n ha mais waypoint
      world.health -= self.forca
      world.inimigos_perdidos += 1
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

  def checar_vivo(self, world):
     if self.health <= 0:
        world.money += self.reward
        world.inimigos_killados += 1
        self.kill()
  
class InimigoFraco(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 0.5
        self.health = 10
        self.reward = 10
        self.forca = 1
        super().__init__(waypoints, image)

class InimigoNormal(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 1.8
        self.health = 20
        self.reward = 20
        self.forca = 2
        super().__init__(waypoints, image)
  
class InimigoForte(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 2.5
        self.health = 50
        self.reward = 50
        self.forca = 10
        super().__init__(waypoints, image)

class InimigoElite(Enemy):
    def __init__(self, waypoints, image):
        self.speed = 1
        self.health = 500
        super().__init__(waypoints, image)