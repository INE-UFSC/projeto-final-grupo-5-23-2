import pygame as pg
import constants as c

class Turret(pg.sprite.Sprite):
  
  def __init__(self, sprite_sheet, tile_x, tile_y):
    pg.sprite.Sprite.__init__(self)
    self.cooldown = 1500
    self.last_shot = pg.time.get_ticks()

    self.tile_x = tile_x
    self.tile_y = tile_y
    
    self.x = (self.tile_x + 0.5) * c.TILE_SIZE
    self.y = (self.tile_y + 0.5) * c.TILE_SIZE

    self.sprite_sheet = sprite_sheet
    self.animation_list = self.load_images()
    self.frame_index = 0
    self.update_time = pg.time.get_ticks()

    self.image = self.animation_list[self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)

  def load_images(self):
    size = self.sprite_sheet.get_height()
    animation_list = []
    for x in range(self.sprite_sheet.get_width() // size):
      temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
      animation_list.append(temp_img)
    return animation_list

  def update(self):
    if pg.time.get_ticks() - self.last_shot > self.cooldown:
      self.play_animation()

  def play_animation(self):
    self.image = self.animation_list[self.frame_index]
    if pg.time.get_ticks() - self.update_time > 15:
      self.update_time = pg.time.get_ticks()
      self.frame_index = (self.frame_index + 1) % len(self.animation_list)
      if self.frame_index == 0:
        self.last_shot = pg.time.get_ticks()