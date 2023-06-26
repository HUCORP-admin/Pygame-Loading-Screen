import pygame as pg

from constants import *

from os import path
from base_sprite import Character
from spritesheet import Spritesheet, Animation


class Player(Character):
	def __init__(self, screen, x, y, *groups):
		super().__init__((x, y), PLAYER_DAMAGE, groups)
		self.screen = screen

		# position
		self.x = x
		self.y = y

		self.direction = 'R'
		
		# specify image
		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.midbottom = (x, y)

		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

		# bullet
		self.bullet_animation = self.load_bullet()
		
	def load(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		# MOVEMENT ANIMATIONS
		# walking animation
		walking_frames = [[22, 346, 62, 55], [88, 348, 65, 49], [160, 345, 65, 54], [238, 344, 53, 56], \
			[296, 338, 60, 57], [365, 342, 63, 51], [433, 343, 65, 52], [503, 343, 58, 55]]
		walking_anim = spritesheet.get_animation(walking_frames, 0.12, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('walking', walking_anim)

		# standing animation
		standing_frames = [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('standing', standing_animation)

		# jumping animation
		jumping_frames = [(609, 343, 43, 51), (664, 337, 48, 64), (720, 338, 48, 64)]
		jumping_animation = spritesheet.get_animation(jumping_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('jumping', jumping_animation)

		# falling animation
		falling_frames = [(773, 344, 60, 50), (839, 323, 44, 80), (897, 326, 46, 77)]
		falling_animation = spritesheet.get_animation(falling_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('falling', falling_animation)

		# landing animation
		landing_frames = [(960, 336, 47, 69), (1023, 362, 47, 43), (1081, 352, 42, 52)]
		landing_animation = spritesheet.get_animation(landing_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('landing', landing_animation)

		# ATTACKING ANIMATIONS
		# first punch
		attack1_frames = [(34, 724, 53, 51), (93, 722, 78, 51), (176, 723, 75, 51), (259, 723, 73, 51), (336, 718, 52, 56)]
		attack1_animation = spritesheet.get_animation(attack1_frames, 0.05, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('attack1', attack1_animation)

		# second punch
		attack2_frames = [(616, 711, 53, 60), (677, 715, 50, 56), (734, 718, 78, 53), (821, 718, 77, 53), (906, 717, 59, 54)]
		attack2_animation = spritesheet.get_animation(attack2_frames, 0.05, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('attack2', attack2_animation)

		# third punch
		attack3_frames = [(24, 845, 51, 55), (86, 848, 55, 53), (150, 847, 82, 54), (240, 847, 80, 54), (327, 846, 67, 55), (403, 848, 46, 53)]
		attack3_animation = spritesheet.get_animation(attack3_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('attack3', attack3_animation)

		# batarang throw
		batarang_throw_frames = [(20, 1004, 46, 54), (81, 997, 53, 61), (149, 1004, 82, 54), (239, 1004, 72, 54), (326, 1003, 67, 55)]
		batarang_throw_animation = spritesheet.get_animation(batarang_throw_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('batarang_throw', batarang_throw_animation)

		# death animation
		death_frames = [(216, 598, 54, 60), (281, 610, 67, 47), (367, 636, 71, 19)]
		death_animation = spritesheet.get_animation(death_frames, 0.15, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('death', death_animation)

	def load_bullet(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		batarang_frames = [(401, 1025, 15, 18), (423, 1028, 36, 10), (466, 1025, 15, 18), (491, 1031, 37, 10)]
		return spritesheet.get_animation(batarang_frames, 0.01, Animation.PlayMode.LOOP, scale=1.2)

	def animate(self):
		if self.active_name == "walking":
			if self.vel.x == 0:
				self.set_active_animation("standing")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "standing":
			if abs(self.vel.x) > 0:
				self.set_active_animation("walking")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "jumping":
			if self.vel.y > 0:
				self.set_active_animation("falling")

		if self.active_name == "falling":
			if self.ground_count > 0:
				self.set_active_animation("landing")

		if self.active_name == "landing":
			if self.is_animation_finished():
				if abs(self.vel.x) > 0:
					self.set_active_animation("walking")
				else:
					self.set_active_animation("standing")
			else:
				self.vel.x = 0

		if self.active_name == 'attack1':
			if self.is_animation_finished():
				if self.attack_count > 1:
					self.set_active_animation('attack2')
				else:
					self.attack_count = 0
					self.set_active_animation("standing")

		if self.active_name == 'attack2':
			if self.is_animation_finished():
				if self.attack_count > 2:
					self.set_active_animation('attack3')
				else:
					self.attack_count = 0
					self.set_active_animation("standing")

		if self.active_name == 'attack3':
			if self.is_animation_finished():
				self.attack_count = 0
				self.set_active_animation('standing')

		if self.active_name == 'batarang_throw':
			if self.active_anim.get_frame_index(self.elapsed_time) > 1:
				if self.shoot_count == 0:
					if self.direction == 'R':
						self.screen.create_bullet(self.rect.midright, 1, PLAYER_BULLET_DAMAGE, self.screen.player_bullets, self.bullet_animation)
					elif self.direction == 'L':
						self.screen.create_bullet(self.rect.midleft, -1, PLAYER_BULLET_DAMAGE, self.screen.player_bullets, self.bullet_animation)
					self.shoot_count += 1

			if self.is_animation_finished():
				self.set_active_animation("standing")
				self.shoot_count = 0

		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		
		# flip image if necessary
		if self.direction == 'L':
			self.image = pg.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def move(self):
		if self.alive:
			keys = pg.key.get_pressed()

			if keys[pg.K_a]:
				self.direction = 'L'
				if not self.attack_count > 0 and not self.active_name == 'batarang_throw':
					self.acc.x = -PLAYER_ACC
			
			elif keys[pg.K_d]:
				self.direction = 'R'
				if not self.attack_count > 0 and not self.active_name == 'batarang_throw':
					self.acc.x = PLAYER_ACC

	def update(self):
		super().update(1/self.screen.game.fps)
		self.animate()

		# update properties
		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

		# check for death
		if self.health <= 0:
			self.health = 0
			self.alive = False
			self.set_active_animation("death");

		if self.attack_count == 1:
			self.set_active_animation("attack1")

		self.rect.midbottom = self.pos
