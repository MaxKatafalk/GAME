import pygame as pg
import math

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Explosion:
    explosion_frames = [
        pg.transform.scale(pg.image.load(f"Sprites/animations/explosion{i}.png").convert_alpha(), (500, 500))
        for i in range(1, 6)
    ]

    def __init__(self, x, y):
        self.frames = Explosion.explosion_frames
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
        future_rect = self.get_rect().inflate(-5, -5).move(dx, dy)
        collided_box = None
        for box in boxes:
            if not box.is_solid:
                continue
            if future_rect.colliderect(box.rect.inflate(-1, -1)):
                collided_box = box
                break
        if collided_box:
            speed = 0.5
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            pushed = set()
            can_push = Tank.push_chain(collided_box, dx, dy, boxes, pushed)
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
            future_x = self.x + dx
            future_y = self.y + dy
            half_width = self.width // 2
            half_height = self.height // 2

            if (half_width <= future_x <= SCREEN_WIDTH - half_width and
                half_height <= future_y <= SCREEN_HEIGHT - half_height):
                self.x = future_x
                self.y = future_y
        new_bullet = None
        if moving and not self.wasMoving:
            new_bullet = Bullet(self.x, self.y, self.angle, self, sprite_path="Sprites/bullets/shotThin.png")
        self.wasMoving = moving
        return new_bullet

    def draw(self, surface):
        if self.alive:
            if self.blink_timer > 0:
                temp = self.original_image.copy()
                temp.fill((255, 255, 255), special_flags=pg.BLEND_RGB_ADD)
                rotated = pg.transform.rotate(temp, -self.angle)
            else:
                rotated = pg.transform.rotate(self.original_image, -self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect)

    def get_rect(self):
        return pg.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    @staticmethod
    def push_chain(box, dx, dy, boxes, pushed):
        if box in pushed:
            return True

        pushed.add(box)
        box.pos += pg.math.Vector2(dx, dy)
        box.rect.center = box.pos
        if not (
                0 <= box.rect.left and box.rect.right <= SCREEN_WIDTH and 0 <= box.rect.top and box.rect.bottom <= SCREEN_HEIGHT):
            box.pos -= pg.math.Vector2(dx, dy)
            box.rect.center = box.pos
            return False
        for other in boxes:
            if other is box:
                continue
            if box.rect.inflate(1, 1).colliderect(other.rect.inflate(1, 1)):
                success = Tank.push_chain(other, dx, dy, boxes, pushed)
                if not success:
                    box.pos -= pg.math.Vector2(dx, dy)
                    box.rect.center = box.pos
                    return False
        return True


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
        return 0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT

    def draw(self, surface):
        rotated = pg.transform.rotate(self.original_image, -self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

    def get_rect(self):
        rotated = pg.transform.rotate(self.original_image, -self.angle)
        return rotated.get_rect(center=(self.x, self.y))


class GameObject:
    def __init__(self, x, y, sprite_path, width, height, is_solid=True):
        img = pg.image.load(sprite_path).convert_alpha()
        self.image = pg.transform.scale(img, (width, height))
        self.pos = pg.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = pg.math.Vector2(0, 0)
        self.is_solid = is_solid

    def update(self):
        self.pos += self.vel
        self.vel *= 0.8
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collides_with_rect(self, other_rect):
        return self.rect.colliderect(other_rect)