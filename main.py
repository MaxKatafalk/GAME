import pygame as pg
import math

pg.init()
WIDTH, HEIGHT = 1800, 1000
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
font = pg.font.Font(None, 60)

def draw_text(text, center, font, color=(255,255,255)):
	surf = font.render(text, True, color)
	rect = surf.get_rect(center=center)
	screen.blit(surf, rect)
	return rect

TILE_SIZE = 200
tiles = [
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass1.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass2.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand1.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand2.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadTransitionE_dirt.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLL.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerLR.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUL.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCornerUR.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadCrossing.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadNorth.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadEast.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW1.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_transitionW2.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileGrass_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),
	pg.transform.scale(pg.image.load("Sprites/map/tileSand_roadSplitS.png").convert(), (TILE_SIZE, TILE_SIZE)),
]

base_map_matrix = [
	[0, 9, 0, 6, 11, 19, 19, 13, 2],
	[10, 4, 10, 7, 21, 2, 3, 18, 2],
	[1, 9, 1, 0, 21, 2, 3, 18, 2],
	[0, 8, 22, 10, 12, 23, 19, 17, 19],
	[1, 0, 9, 1, 21, 18, 2, 18, 2]
]
base_objects = [
	(200, 200, "Sprites/objects/crateWood.png", 40, 40),
	(600, 300, "Sprites/objects/crateWood.png", 40, 40),
	(1100, 300, "Sprites/objects/barricadeWood.png", 40, 40),
	(700, 300, "Sprites/objects/barricadeWood.png", 40, 40),
	(900, 300, "Sprites/objects/barricadeWood.png", 40, 40),
]
base_tank_positions = [
	(1200, 700, (0, 255, 0), "Sprites/tanks/tank_blue.png"),
	(300, 300, (0, 0, 255), "Sprites/tanks/tank_green.png"),
]
maps_data = [
	{"map_matrix": base_map_matrix, "objects": base_objects, "tanks_positions": base_tank_positions},
	{"map_matrix": base_map_matrix, "objects": base_objects, "tanks_positions": base_tank_positions},
	{"map_matrix": base_map_matrix, "objects": base_objects, "tanks_positions": base_tank_positions},
]

heart_img = pg.image.load("Sprites/map/images.png").convert_alpha()
heart_img = pg.transform.scale(heart_img, (50, 40))

background = None
boxes = []
tanks = []
bullets = []
explosions = []
winner = None
current_map = 0
score_blue = 0
score_green = 0
round_over = False

explosion_frames = [
	pg.transform.scale(pg.image.load(f"Sprites/animations/explosion{i}.png").convert_alpha(), (500, 500))
	for i in range(1, 6)
]

class Explosion:
	def __init__(self, x, y):
		self.frames = explosion_frames
		self.index = 0
		self.image = self.frames[0]
		self.rect = self.image.get_rect(center=(x, y))
		self.timer = 0
		self.frame_rate = 5
		self.finished = False
	def update(self):
		self.timer += 1
		if self.timer >= self.frame_rate:
			self.timer = 0
			self.index += 1
			if self.index < len(self.frames):
					self.image = self.frames[self.index]
			else:
					self.finished = True
	def draw(self, surface):
		if not self.finished:
			surface.blit(self.image, self.rect)

def push_chain(box, dx, dy, boxes, pushed):
	if box in pushed:
		return True
	pushed.add(box)
	box.pos += pg.math.Vector2(dx, dy)
	box.rect.center = box.pos
	if not (0 <= box.rect.left and box.rect.right <= WIDTH and 0 <= box.rect.top and box.rect.bottom <= HEIGHT):
		box.pos -= pg.math.Vector2(dx, dy)
		box.rect.center = box.pos
		return False
	for other in boxes:
		if other is box:
			continue
		if box.rect.inflate(-7, -7).colliderect(other.rect.inflate(-7, -7)):
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
		self.alive = True
		self.lives = 3
		self.blink_timer = 0
		img = pg.image.load(sprite_path).convert_alpha()
		self.original_image = pg.transform.scale(img, (width, height))
	def update(self, moving, boxes):
		if self.blink_timer > 0:
			self.blink_timer -= 1
		if not self.alive:
			return None
		if moving and not self.wasMoving:
			self.rotationDirection *= -1
		speed = 2
		rad = math.radians(self.angle)
		dx = math.cos(rad) * speed
		dy = math.sin(rad) * speed
		future_rect = self.get_rect().inflate(-7, -7).move(dx, dy)
		collided_box = None
		for box in boxes:
			if future_rect.colliderect(box.rect.inflate(-7, -7)):
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
		if self.alive:
			if self.blink_timer > 0:
					temp = self.original_image.copy()
					temp.fill((255,255,255), special_flags=pg.BLEND_RGB_ADD)
					rotated = pg.transform.rotate(temp, -self.angle)
			else:
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
	def update(self, boxes):
		rad = math.radians(self.angle)
		self.x += math.cos(rad) * self.speed
		self.y += math.sin(rad) * self.speed
		self.rect = self.get_rect()
		for box in boxes:
			if self.rect.colliderect(box.rect):
					return False
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

def init_map(map_index):
	global background, boxes, tanks, bullets, explosions, winner
	data = maps_data[map_index]
	matrix = data["map_matrix"]
	rows = len(matrix)
	cols = len(matrix[0])
	bg_w = cols * TILE_SIZE
	bg_h = rows * TILE_SIZE
	background = pg.Surface((bg_w, bg_h))
	for r, row in enumerate(matrix):
		for c, tile_id in enumerate(row):
			background.blit(tiles[tile_id], (c * TILE_SIZE, r * TILE_SIZE))
	boxes = []
	for (x, y, sprite, w, h) in data["objects"]:
		boxes.append(GameObject(x, y, sprite, w, h))
	tanks = []
	for (x, y, color, sprite) in data["tanks_positions"]:
		tanks.append(Tank(x, y, 60, 55, color, sprite))
	bullets = []
	explosions = []
	winner = None
	return tanks, boxes, bullets, explosions

def reset_round():
	global tanks, boxes, bullets, explosions, round_over
	if score_blue < 3 and score_green < 3:
		tanks, boxes, bullets, explosions = init_map(current_map)
		round_over = False

state = "menu"
running = True
start_rect = None
settings_rect = None
map1_rect = map2_rect = map3_rect = None
return_rect = None
final_button = None

while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False
		if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
			mx, my = ev.pos
			if state == "menu":
					if start_rect and start_rect.collidepoint(mx, my):
						state = "map_selection"
					elif settings_rect and settings_rect.collidepoint(mx, my):
						state = "settings"
			elif state == "map_selection":
					if map1_rect and map1_rect.collidepoint(mx, my):
						current_map = 0
						tanks, boxes, bullets, explosions = init_map(0)
						score_blue = 0
						score_green = 0
						round_over = False
						state = "game"
					elif map2_rect and map2_rect.collidepoint(mx, my):
						current_map = 1
						tanks, boxes, bullets, explosions = init_map(1)
						score_blue = 0
						score_green = 0
						round_over = False
						state = "game"
					elif map3_rect and map3_rect.collidepoint(mx, my):
						current_map = 2
						tanks, boxes, bullets, explosions = init_map(2)
						score_blue = 0
						score_green = 0
						round_over = False
						state = "game"
			elif state == "game":
					if return_rect and return_rect.collidepoint(mx, my):
						background = None
						boxes = []
						tanks = []
						bullets = []
						explosions = []
						winner = None
						state = "menu"
			elif state == "final":
					if final_button and final_button.collidepoint(mx, my):
						background = None
						boxes = []
						tanks = []
						bullets = []
						explosions = []
						winner = None
						state = "menu"
		if state == "settings" and ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
			state = "menu"
		if state == "game" and ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
			background = None
			boxes = []
			tanks = []
			bullets = []
			explosions = []
			winner = None
			state = "menu"

	screen.fill((0, 0, 0))

	if state == "menu":
		draw_text("TANKS", (WIDTH//2, HEIGHT//3), font, (255,255,0))
		start_rect = draw_text("Начать игру", (WIDTH//2, HEIGHT//2), font)
		settings_rect = draw_text("Настройки (Esc)", (WIDTH//2, HEIGHT//2 + 100), font)

	elif state == "settings":
		draw_text("Настройки: нажмите ESC, чтобы вернуться", (WIDTH//2, HEIGHT//2), font)

	elif state == "map_selection":
		draw_text("Выберите карту", (WIDTH//2, HEIGHT//4), font, (255,255,0))
		map1_rect = draw_text("Карта 1", (WIDTH//2, HEIGHT//2 - 60), font)
		map2_rect = draw_text("Карта 2", (WIDTH//2, HEIGHT//2), font)
		map3_rect = draw_text("Карта 3", (WIDTH//2, HEIGHT//2 + 60), font)

	elif state == "game":
		if background is None:
			tanks, boxes, bullets, explosions = init_map(current_map)
		screen.blit(background, (0, 0))
		for box in boxes:
			box.update()
			box.draw(screen)
		keys = pg.key.get_pressed()
		buttons = [pg.K_UP, pg.K_w]
		for idx, tank in enumerate(tanks):
			moving = keys[buttons[idx]]
			new_b = tank.update(moving, boxes)
			tank.draw(screen)
			if new_b and not round_over:
					bullets.append(new_b)
		for b in bullets[:]:
			if not b.update(boxes):
					bullets.remove(b)
					continue
			b.draw(screen)
			if not round_over:
					for t in tanks:
						if t.alive and t is not b.owner and b.get_rect().colliderect(t.get_rect()):
							t.lives -= 1
							t.blink_timer = 15
							bullets.remove(b)
							if t.lives <= 0:
									t.alive = False
									explosions.append(Explosion(t.x, t.y))
									other = tanks[0] if t is tanks[1] else tanks[1]
									if other.color == (0,255,0):
										score_blue += 1
									else:
										score_green += 1
									round_over = True
							break
		for ex in explosions[:]:
			ex.update()
			ex.draw(screen)
			if ex.finished:
					explosions.remove(ex)
		if len(tanks) >= 2:
			blue_tank = tanks[0]
			green_tank = tanks[1]
			for i in range(blue_tank.lives):
					x = 20 + i * 50
					y = 20
					screen.blit(heart_img, (x, y))
			for i in range(green_tank.lives):
					x = WIDTH - (i + 1) * 50 - 20
					y = 20
					screen.blit(heart_img, (x, y))
		score_text = f"Зеленый: {score_green}   Синий: {score_blue}"
		draw_text(score_text, (WIDTH//2, 30), font)
		if round_over and not explosions:
			reset_round()
		if score_blue >= 3 or score_green >= 3:
			winner = "Синий" if score_blue > score_green else "Зеленый"
			state = "final"

	elif state == "final":
		draw_text(f"Победил: {winner}", (WIDTH//2, HEIGHT//2 - 30), font)
		final_button = pg.draw.rect(screen, (200,50,50), (WIDTH//2 - 100, HEIGHT//2 + 30, 200, 60))
		draw_text("В меню", (WIDTH//2, HEIGHT//2 + 60), font)

	pg.display.flip()
	clock.tick(60)

pg.quit()
