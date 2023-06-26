import pygame as pg
import time
import math

from os import path
from constants import *

from map import TiledMap, Camera
from player import Player
from enemies import ShooterEnemy, MeleeEnemy
from sprites import Obstacle, Bullet


vec = pg.math.Vector2

def draw_player_health(surf, x, y, outline_dir, pct):
	if pct < 0:
		pct = 0

	# prepare outline
	image = pg.image.load(path.join(outline_dir, PLAYER_BAR_OUTLINE)).convert()
	image = pg.transform.scale(image, (PLAYER_BAR_WIDTH, PLAYER_BAR_HEIGHT))
	image.set_colorkey(BLACK)

	# position
	x = x - PLAYER_BAR_WIDTH/2

	fill = pct*(PLAYER_BAR_WIDTH - 42)
	fill_rect = pg.Rect(x + 42, y + 35, fill, PLAYER_BAR_HEIGHT/4)

	if pct > 0.3:
		color = LIGHT_ORANGE
	else:
		color = RED

	surf.blit(image, (x, y))
	pg.draw.rect(surf, color, fill_rect)

def draw_health_bar(surf, camera, x, y, pct):
	if pct < 0:
		pct = 0

	x = x - ENEMY_BAR_WIDTH/2
	y = y - 20

	fill = pct * ENEMY_BAR_WIDTH
	outline_rect = pg.Rect(x, y, ENEMY_BAR_WIDTH, ENEMY_BAR_HEIGHT)
	fill_rect = pg.Rect(x, y, fill, ENEMY_BAR_HEIGHT)
	
	if pct > 0.6:
		color = GREEN
	elif pct > 0.3:
		color = YELLOW
	else:
		color = RED

	pg.draw.rect(surf, color, camera.apply_rect(fill_rect))
	pg.draw.rect(surf, WHITE, camera.apply_rect(outline_rect), 2)

def collide_with_walls(character, hit):
	# character's bottom and wall top
	if abs(hit.rect.top - character.rect.bottom) < COLLISION_TOLERANCE:
		character.vel.y = 0
		character.pos.y = hit.rect.top + 1
		character.ground_count += 1

	# character's top and wall bottom
	if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE:
		character.vel.y = 0 
		character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	if character.vel.y < 0:
		if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE + 30:
			character.vel.y = 0
			character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	# character's left and wall right
	if abs(hit.rect.right - character.rect.left) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.right + character.rect.width/2 + 1
		if (type(character) is MeleeEnemy):
			character.direction = 'R'

	# character's right and wall left
	if abs(hit.rect.left - character.rect.right) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.left - character.rect.width/2 - 1
		if (type(character) is MeleeEnemy):
			character.direction = 'L'

def combat_collisions(character, hit):
	# player's right and wall left
	if abs(hit.rect.left - character.rect.right) < COMBAT_TOLERANCE:
		if (type(hit) is MeleeEnemy):
			hit.direction = 'L'

	# character's left and wall right
	if abs(hit.rect.right - character.rect.left) < COMBAT_TOLERANCE:
		if (type(hit) is MeleeEnemy):
			hit.direction = 'R'


class Level1:
	def __init__(self, game):
		self.game = game

	def load(self):
		# prepare map
		self.map = TiledMap(path.join(self.game.map_dir, 'Base Level.tmx'))
		self.map_img, self.map_rect = self.map.make_map()

	def new(self, bar):
		progress = 0
		bar.put(progress)
		
		self.load()

		progress += 5
		bar.put(progress)

		# sprite groups
		self.all_sprites = pg.sprite.Group()
		self.melee_enemies = pg.sprite.Group()
		self.shooter_enemies = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.player_bullets = pg.sprite.Group()
		self.enemy_bullets = pg.sprite.Group()

		progress += 10
		bar.put(progress)

		increment = (90 - progress)/len(list(self.map.tmx_data.objects))
		for obj in self.map.tmx_data.objects:
			obj_midbottom = vec(obj.x + obj.width / 2, obj.y + obj.height)
			if obj.name == 'player':
				self.player = Player(self, obj_midbottom.x, obj_midbottom.y, self.all_sprites)
			elif obj.name == 'melee_enemy':
				MeleeEnemy(self, obj_midbottom.x, obj_midbottom.y, self.all_sprites, self.melee_enemies)
			elif obj.name == 'shooter_enemy':
				ShooterEnemy(self, obj_midbottom.x, obj_midbottom.y, self.all_sprites, self.shooter_enemies)
			elif obj.name == 'wall':
				Obstacle(obj.x, obj.y, obj.width, obj.height, self.walls)

			progress += increment
			bar.put(math.floor(progress))

		# camera display
		self.camera = Camera(self.game, self.map.width, self.map.height)
		self.draw_debug = True

		progress = 100
		bar.put(progress)

		time.sleep(1)

	def run(self):
		# play background music
		pg.mixer.music.load(path.join(self.game.snd_dir, 'level_track.ogg'))
		pg.mixer.music.play(loops=-1)

		while True:
			self.game.clock.tick(self.game.fps)
			self.events()
			self.update()
			self.display()

	def create_bullet(self, pos, dir, damage, group, anim=None):
		Bullet(self, vec(pos), dir, damage, anim, self.all_sprites, group)

	def events(self):
		# handle events in game loop
		for e in pg.event.get():
			if e.type == pg.QUIT:
				self.game.quit()
			elif e.type == pg.KEYDOWN:
				if self.player.alive:
					if e.key == pg.K_j:
						if not self.player.active_name == 'batarang_throw':
							self.player.attack_count += 1
				
					elif e.key == pg.K_k:
						if not self.player.active_name == 'batarang_throw':
							self.player.set_active_animation('batarang_throw')

					if e.key == pg.K_w:
						if self.player.ground_count > 0:
							self.player.vel.y = PLAYER_JUMP
							self.player.ground_count = 0


	def update(self):
		self.all_sprites.update()
		self.camera.update(self.player)
		self.check_collisions();

	def display(self):
		self.camera.draw_bg(self.game.surface, self.map_img, self.map_rect)
		self.camera.draw(self.game.surface, self.all_sprites)

		if self.draw_debug:
			self.camera.draw_debug(self.game.surface, self.all_sprites, self.walls)

		# draw health bars
		draw_player_health(self.game.surface, 120, 50, self.game.img_dir, self.player.health / HEALTH)
		for enemy in [*self.melee_enemies, *self.shooter_enemies]:
			if self.draw_debug or enemy.health < HEALTH:
				draw_health_bar(self.game.surface, self.camera, enemy.pos.x, enemy.rect.top, enemy.health / HEALTH)

		pg.display.flip()

	def check_collisions(self):
		# PLAYER COLLISIONS
		# collision with walls
		hits = pg.sprite.spritecollide(self.player, self.walls, False)
		if hits:
			for hit in hits:
				collide_with_walls(self.player, hit)

		# collisions with melee enemies
		hits = pg.sprite.spritecollide(self.player, self.melee_enemies, False)
		for hit in hits:
			hit.vel.x = 0
			hit.attack_count += 1
			combat_collisions(self.player, hit)

		# ENEMY COLLISIONS
		# melee collision with walls
		hits = pg.sprite.groupcollide(self.melee_enemies, self.walls, False, False)
		for enemy in hits:
			for hit in hits[enemy]:
				collide_with_walls(enemy, hit)

		# shooter collision with walls
		hits = pg.sprite.groupcollide(self.shooter_enemies, self.walls, False, False)
		for enemy in hits:
			for hit in hits[enemy]:
				collide_with_walls(enemy, hit)

		# BULLET COLLISIONS
		hits = pg.sprite.spritecollide(self.player, self.enemy_bullets, True)
		for hit in hits:
			self.player.health -= hit.damage

		hits = pg.sprite.groupcollide(self.shooter_enemies, self.player_bullets, False, True)
		for enemy in hits:
			for hit in hits[enemy]:
				enemy.health -= hit.damage

		hits = pg.sprite.groupcollide(self.melee_enemies, self.player_bullets, False, True)
		for enemy in hits:
			for hit in hits[enemy]:
				enemy.health -= hit.damage
