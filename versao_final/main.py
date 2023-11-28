import pygame as pg
import json
from enemy import InimigoFraco, InimigoNormal, InimigoElite, InimigoForte
from world import World
from turret import TurretLevel1, TurretLevel2, TurretLevel3
from button import Button
import constants as c

#COMO ESTA EM DESENVOLVIMENTO, O MAIN.PY ESTA PROCEDURAL (AINDA)
#VERSAO BETA

#iniciando pygame
pg.init()


#criando clock
clock = pg.time.Clock()

#criando janela do jogo
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.PANEL_SIZE, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

#Para criar textos
text_font = pg.font.SysFont("Arial", 30)

def draw_text(text, font, text_color, x, y):
  img = font.render(text, True, text_color)
  screen.blit(img, (x, y))


########################################################Isso aqui deve dar pra ficar só dentro de play()
ultimo_spawn_inimigo = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
########################################################



#mapa
map_image = pg.image.load('levels/default.png').convert_alpha()

#turret
turret_sheet1 = pg.image.load('assets/imagens/torres/turret_1.png').convert_alpha()
turret_sheet2 = pg.image.load('assets/imagens/torres/turret_2.png').convert_alpha()
turret_sheet3 = pg.image.load('assets/imagens/torres/turret_3.png').convert_alpha()
cursor_turret = pg.image.load('assets/imagens/torres/cursor_turret.png').convert_alpha()


#inimigos
enemy_image1 = pg.image.load('assets/imagens/inimigos/enemy_1.png').convert_alpha()
enemy_image2 = pg.image.load('assets/imagens/inimigos/enemy_2.png').convert_alpha()
enemy_image3 = pg.image.load('assets/imagens/inimigos/enemy_3.png').convert_alpha()

#enemy_image = pg.transform.scale_by(enemy_image, 1/8) nao apagar

#botoes
buy_turret_image = pg.image.load('assets/imagens/botoes/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/imagens/botoes/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/imagens/botoes/upgrade_turret.png').convert_alpha()

  #tela de inicio
wallpaper_image = pg.image.load('assets/imagens/wallpaper.jpeg').convert_alpha()
new_game_button_image = pg.image.load('assets/imagens/botoes/newgame.png').convert_alpha()
leave_button_image = pg.image.load('assets/imagens/botoes/leave.png').convert_alpha()
records_button_image = pg.image.load('assets/imagens/botoes/records.png').convert_alpha()

  #pause
pause_image = pg.image.load('assets/imagens/componentes/pause.png').convert_alpha()
close_button_image = pg.image.load('assets/imagens/botoes/close.png').convert_alpha()
back_button_image = pg.image.load('assets/imagens/botoes/back.png').convert_alpha()

#pegando o arquivo json para usar como fase:
with open('levels/default.tmj') as file:
  world_data = json.load(file)

#criando "mundo"
world = World(world_data, map_image)
world.process_data()
world.process_inimigos()

#ta horrivel isso, eu sei PROCEDURAL
def decidir_tipo_inimigo():
  tipo = world.lista_inimigos[world.inimigos_spawnados]
  world.inimigos_spawnados += 1
  if tipo == "fraco":
    return InimigoFraco(world.waypoints, enemy_image1)
  elif tipo == "normal":
    return InimigoNormal(world.waypoints, enemy_image2)
  else:
    return InimigoForte(world.waypoints, enemy_image3)
#por enquanto o inimigo elite ta gerando o inimigo forte mesmo


def upgrade_turret(turret, turret_sheet2, turret_sheet3):
  #teria como concatenar o numero +1 mas deu preguica
  if turret.nivel == 1:
      newturret = TurretLevel2(turret_sheet2, turret.tile_x, turret.tile_y)
      return newturret

  else:
      newturret = TurretLevel3(turret_sheet3, turret.tile_x, turret.tile_y)
      return newturret

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
      new_turret = TurretLevel1(turret_sheet1, mouse_tile_x, mouse_tile_y)
      turret_group.add(new_turret)

def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return turret  
    
def clear_selection():
  for turret in turret_group:
    turret.selected = False

#criando grupos de inimigos
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()


#create buttons 
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
new_game_button = Button(c.SCREEN_WIDTH + 50, 300, new_game_button_image, True)
close_button = Button(300, 370, close_button_image, True)
back_button = Button(500, 370, back_button_image, True)

#game loop
def play():
  ultimo_spawn_inimigo = pg.time.get_ticks()
  placing_turrets = False
  selected_turret = None
  run = True
  while run:

    clock.tick(c.FPS)

    # Updating

    #atualizar grupos
    enemy_group.update()
    turret_group.update(enemy_group)

    if selected_turret:
      selected_turret.selected = True

    # Drawing

    screen.fill("grey100")

    #desenharlevel
    world.draw(screen)

    #desenhargrupos
    enemy_group.draw(screen)
    turret_group.draw(screen)
    for turret in turret_group:
      turret.draw(screen)


    #spawnar inimigos
    if pg.time.get_ticks() - ultimo_spawn_inimigo >= c.SPAWN_COOLDOWN and world.inimigos_spawnados < len(world.lista_inimigos):
      enemy_group.add(decidir_tipo_inimigo())
      ultimo_spawn_inimigo = pg.time.get_ticks()


    #desenhar botoes
    if turret_button.draw(screen):
      placing_turrets = True
    if placing_turrets == True:
      cursor_rect = cursor_turret.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_turret, cursor_rect)
      if cancel_button.draw(screen):
        placing_turrets = False
    
    #se um turret for selecionado:
    if selected_turret and selected_turret.nivel < 3:
      if upgrade_button.draw(screen):
        turret_group.remove(selected_turret)
        turret_group.add(upgrade_turret(selected_turret, turret_sheet2, turret_sheet3))
        selected_turret = None

    #event handler
    for event in pg.event.get():
      
      if event.type == pg.QUIT:
        run = False
      
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pg.mouse.get_pos()
        if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
          selected_turret = None
          clear_selection()
          if placing_turrets == True:
            create_turret(mouse_pos)
          else:
              selected_turret = select_turret(mouse_pos)

      if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          pause()



    #update display
    pg.display.flip()


#Para pausar
def pause():
  paused = True

  while paused:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()
    
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if back_button.draw(screen):
          paused = False
        elif close_button.draw(screen):
          pg.quit()
          quit()

    screen.fill('blue')
    back_button.draw(screen)
    close_button.draw(screen)
    pg.display.update()
    clock.tick(30)


play()

pg.quit()