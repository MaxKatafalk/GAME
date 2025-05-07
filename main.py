import pygame as pg
import math

pg.init()
screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()

class Tank:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width 
		self.height = height 
		self.color = color
		self.angle = 0
		self.speed = 0
		self.speedRotation = 2
		self.surface = pg.Surface((width, height), pg.SRCALPHA)

	def update(self, moving):
		if not moving:
			self.angle = (self.angle + self.speedRotation) % 360
		else:
			radian = math.radians(self.angle)
			self.x += math.cos(radian) * 2
			self.y += math.sin(radian) * 2

	def draw(self, surface):
		rectSurf = pg.Surface((self.width, self.height), pg.SRCALPHA)
		pg.draw.rect(rectSurf, self.color, (0, 0, self.width, self.height))
		rotated = pg.transform.rotate(rectSurf, -self.angle)
		rect = rotated.get_rect(center=(self.x, self.y))
		surface.blit(rotated, rect)


tanks = [Tank(300, 300, 100, 40, (0, 255, 0)), Tank(500, 500, 100, 40, (0, 0, 255))]

buttons = [pg.K_UP, pg.K_w]

running = True

while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False

	screen.fill((30, 30, 30))

	keys = pg.key.get_pressed()

	for index, tank in enumerate(tanks):
		moving = keys[buttons[index]]
		tank.update(moving)
		tank.draw(screen)

	pg.display.flip()
	clock.tick(60)
			
pg.quit()