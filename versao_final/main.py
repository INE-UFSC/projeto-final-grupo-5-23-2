import pygame as pg
from pygame import mixer
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

#icone
icon_image = pg.image.load('assets/imagens/componentes/icon1.jpeg').convert_alpha()
pg.display.set_icon(icon_image)

#Para criar textos
text_font = pg.font.SysFont("Arial", 30)

def draw_text(text, font, text_color, x, y):
  img = font.render(text, True, text_color)
  screen.blit(img, (x, y))


########################################################Isso aqui deve dar pra ficar só dentro de play()
#level_comecou = False
#ultimo_spawn_inimigo = pg.time.get_ticks()
#placing_turrets = False
#selected_turret = None
########################################################
#têm q colocar dentro de play, pq sao variaveis externas. Serao atributos futuramente

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

#botoes imagens
buy_turret_image = pg.image.load('assets/imagens/botoes/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/imagens/botoes/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/imagens/botoes/upgrade_turret.png').convert_alpha()
begin_round_image = pg.image.load('assets/imagens/botoes/begin.png').convert_alpha()
acelerar_image = pg.image.load('assets/imagens/botoes/fast_forward.png').convert_alpha()

  #tela de inicio
wallpaper_image = pg.image.load('assets/imagens/wallpaper.jpeg').convert_alpha()
new_game_button_image = pg.image.load('assets/imagens/botoes/newgame.png').convert_alpha()
leave_button_image = pg.image.load('assets/imagens/botoes/leave.png').convert_alpha()
records_button_image = pg.image.load('assets/imagens/botoes/records.png').convert_alpha()
title_image = pg.image.load('assets/imagens/componentes/title.png').convert_alpha()

  #pause
pause_image = pg.image.load('assets/imagens/componentes/pause.png').convert_alpha()
close_button_image = pg.image.load('assets/imagens/botoes/close.png').convert_alpha()
back_button_image = pg.image.load('assets/imagens/botoes/back.png').convert_alpha()

  #game over
game_over_text_image = pg.image.load('assets/imagens/componentes/gameover_text.png').convert_alpha()
tela_inicial_button_image = pg.image.load('assets/imagens/botoes/tela_inicial.png').convert_alpha()
game_over_image = pg.image.load('assets/imagens/fundo_gameover.jpeg').convert_alpha()
new_game_gameover_button_image = pg.image.load('assets/imagens/botoes/novojogo_gameover.png').convert_alpha()

  #win
continue_button_image = pg.image.load('assets/imagens/botoes/continuar.png').convert_alpha()
win_image = pg.image.load('assets/imagens/win.jpeg').convert_alpha()
congratulations_image = pg.image.load('assets/imagens/congratulations.png').convert_alpha()
credits_image = pg.image.load('assets/imagens/credits.png').convert_alpha()

  #musicas e sons
click_sound = mixer.Sound('assets/effects/click.wav')

#pegando o arquivo json para usar como fase:
with open('levels/default.tmj') as file:
  world_data = json.load(file)
#carregando fontes:
fonte1 = pg.font.SysFont("Consolas", 25, bold=True)
fontegrande1 = pg.font.SysFont("Consolas", 40)


#criando "mundo"
world = World(world_data, map_image)
world.process_data()
world.process_inimigos()

def printar_texto_na_tela(text, fonte, text_col, x, y):
  img = fonte.render(text, True, text_col)
  screen.blit(img, (x, y))

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
        break
    #ver se tem dinheiro rs
    if space_is_free:
      if world.money >= c.BUY_COST:
        new_turret = TurretLevel1(turret_sheet1, mouse_tile_x, mouse_tile_y)
        turret_group.add(new_turret)
        world.money -= c.BUY_COST

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


#tela inicial
def init():

  new_game_button = Button(230, 280, new_game_button_image, True)
  leave_button = Button(230, 380, leave_button_image, True)
  records_button = Button(230, 480, records_button_image, True)
  iniciar = True
  music = mixer.Sound('assets/musics/music1.mp3')
  music.play(-1)

  while iniciar:
    clock.tick(c.FPS)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        iniciar = False
        pg.quit()
        quit()
        
      if event.type == pg.MOUSEBUTTONDOWN:
        if new_game_button.draw(screen):
          click_sound.play()
          music.stop()
          play()
        elif leave_button.draw(screen):
          click_sound.play()
          pg.quit()
          quit()
        elif records_button.draw(screen):
          click_sound.play()
          pass
      
      screen.blit(wallpaper_image, (-40, 0))
      screen.blit(title_image, (35, 130))
      new_game_button.draw(screen)
      leave_button.draw(screen)
      records_button.draw(screen)

    pg.display.update()

#game loop
def play():
  #musica

  #algumas variaveis importantes
  ultimo_spawn_inimigo = pg.time.get_ticks()
  placing_turrets = False
  selected_turret = None
  level_comecou = False
  game_over = False

  turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
  cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
  upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
  begin_round_button = Button(c.SCREEN_WIDTH + 60, 300, begin_round_image, True)
  acelerar_button = Button(c.SCREEN_WIDTH + 50, 300, acelerar_image, False)

  run = True
  while run:

    clock.tick(c.FPS)

    # Updating

    # checar se nao fomos de base ou se favela venceu
    if not game_over:
      if world.health <= 0:
        game_over = True
        tela_game_over()
      
      if world.level > c.LEVELS_TOTAIS:
        game_over = True
        tela_win()


    #atualizar grupos
    enemy_group.update(world)
    turret_group.update(enemy_group, world)

    if selected_turret:
      selected_turret.selected = True

    # Drawing ------------------------

    screen.fill("grey100")

    #desenharlevel
    world.draw(screen)

    #desenhargrupos
    enemy_group.draw(screen)
    turret_group.draw(screen)
    for turret in turret_group:
      turret.draw(screen)

    printar_texto_na_tela((str(world.health)), fonte1, "grey100", 0, 0) 
    printar_texto_na_tela((str(int(world.money))), fonte1, "grey100", 0, 30)
    printar_texto_na_tela((f"level {str(world.level)}"), fonte1, "grey100", 0, 60)

    if not game_over:
      #checar se começou:
      if not level_comecou:
        if begin_round_button.draw(screen):
          click_sound.play()
          level_comecou = True
      else:
        world.velocidade_jogo = 1
        if acelerar_button.draw(screen):
          world.velocidade_jogo = 3
        #spawnar inimigos
        if pg.time.get_ticks() - ultimo_spawn_inimigo >= c.SPAWN_COOLDOWN/world.velocidade_jogo and world.inimigos_spawnados < len(world.lista_inimigos):
          enemy_group.add(decidir_tipo_inimigo())
          ultimo_spawn_inimigo = pg.time.get_ticks()
      
      #checar se a wave n acabou:
      if world.checar_round_acabou():
        level_comecou = False

      #desenhar botoes
      if turret_button.draw(screen):
        click_sound.play()
        placing_turrets = True
      if placing_turrets == True:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
          screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
          click_sound.play()
          placing_turrets = False
      
      #se um turret for selecionado:
      if selected_turret and selected_turret.nivel < 3:
        if upgrade_button.draw(screen):
    #possivelmente no futuro player.money
          if world.money >= c.UPGRADE_COST:
            world.money -= c.UPGRADE_COST
            selected_turret.kill()
            turret_group.add(upgrade_turret(selected_turret, turret_sheet2, turret_sheet3))
            selected_turret = None

    #event handler
    for event in pg.event.get():
      
      if event.type == pg.QUIT:
        run = False
        pg.quit()
        quit()
      
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
  screen.blit(pause_image, (170, 100))
  close_button = Button(300, 370, close_button_image, True)
  back_button = Button(500, 370, back_button_image, True)
  back_button.draw(screen)
  close_button.draw(screen)

  while paused:
    clock.tick(c.FPS)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if back_button.draw(screen):
          click_sound.play()
          paused = False
        elif close_button.draw(screen):
          click_sound.play()
          pg.quit()
          quit()
    pg.display.update()

#tela game over
def tela_game_over():
  clock.tick(c.FPS)
  game_over = True

  screen.blit(game_over_image, (0, 0))
  screen.blit(game_over_text_image, (180, 220))
  new_game_button = Button(250, 370, new_game_gameover_button_image, True)
  tela_inicial_button = Button(490, 370, tela_inicial_button_image, True)
  new_game_button.draw(screen)
  tela_inicial_button.draw(screen)
  draw_text(f'Fase alcançada: {world.level}', text_font, "white", 325, 315)

  while game_over:    
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if new_game_button.draw(screen):
          click_sound.play()
          game_over = False
          restart()
        elif tela_inicial_button.draw(screen):
          click_sound.play()
          game_over = False
          init()

    pg.display.update()

#tela vitoria
def tela_win():
  clock.tick(c.FPS)
  win = True
  screen.blit(win_image, (0, 0))
  screen.blit(congratulations_image, (150, 220))
  screen.blit(credits_image, (50, 600))
  continue_button = Button(370, 350, continue_button_image, True)
  continue_button.draw(screen)

  while win:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if continue_button.draw(screen) == 1:
          click_sound.play()
          init()

    pg.display.update()

# o restart aqui terá que 1) rodar a funcao jogar de novo; e 2) resetar todas as classes e objetos q nós tínhamos
# basicamente rodará a nossa classe principal de novo (o que ainda n foi feito). Ent, n precisa de definir a funcao restart.
def restart():
  world = World(world_data, map_image)
  #etc

init()


pg.quit()