import pygame as pg
from constants import *

from os import path
from game import Game
from menu_screen import StartScreen


class Launcher(Game):
	def __init__(self):
		super().__init__(WIDTH, HEIGHT)
		pg.display.set_caption("The Batman")

		# locate asset directories
		self.img_dir = path.join(self.dir, 'assets', 'img')
		self.snd_dir = path.join(self.dir, 'assets', 'snd')
		self.font_dir = path.join(self.dir, 'assets', 'font')
		self.map_dir = path.join(self.dir, 'assets', 'map')

		# constants
		self.fps = 60

	def start(self):
		start_screen = StartScreen(self)
		self.set_screen(start_screen)


if __name__ == "__main__":
	launcher = Launcher()
	launcher.start()
