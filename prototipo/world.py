import pygame as pg

class World():
  def __init__(self, data, map_image):
    self.title_map = []
    self.waypoints = []
    self.level_data = data
    self.image = map_image

  def process_data(self):
    #pega os dados sobre o mapa (json) e, por meio de multiplas iteracoes, envia o dicionario com os waypoints para process_waypoints()
    for layer in self.level_data["layers"]:
      if layer["name"] == "tilemap":
        self.tile_map = layer["data"]
      elif layer["name"] == "waypoints":
        for obj in layer["objects"]:
          waypoint_data = obj["polyline"]
          self.process_waypoints(waypoint_data)

  def process_waypoints(self, data):
    #itera por cada waypoint e extrai as variaveis x e y, armazenando-as em self.waypoints
    for point in data:
      temp_x = point.get("x")
      temp_y = point.get("y")
      self.waypoints.append((temp_x, temp_y))

  def draw(self, surface):
    #desenha o mapa
    surface.blit(self.image, (0, 0))