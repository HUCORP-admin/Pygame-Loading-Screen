from typing import Tuple
import pygame as pg
from os import path

from constants import *
from base_sprite import Character
from spritesheet import Spritesheet, Animation


class MeleeEnemy(Character):
	def __init__(self, screen, x, y, *groups):
		super().__init__((x, y), MELEE_DAMAGE, groups)
		self.screen = screen

		# position
		self.x = x
		self.y = y

		# specify image
		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.midbottom = (x, y)

		# combat
		self.attack_count = 0

	def load(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'melee_enemy_spritesheet.png'), bg=(0, 64, 128))
		
		# walking animation
		walking_frames = [(5, 9, 35, 76), (8, 94, 46, 74), (65, 94, 50, 72), (128, 93, 36, 73), (172, 93, 39, 75), (219, 94, 42, 74), (274, 93, 41, 75), (320, 93, 49, 75)]
		walking_animation = spritesheet.get_animation(walking_frames, 0.20, Animation.PlayMode.LOOP)
		self.store_animation('walking', walking_animation)

		# attacking animation
		attacking_frames = [(6, 176, 46, 80), (56, 172, 52, 84), (138, 259, 63, 76), (207, 262, 39, 73)]
		attacking_animation = spritesheet.get_animation(attacking_frames, 0.20, Animation.PlayMode.LOOP)
		self.store_animation('attacking', attacking_animation)

	def move(self):
		if self.active_name == 'walking':
			if self.direction == 'R':
				self.acc.x = MELEE_ACC
			elif self.direction == 'L':
				self.acc.x = -MELEE_ACC

	def attack(self):
		self.set_active_animation('attacking')

	def animate(self):
		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)

		# flip image if necessary
		if self.direction == 'L':
			self.image = pg.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		super().update(1/self.screen.game.fps)
		self.animate()

		if self.attack_count > 0:
			self.set_active_animation("attacking")
		else:
			self.set_active_animation("walking")

		if abs(self.vel.x - MELEE_MAX_SPEED) > 0:
			if self.vel.x > 0:
				self.vel.x = MELEE_MAX_SPEED
			else:
				self.vel.x = -MELEE_MAX_SPEED

		if self.pos.x - self.x > MELEE_WALKING_DISTANCE:
			self.direction = 'L'
			self.vel.x = 0
			self.pos.x = self.x + MELEE_WALKING_DISTANCE

		elif self.pos.x - self.x < 0:
			self.direction = 'R'
			self.vel.x = 0
			self.pos.x = self.x

		self.attack_count = 0
		self.rect.midbottom = self.pos
		
		if self.health <= 0:
			self.kill()


class ShooterEnemy(Character):
	def __init__(self, screen, x, y, *groups):
		super().__init__((x, y), SHOOTER_DAMAGE, groups)
		self.screen = screen

		# position
		self.x = x
		self.y = y
		self.direction = 'R'
		
		# image
		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.midbottom = (x, y)

		# update properties
		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

		self.bullet_animation = self.load_bullet()
		self.last_shot = 0
		
	def load(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'shooter_enemy_spritesheet.png'), bg=(153, 41, 189))

		# standing animation
		standing_frames = [(1, 7, 37, 74), (42, 6, 35, 75), (82, 5, 34, 76), (122, 6, 33, 75)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP)
		self.store_animation('standing', standing_animation)

		# shooting animation
		shooting_frames = [(2, 254, 37, 58), (42, 253, 44, 59), (90, 256, 51, 56), (144, 247, 94, 65), (247, 253, 44, 59), (296, 256, 51, 56), (353, 254, 37, 58)]
		#shooting_frames = [(2, 170, 36, 70), (41, 167, 49, 73), (96, 170, 56, 70), (159, 170, 81, 70), (246, 167, 49, 73), (301, 170, 56, 70), (364, 170, 36, 70)]
		shooting_animation = spritesheet.get_animation(shooting_frames, 0.10, Animation.PlayMode.NORMAL)
		self.store_animation('shooting', shooting_animation)

	def load_bullet(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'shooter_enemy_spritesheet.png'), bg=(153, 41, 189))
		return spritesheet.get_animation([(511, 297, 14, 3)], 1, Animation.PlayMode.LOOP)

	def move(self):
		if abs(self.screen.player.pos.y - self.pos.y) < PLATFORM_GAP:
			if self.screen.player.pos.x > self.pos.x:
				self.direction = 'R'
			elif self.screen.player.pos.x < self.pos.x:
				self.direction = 'L'

	def attack(self):
		if abs(self.screen.player.pos.x - self.pos.x) < SHOOTER_RANGE:
			if self.screen.player.rect.bottom > self.rect.top:
				if self.active_name == "standing" and (pg.time.get_ticks() - self.last_shot) > SHOOTER_DELAY:
					self.shoot_count += 1

	def animate(self):
		if self.active_name == 'shooting':
			if self.active_anim.get_frame_index(self.elapsed_time) > 2:
				if self.shoot_count > 0:
					if self.direction == 'R':
						self.screen.create_bullet((self.rect.right, self.rect.top + 10), 1, SHOOTER_DAMAGE, self.screen.enemy_bullets, self.bullet_animation)
					elif self.direction == 'L':
						self.screen.create_bullet((self.rect.left, self.rect.top + 10), -1, SHOOTER_DAMAGE, self.screen.enemy_bullets, self.bullet_animation)
					
					self.shoot_count = 0
					self.last_shot = pg.time.get_ticks()

			if self.is_animation_finished():
				self.set_active_animation('standing')

		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)

		# flip image if necessary
		if self.direction == 'L':
			self.image = pg.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		super().update(1/self.screen.game.fps)
		self.attack()
		self.animate()
		self.rect.midbottom = self.pos

		# update properties
		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

		if self.shoot_count > 0:
			self.set_active_animation("shooting")

		if self.health <= 0:
			self.kill()
