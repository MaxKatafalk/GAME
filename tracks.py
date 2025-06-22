import pygame as pg
import math

class TrackMark:
	def __init__(self, x, y, angle, timestamp):
		self.x = x
		self.y = y
		self.angle = angle
		self.spawn_time = timestamp

class TankTracks:
	def __init__(
		self,
		sprite_path,
		spacing=20,
		fade_time=0.8,
		track_width=20,
		track_height=40
	):
		self.original_img = pg.image.load(sprite_path).convert_alpha()
		self.spacing = spacing
		self.fade_time = fade_time
		self.tracks = []
		self._last_pos = None
		self._accum_dist = 0.0
		self.track_width = track_width
		self.track_height = track_height

	def update(self, x, y, angle):
		now = pg.time.get_ticks() / 1000.0
		if self._last_pos is None:
				self._last_pos = (x, y)
				return

		dx = x - self._last_pos[0]
		dy = y - self._last_pos[1]
		dist = math.hypot(dx, dy)
		self._accum_dist += dist
		self._last_pos = (x, y)

		if self._accum_dist >= self.spacing:
				self._accum_dist %= self.spacing
				self.tracks.append(TrackMark(x, y, angle, now))

		self.tracks = [
				m for m in self.tracks
				if now - m.spawn_time <= self.fade_time
		]

	def draw(self, surface):
		now = pg.time.get_ticks() / 1000.0
		for m in self.tracks:
				age = now - m.spawn_time
				alpha = max(0, 255 - int(255 * (age / self.fade_time)))

				img = pg.transform.scale(self.original_img, (self.track_width, self.track_height))
				img.set_alpha(alpha)
				rotated = pg.transform.rotate(img, -m.angle)
				rect = rotated.get_rect(center=(m.x, m.y))
				surface.blit(rotated, rect)