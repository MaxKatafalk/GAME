import pygame
import sys

# Инициализация Pygame
pygame.init()
hui='chlen'
# Размер окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мой первый Pygame")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры шарика
x, y = WIDTH // 2, HEIGHT // 2
radius = 30
speed_x, speed_y = 5, 3

# Основной цикл
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)  # Ограничение до 60 кадров в секунду

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Логика движения шарика
    x += speed_x
    y += speed_y

    # Отскоки от стенок
    if x - radius <= 0 or x + radius >= WIDTH:
        speed_x = -speed_x
    if y - radius <= 0 or y + radius >= HEIGHT:
        speed_y = -speed_y

    # Рисование
    screen.fill(WHITE)  # Заливка фона белым
    pygame.draw.circle(screen, RED, (x, y), radius)  # Рисуем шарик

    pygame.display.flip()  # Обновляем экран

# Завершение работы
pygame.quit()
sys.exit()
