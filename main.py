import pygame as pg
import math

pg.init()
size = WIDTH, HEIGHT = 1500, 1200
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
font = pg.font.Font(None, 60)

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
	Tank(300, 300, 60, 55, (0, 255, 0), sprite_path="tanks/tank_blue.png"),
	Tank(1200, 1000, 60, 55, (0, 0, 255), sprite_path="tanks/tank_green.png")
]
buttons = [pg.K_UP, pg.K_w]

bullets = []
winner = None
running = True

while running:
	for ev in pg.event.get():
		if ev.type == pg.QUIT:
			running = False

	screen.fill((30, 30, 30))
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
					winner = "Зелёный" if b.owner.color == (0, 255, 0) else "Синий"
					break
		if winner:
			break

	if winner:
		text = font.render(f"Победил: {winner}", True, (255, 255, 255))
		text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
		screen.blit(text, text_rect)

	pg.display.flip()
	clock.tick(60)

pg.quit()
