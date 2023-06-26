import pygame as pg
from constants import *
from base_sprite import AnimatedSprite

vec = pg.math.Vector2

class Bullet(AnimatedSprite):
	def __init__(self, screen, pos, dir, damage, anim=None, *groups):
		super().__init__(groups)
		self.screen = screen
		self.damage = damage

		# image
		if anim != None:
			self.store_animation("bullet", anim)
			self.image = self.active_anim.get_frame(0)
		else:
			self.image = pg.Surface((20, 10))
			self.image.fill(YELLOW)

		self.rect = self.image.get_rect()

		# position
		self.pos = vec(pos)
		self.rect.center = pos
		self.vel = vec(dir * PLAYER_BULLET_SPEED, 0)

		self.x = self.pos.x

	def update(self):
		super().update(1/self.screen.game.fps)

		if self.active_name != "":
			center = self.rect.center
			self.image = self.active_anim.get_frame(self.elapsed_time)
			self.rect = self.image.get_rect()
			self.rect.center = center

		self.pos += self.vel * 1/self.screen.game.fps
		self.rect.center = self.pos

		if pg.sprite.spritecollideany(self, self.screen.walls):
			self.kill()

		if abs(self.pos.x - self.x) > BULLET_DISTANCE:
			self.kill()


class Obstacle(pg.sprite.Sprite):
	def __init__(self, x, y, w, h, *groups):
		super().__init__(groups)

		# rect
		self.rect = pg.Rect(x, y, w, h)
		self.hit_rect = self.rect

		# position
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
