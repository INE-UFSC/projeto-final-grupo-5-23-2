import pygame as pg
from pygame import mixer
import math
import constants as c
from abc import ABC, abstractmethod

class Tower(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def update(self, enemy, controlador):
        pass

    def ativar(self, player):
        pass

    def calcular_tiles(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

class Turret(pg.sprite.Sprite, Tower):

    def __init__(self, sprite_sheet, tile_x, tile_y, range, cooldown, damage):
        pg.sprite.Sprite.__init__(self)
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.level = 0

        self.range = range
        self.cooldown = cooldown
        self.damage = damage

        self.calcular_tiles(tile_x, tile_y)

        self.sprite_sheet = sprite_sheet
        self.max_level = len(sprite_sheet)-1
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.desenhar_range()
    
    def upgrade(self):
        if self.level < self.max_level:
            self.level += 1
            self.damage = self.damage + self.level * self.damage
            self.cooldown = self.cooldown - self.cooldown * 0.3
            self.range = self.range + self.level * 0.15
            self.animation_list = self.load_images()
            self.original_image = self.animation_list[self.frame_index]

    def load_images(self):
        size = self.sprite_sheet[self.level].get_height()
        animation_list = []
        for x in range(self.sprite_sheet[self.level].get_width() // size):
            temp_img = self.sprite_sheet[self.level].subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group, ControladorLevel):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > (self.cooldown/ControladorLevel.velocidade_jogo):
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            x = enemy.pos[0] - self.x
            y = enemy.pos[1] - self.y
            dist = (x ** 2 + y ** 2) ** (1/2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y, x))
                # causar dano
                shot_sound = mixer.Sound('assets/effects/shot.wav')
                shot_sound.play()
                self.causar_dano(self.target)

    def causar_dano(self, target):
        target.health -= self.damage

    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > 15:
            self.update_time = pg.time.get_ticks()
            self.frame_index = (self.frame_index +
                                1) % len(self.animation_list)
            if self.frame_index == 0:
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def desenhar_range(self):
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100",
                       (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    
class FarmingTurret(pg.sprite.Sprite, Tower):
    def __init__(self, image, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)

        self.image = image
        
        self.calcular_tiles(tile_x, tile_y)

        self.money_per_turn = c.MONEY_PER_TURN_TORRE
        self.rect = self.image.get_rect()

        self.level = 1
        self.max_level = 1
    
    def ativar(self, player):
        player.money += self.money_per_turn
    
    def draw(self, surface):
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
    

#não vai ter upgrade pois não achei uma sprite para colocar como upgrade kkk

