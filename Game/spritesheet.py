import pygame as pg

from enum import Enum


class Spritesheet:
	def __init__(self, filename, bg=None):
		self.spritesheet = pg.image.load(filename).convert()
		self.bg = bg

	def get_image(self, frame, scale=None, flip=False):
		image = self.spritesheet.subsurface(pg.Rect(frame))
		
		if scale is not None:
			image = pg.transform.scale(image, (frame[2]*scale, frame[3]*scale))

		if flip:
			image = pg.transform.flip(image, True, False)

		if self.bg is not None:
			image.set_colorkey(self.bg)

		return image

	def get_animation(self, coords, frame_duration, mode, scale=None, flip=None):
		# extract images & create animation
		frames = [self.get_image(frame, scale, flip) for frame in coords]
		return Animation(frames, frame_duration, mode)


class Animation:
	class PlayMode(Enum):
		NORMAL = 1
		REVERSED = 2
		LOOP = 3
		LOOP_REVERSED = 4
		LOOP_PINGPONG = 5
		LOOP_RANDOM = 6

	def __init__(self, frames, frame_duration, mode):
		# assign animation settings
		self.frames = frames
		self.frame_duration = frame_duration
		self.animation_duration = len(self.frames)*self.frame_duration
		self.mode = mode
		
		# keep track of animation
		self.last_frame_number = 0
		self.last_state_time = 0

	def get_frame(self, state_time):
		frame_number = self.get_frame_index(state_time)
		return self.frames[frame_number]

	def get_frame_index(self, state_time):
		if len(self.frames) == 1:
			return 0

		frame_number = int(state_time/self.frame_duration)

		# set frame number by animation play mode
		if self.mode == self.PlayMode.NORMAL:
			frame_number = min(len(self.frames) - 1, frame_number)
		elif self.mode == self.PlayMode.LOOP:
			frame_number = frame_number % len(self.frames)
		elif self.mode == self.PlayMode.LOOP_PINGPONG:
			frame_number = frame_number % ((len(self.frames) * 2 ) - 2)
			if frame_number >= len(self.frames):
				frame_number = len(self.frames) - 2 - (frame_number - len(self.frames))

		self.last_frame_number = frame_number
		self.last_state_time = state_time

		return frame_number

	def is_animation_finished(self, state_time):
		frame_number = int(state_time/self.frame_duration)
		return len(self.frames) - 1 < frame_number

