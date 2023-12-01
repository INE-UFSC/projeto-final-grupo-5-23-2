import pygame as pg
import math
import constants as c


class Turret(pg.sprite.Sprite):
  
  def __init__(self, sprite_sheet, tile_x, tile_y):
    pg.sprite.Sprite.__init__(self)
    self.last_shot = pg.time.get_ticks()
    self.selected = False  
    self.target = None

    self.tile_x = tile_x
    self.tile_y = tile_y
    
    self.x = (self.tile_x + 0.5) * c.TILE_SIZE
    self.y = (self.tile_y + 0.5) * c.TILE_SIZE

    self.sprite_sheet = sprite_sheet
    self.animation_list = self.load_images()
    self.frame_index = 0
    self.update_time = pg.time.get_ticks()

    self.angle = 90
    self.original_image = self.animation_list[self.frame_index]
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)

    self.range_image = pg.Surface((self.range * 2, self.range * 2))
    self.range_image.fill((0, 0, 0))
    self.range_image.set_colorkey((0, 0, 0)) 
    pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
    self.range_image.set_alpha(100)
    self.range_rect = self.range_image.get_rect()
    self.range_rect.center = self.rect.center


  def load_images(self):
    size = self.sprite_sheet.get_height()
    animation_list = []
    for x in range(self.sprite_sheet.get_width() // size):
      temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
      animation_list.append(temp_img)
    return animation_list

  def update(self, enemy_group, world):
    if self.target:
      self.play_animation()
    else:
      if pg.time.get_ticks() - self.last_shot > (self.cooldown/world.velocidade_jogo):
        self.pick_target(enemy_group)
  #ao inves de deixar self.cooldown/world.velocidade_jogo aqui, trocar eles para uma variavel self na hora de criar
  #o velocidade_jogo tbm n será atributo de world, mas sim de outra classed
  def pick_target(self, enemy_group):
    x_dist = 0
    y_dist = 0
    for enemy in enemy_group:
      x = enemy.pos[0] - self.x
      y = enemy.pos[1] - self.y
      dist = (x ** 2 + y ** 2) ** (1/2)
      if dist < self.range:
        self.target = enemy
        self.angle =  math.degrees(math.atan2(-y, x))
        #causar dano
        self.causar_dano(self.target)
    
  def causar_dano(self, target):
    target.health -= self.damage
        
      

  def play_animation(self):
    self.original_image = self.animation_list[self.frame_index]
    if pg.time.get_ticks() - self.update_time > 15:
      self.update_time = pg.time.get_ticks()
      self.frame_index = (self.frame_index + 1) % len(self.animation_list)
      if self.frame_index == 0:
        self.last_shot = pg.time.get_ticks()
        self.target = None

  def draw(self, surface):
    self.image = pg.transform.rotate(self.original_image, self.angle - 90  )
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
    surface.blit(self.image, self.rect)
    if self.selected:
       surface.blit(self.range_image, self.range_rect)
  

  #ideias para o delete:
  #jogar o turret pra uma tile no meio do nada(sei lá)


  
#para upgradear remove-se o turret da tile e instancia o mesmo porém de nível +1 (ideia)


class TurretLevel1(Turret):
  def __init__(self, sprite_sheet, tile_x, tile_y):
    self.range = 90
    self.cooldown = 600
    self.nivel = 1
    self.damage = 6
    super().__init__(sprite_sheet, tile_x, tile_y)


class TurretLevel2(Turret):
  def __init__(self, sprite_sheet, tile_x, tile_y):
    self.range = 110
    self.cooldown = 300
    self.nivel = 2
    self.damage = 20
    super().__init__(sprite_sheet, tile_x, tile_y)
    


class TurretLevel3(Turret):
  def __init__(self, sprite_sheet, tile_x, tile_y):
    self.range = 125
    self.cooldown = 90
    self.nivel = 3
    self.damage = 40
    super().__init__(sprite_sheet, tile_x, tile_y)