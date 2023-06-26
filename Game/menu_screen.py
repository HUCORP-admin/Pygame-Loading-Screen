import pygame as pg

from constants import *
from os import path

from loading_screen import LoadingScreen
from level1 import Level1


class StartScreen:
	def __init__(self, game):
		self.game = game
		
		self.bg = pg.transform.scale(
			pg.image.load(path.join(self.game.img_dir, 'title_bg.jpg')).convert(), (self.game.width, self.game.height)
		)

		self.running = True

		# fonts
		self.title_font = pg.font.Font(path.join(self.game.font_dir, 'Fiorello CG Condensed Regular.otf'), 128)
		self.start_font = pg.font.Font(path.join(self.game.font_dir, 'PressStart2P-Regular.ttf'), 14)
	
	def run(self):
		# play background music
		pg.mixer.music.load(path.join(self.game.snd_dir, 'title_track.ogg'))
		pg.mixer.music.play(loops=-1)

		while True:
			self.events()
			self.display()

	def events(self):
		for e in pg.event.get():
			if e.type == pg.KEYUP:
				pg.mixer.music.fadeout(1000)
				self.game.set_screen(LoadingScreen(self.game, Level1(self.game)))

			if e.type == pg.QUIT:
				self.game.quit()
			
	def display(self):
		# draw background
		self.game.surface.blit(self.bg, self.bg.get_rect())
		
		# draw text
		self.game.draw_text(225, 50, self.title_font, WHITE, "THE")
		self.game.draw_text(225, 180, self.title_font, WHITE, "BATMAN")

		self.game.draw_text(225, 400, self.start_font, WHITE, "Press any key to start...")

		pg.display.flip()
