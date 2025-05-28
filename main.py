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

def push_chain(box, dx, dy, boxes, pushed):
	if box in pushed:
		return True
	pushed.add(box)

	box.pos += pg.math.Vector2(dx, dy)
	box.rect.center = box.pos

	if not (0 <= box.rect.left and box.rect.right <= WIDTH
			and 0 <= box.rect.top and box.rect.bottom <= HEIGHT):
		box.pos -= pg.math.Vector2(dx, dy)
		box.rect.center = box.pos
		return False

	for other in boxes:
		if other is box:
			continue
		if box.rect.inflate(-3, -3).colliderect(other.rect.inflate(-3, -3)):
			success = push_chain(other, dx, dy, boxes, pushed)
			if not success:
					box.pos -= pg.math.Vector2(dx, dy)
					box.rect.center = box.pos
					return False

	return True

class Tank:
	def __init__(self, x, y, width, height, color, sprite_path):
		self.x = x
		self.y = y
		self.width = width 
		self.height = height 
		self.color = color
		self.angle = 0
		self.speedRotation = 2
		self.pushing = False
		self.rotationDirection = 1
		self.wasMoving = False
		img = pg.image.load(sprite_path).convert_alpha()
		self.original_image = pg.transform.scale(img, (width, height))

	def update(self, moving, boxes):
		if moving and not self.wasMoving:
			self.rotationDirection *= -1

		speed = 2
		rad = math.radians(self.angle)
		dx = math.cos(rad) * speed
		dy = math.sin(rad) * speed

		future_rect = self.get_rect().inflate(-3, -3).move(dx, dy)

		collided_box = None
		for box in boxes:
			if future_rect.colliderect(box.rect.inflate(-3, -3)):
					collided_box = box
					break

		if collided_box:
			speed = 0.5
			dx = math.cos(rad) * speed
			dy = math.sin(rad) * speed

			pushed = set()
			can_push = push_chain(collided_box, dx, dy, boxes, pushed)

			if not can_push:
				dx = dy = 0
			else:
				if not self.pushing:
					for b in pushed:
						b.vel = pg.math.Vector2(dx, dy)
					self.pushing = True
		else:
			self.pushing = False

		if not moving:
			self.angle = (self.angle + self.speedRotation * self.rotationDirection) % 360
		else:
			self.x += dx
			self.y += dy

		new_bullet = None
		if moving and not self.wasMoving:
			new_bullet = Bullet(self.x, self.y, self.angle, self, sprite_path="Sprites/bullets/shotThin.png")

		self.wasMoving = moving
		return new_bullet

	def draw(self, surface):
			rotated = pg.transform.rotate(self.original_image, -self.angle)
			rect = rotated.get_rect(center=(self.x, self.y))
			surface.blit(rotated, rect)

	def get_rect(self):
		return pg.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

class Bullet:
	def __init__(self, x, y, angle, owner, sprite_path):
		self.x = x
		self.y = y
		self.angle = angle
		self.speed = 5
		self.owner = owner

		img = pg.image.load(sprite_path).convert_alpha()
		self.original_image = pg.transform.scale(img, (30, 10))

	def update(self):
		rad = math.radians(self.angle)
		self.x += math.cos(rad) * self.speed
		self.y += math.sin(rad) * self.speed
		return 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

	def draw(self, surface):
		rotated = pg.transform.rotate(self.original_image, -self.angle)
		rect = rotated.get_rect(center=(self.x, self.y))
		surface.blit(rotated, rect)

	def get_rect(self):
		rotated = pg.transform.rotate(self.original_image, -self.angle)
		return rotated.get_rect(center=(self.x, self.y))
	
class GameObject:
	def __init__(self, x, y, sprite_path, width, height):
		img = pg.image.load(sprite_path).convert_alpha()
		self.image = pg.transform.scale(img, (width, height))
		self.pos = pg.math.Vector2(x, y)
		self.rect = self.image.get_rect(center=self.pos)
		self.vel = pg.math.Vector2(0, 0)

	def update(self):
		self.pos += self.vel
		self.vel *= 0.8
		self.rect.center = self.pos

	def draw(self, surface):
		surface.blit(self.image, self.rect)

	def collides_with_rect(self, other_rect):
		return self.rect.colliderect(other_rect)

boxes = [
	GameObject(200, 200, "Sprites/objects/crateWood.png", width=40, height=40),
	GameObject(600, 300, "Sprites/objects/crateWood.png", width=40, height=40),
	GameObject(1100, 300, "Sprites/objects/barricadeWood.png", width=40, height=40),
	GameObject(700, 300, "Sprites/objects/barricadeWood.png", width=40, height=40),
	GameObject(900, 300, "Sprites/objects/barricadeWood.png", width=40, height=40),
]


tanks = [
	Tank(1200, 700, 60, 55, (0, 255, 0), sprite_path="Sprites/tanks/tank_blue.png"),
	Tank(300, 300, 60, 55, (0, 0, 255), sprite_path="Sprites/tanks/tank_green.png")
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
		start_rect = draw_text("Начать игру",   (WIDTH//2, HEIGHT//2), font)
		settings_rect = draw_text("Настройки (Esc)", (WIDTH//2, HEIGHT//2 + 100), font)

	elif state == "settings":
		draw_text("Настройки: нажмите ESC, чтобы вернуться", (WIDTH//2, HEIGHT//2), font)

	elif state == "game":
		screen.blit(background, (0, 0))
		for box in boxes:
			box.update()
			box.draw(screen)
		
		keys = pg.key.get_pressed()
		for idx, tank in enumerate(tanks):
			moving = keys[buttons[idx]]
			new_b = tank.update(moving, boxes)
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