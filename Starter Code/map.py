import pygame as pg
from pytmx.util_pygame import load_pygame


class TiledMap:
	def __init__(self, filename):
		self.tmx_data = load_pygame(filename)
		self.width = self.tmx_data.width * self.tmx_data.tilewidth
		self.height = self.tmx_data.height * self.tmx_data.tileheight

	def render(self, surface):
		for layer in self.tmx_data.visible_layers:
			if hasattr(layer, 'data'):
				for x, y, gid in layer:
					tile = self.tmx_data.get_tile_image_by_gid(gid)
					if tile:
						surface.blit(tile, (x*self.tmx_data.tilewidth, y*self.tmx_data.tileheight))

	def make_map(self):
		temp_surface = pg.Surface((self.width, self.height))
		self.render(temp_surface)
		return temp_surface, temp_surface.get_rect()


class Camera:
	def __init__(self, game, width, height):
		self.game = game
		self.camera = pg.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def apply_rect(self, rect):
		return rect.move(self.camera.topleft)

	def draw_bg(self, surface, img, rect):
		surface.blit(img, self.apply_rect(rect))

	def draw(self, surface, group):
		for sprite in group:
			surface.blit(sprite.image, self.apply(sprite))

	def draw_debug(self, surface, *groups):
		for group in groups:
			for sprite in group:
				pg.draw.rect(surface, (0, 255, 255), self.apply_rect(sprite.rect), 1)


	def update(self, target):
		x = max(-self.width + self.game.width, min(0, -target.rect.x + int(self.game.width/2)))
		y = max(-self.height + self.game.height, min(0, -target.rect.y + int(self.game.height/2)))

		self.camera = pg.Rect(x, y, self.width, self.height)
		self.camera.move(self.camera.topleft)