import pygame as pg
from constants import *

vec = pg.math.Vector2


class AnimatedSprite(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)

		# control
		self.elapsed_time = 0
		self.active_anim = None
		self.active_name = ""
		self.animation_storage = {}

	def store_animation(self, name, anim):
		self.animation_storage[name] = anim

		# if no animation playing, start this one
		if self.active_name == "":
			self.set_active_animation(name)

	def set_active_animation(self, name):
		# check if animation with name exist
		if name not in self.animation_storage.keys():
			print(f'No animation: {name}')
			return

		# check if this animation is already running
		if name == self.active_name:
			return

		self.active_name = name
		self.active_anim = self.animation_storage[name]
		self.elapsed_time = 0

	def is_animation_finished(self):
		return self.active_anim.is_animation_finished(self.elapsed_time)

	def update(self, dt):
		self.elapsed_time += dt


class Character(AnimatedSprite):
	def __init__(self, pos, damage, *groups):
		super().__init__(groups)
		
		# properties
		self.health = HEALTH
		self.damage = damage
		self.direction = 'R'
		self.alive = True
		
		# physics
		self.ground_count = 0
		self.attack_count = 0
		self.shoot_count = 0
		self.pos = vec(pos)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

	def move(self):
		pass

	def update(self, dt):
		super().update(dt)

		# apply gravity
		# self.acc = vec(0, 0)
		self.acc = vec(0, GRAVITY)

		# movement
		self.move()

		# apply friction
		self.acc.x += self.vel.x * FRICTION

		# eqns of motions
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		if abs(self.vel.x) < 0.5:
			self.vel.x = 0

		if self.vel.y > 10:
			self.vel.y = 10