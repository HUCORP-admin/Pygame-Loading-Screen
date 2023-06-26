import pygame as pg
import sys

from os import path


class Game:
	def __init__(self, width, height):
		# initialize pygame
		pg.init()
		pg.mixer.init()

		self.width = width
		self.height = height

		# set screen
		self.screen = None
		self.surface = pg.display.set_mode((self.width, self.height))
		self.clock = pg.time.Clock()

		# current directory
		self.dir = path.dirname(__file__)

		# colors
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.green = (0, 255, 0)
		self.light_green = (34, 177, 76)

	def draw_text(self, x, y, font, color, text):
		surface = font.render(text, True, color)
		rect = surface.get_rect()
		rect.midtop = (x, y)
		self.surface.blit(surface, rect)

	def set_screen(self, scr):
		# delete existing screen
		if self.screen != None:
			del self.screen
			self.screen = None

		self.screen = scr

		# show new screen
		if (self.screen != None):
			self.screen.run()

	def quit(self):
		# exit the game
		pg.quit()
		sys.exit()

	def events(self):
		# handle events in game loop
		for e in pg.event.get():
			if e.type == pg.QUIT:
				self.quit()
