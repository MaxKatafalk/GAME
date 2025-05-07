import pygame as pg

pg.init()
screen = pg.display.set_mode(1000, 1000)

running = True

while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False
			
pg.quit()