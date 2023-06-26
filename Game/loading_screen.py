import pygame as pg
import threading
import queue

from level1 import Level1
from constants import *


class LoadingScreen:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.progress = 0
        self.queue = queue.Queue()

        # font
        self.font_size = 28
        self.font = pg.font.Font(pg.font.match_font('sans-serif'), self.font_size)

    def run(self):
        if type(self.level) is Level1:
            loading_thread = threading.Thread(target=self.level.new, args=(self.queue,))
            loading_thread.start()
        else:
            # Todo - load a different level
            pass

        while True:
            self.events()
            self.display()
            self.update()

            if not loading_thread.is_alive():
                self.game.set_screen(self.level)

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                # quit the game
                self.game.quit()

    def display(self):
        # fill background
        self.game.surface.fill(BLACK)

        # progress bar
        bar_height = 30
        bar_width = WIDTH - WIDTH/4

        x = WIDTH/2 - bar_width/2
        y = HEIGHT/2

        pct = self.progress / 100
        if pct >= 1:
            pct = 1

        fill = pct*bar_width
        outline_rect = pg.Rect(x - 10, y - 10, bar_width + 20, bar_height + 20)
        fill_rect = pg.Rect(x, y, fill, bar_height)

        # draw bar
        pg.draw.rect(self.game.surface, WHITE, fill_rect)
        pg.draw.rect(self.game.surface, WHITE, outline_rect, 2)

        # draw text
        self.game.draw_text(WIDTH/2 - self.font_size/2, HEIGHT/2 - self.font_size/2 - bar_height - 50, self.font, WHITE, "Loading...")

        # *flip* the display
        pg.display.flip()

    def update(self):
        if not self.queue.empty():
            self.progress = self.queue.get()
