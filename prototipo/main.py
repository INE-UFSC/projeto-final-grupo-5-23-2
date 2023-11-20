import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as c

#COMO ESTA EM DESENVOLVIMENTO, O MAIN.PY ESTA PROCEDURAL (AINDA)
#VERSAO BETA

#iniciando pygame
pg.init()


#criando clock
clock = pg.time.Clock()

#criando janela do jogo
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")


#mapa
map_image = pg.image.load('levels/default.png').convert_alpha()

#turret
turret_image = pg.image.load('assets/imagens/torres/dot_blue.png').convert_alpha()
turret_image = pg.transform.scale_by(turret_image, 1/25)

#inimigos
enemy_image = pg.image.load('assets/imagens/inimigos/Location_dot_black.svg.png').convert_alpha()
enemy_image = pg.transform.scale_by(enemy_image, 1/15)

#pegando o arquivo json para usar como fase:
with open('levels/default.tmj') as file:
  world_data = json.load(file)

#criando "mundo"
world = World(world_data, map_image)
world.process_data()


def create_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #checar se a tile eh valida para torre
  if world.tile_map[mouse_tile_num] == 38:
    #checar se ja nao tem uma torre la
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
    #finalmente criar a torre
    if space_is_free:
      new_turret = Turret(turret_image, mouse_tile_x, mouse_tile_y)
      turret_group.add(new_turret)

#criando grupos de inimigos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  screen.fill("grey100")

  #desenharlevel
  world.draw(screen)

  #atualizar grupos
  enemy_group.update()

  #desenhargrupos
  enemy_group.draw(screen)
  turret_group.draw(screen)

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      create_turret(mouse_pos)
      
  #update display
  pg.display.flip()

pg.quit()