import pygame as pg

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

running = True
while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False
			
pg.quit()