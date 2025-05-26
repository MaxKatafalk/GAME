import pygame as pg
import math

pg.init()
size = WIDTH, HEIGHT = 1800, 1000
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
font = pg.font.Font(None, 60)

def draw_text(text, center, font, color=(255,255,255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)
    return rect

TILE_SIZE = 200

tiles = [
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass1.png").convert(), (TILE_SIZE, TILE_SIZE)),#0
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass2.png").convert(), (TILE_SIZE, TILE_SIZE)),#1
	pg.transform.scale(pg.image.load("Sprites/map/tileSand1.png").convert(), (TILE_SIZE, TILE_SIZE)),#2
	pg.transform.scale(pg.image.load("Sprites/map/tileSand2.png").convert(), (TILE_SIZE, TILE_SIZE)),#3
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),#4
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),#5
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),#6
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),#7
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),#8
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),#9
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),#10
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE.png").convert(), (TILE_SIZE, TILE_SIZE)),#11
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE_dirt.png").convert(), (TILE_SIZE, TILE_SIZE)),#12
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),#13
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),#14
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),#15
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),#16
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),#17
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),#18
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),#19
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW1.png").convert(), (TILE_SIZE, TILE_SIZE)),#20
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW2.png").convert(), (TILE_SIZE, TILE_SIZE)),#21
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),#22
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),#23


]

map = [[0, 9, 0, 6, 11, 19 , 19, 13, 2], 
		 [10, 4, 10, 7, 21, 2 , 3, 18, 2], 
		 [1, 9, 1, 0 ,21, 2 , 3, 18, 2], 
		 [0, 8, 22, 10, 12, 23 , 19, 17, 19], 
		 [1, 0, 9, 1, 21, 18, 2, 18, 2] 
		]

map_cols = len(map[0])
map_rows = len(map)
map_width  = map_cols * TILE_SIZE
map_height = map_rows * TILE_SIZE

background = pg.Surface((map_width, map_height))
for row_idx, row in enumerate(map):
    for col_idx, tile_id in enumerate(row):
        x = col_idx * TILE_SIZE
        y = row_idx * TILE_SIZE
        background.blit(tiles[tile_id], (x, y))

class Tank:
	def __init__(self, x, y, width, height, color, sprite_path=None):
		self.x = x
		self.y = y
		self.width = width 
		self.height = height 
		self.color = color
		self.angle = 0
		self.speedRotation = 2
		self.rotationDirection = 1
		self.wasMoving = False 

		if sprite_path:
			img = pg.image.load(sprite_path).convert_alpha()
			self.original_image = pg.transform.scale(img, (width, height))
		else:
			self.original_image = None

	def update(self, moving):
		if moving and not self.wasMoving:
			self.rotationDirection *= -1

		if not moving:
			self.angle = (self.angle + self.speedRotation * self.rotationDirection) % 360
		else:
			rad = math.radians(self.angle)
			self.x += math.cos(rad) * 2
			self.y += math.sin(rad) * 2

		new_bullet = None
		if moving and not self.wasMoving:
			new_bullet = Bullet(self.x, self.y, self.angle, self)

		self.wasMoving = moving
		return new_bullet

	def draw(self, surface):
		if self.original_image:
			rotated = pg.transform.rotate(self.original_image, -self.angle)
			rect = rotated.get_rect(center=(self.x, self.y))
			surface.blit(rotated, rect)
		else:
			rect_surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
			pg.draw.rect(rect_surf, self.color, (0, 0, self.width, self.height))
			rotated = pg.transform.rotate(rect_surf, -self.angle)
			rect = rotated.get_rect(center=(self.x, self.y))
			surface.blit(rotated, rect)

	def get_rect(self):
		return pg.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

class Bullet:
	def __init__(self, x, y, angle, owner):
		self.x = x
		self.y = y
		self.angle = angle
		self.speed = 5
		self.radius = 5
		self.owner = owner

	def update(self):
		rad = math.radians(self.angle)
		self.x += math.cos(rad) * self.speed
		self.y += math.sin(rad) * self.speed
		return 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

	def draw(self, surface):
		pg.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

	def get_rect(self):
		return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

tanks = [
	Tank(300, 300, 60, 55, (0, 255, 0), sprite_path="Sprites/tanks/tank_blue.png"),
	Tank(1200, 700, 60, 55, (0, 0, 255), sprite_path="Sprites/tanks/tank_green.png")
]
buttons = [pg.K_UP, pg.K_w]
bullets = []
winner = None
state = "menu"

running = True
while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False

		if state == "menu" and ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
			mx, my = ev.pos
			if start_rect.collidepoint(mx, my):
					state = "game"
			elif settings_rect.collidepoint(mx, my):
					state = "settings"

		if state == "settings" and ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
			state = "menu"

	screen.fill((0,0,0))

	if state == "menu":
		draw_text("TANKS", (WIDTH//2, HEIGHT//3), font, (255,255,0))
		start_rect = draw_text("Начать игру",   (WIDTH//2, HEIGHT//2    ), font)
		settings_rect = draw_text("Настройки (Esc)", (WIDTH//2, HEIGHT//2+100), font)

	elif state == "settings":
		draw_text("Настройки: нажмите ESC, чтобы вернуться", (WIDTH//2, HEIGHT//2), font)

	elif state == "game":
		screen.blit(background, (0, 0))

		keys = pg.key.get_pressed()
		for idx, tank in enumerate(tanks):
			moving = keys[buttons[idx]]
			new_b = tank.update(moving)
			tank.draw(screen)
			if new_b:
					bullets.append(new_b)

		for b in bullets[:]:
			if not b.update():
					bullets.remove(b)
					continue
			b.draw(screen)
			for t in tanks:
					if t is not b.owner and b.get_rect().colliderect(t.get_rect()):
						winner = "Синий" if b.owner.color == (0,255,0) else "Зеленый"
						break
			if winner:
					break

		if winner:
			draw_text(f"Победил: {winner}", (WIDTH//2, HEIGHT//2), font)

	pg.display.flip()
	clock.tick(60)

pg.quit()