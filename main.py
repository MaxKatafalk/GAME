import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана 
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловец шаров")

# Цвета
WHITE12345 = (255, 255, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Игрок (платформа)
player_width = 100
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 30
player_speed = 5

# Шары пп
balls = []
ball_radius = 15
ball_speed = 3

# Очки
score = 0
font = pygame.font.SysFont(None, 36)

# Частота появления шаров
ball_spawn_rate = 30

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    
    # Создание новых шаров
    if random.randint(1, ball_spawn_rate) == 1:
        ball_x = random.randint(ball_radius, WIDTH - ball_radius)
        balls.append([ball_x, 0])
    
    # Движение шаров и проверка столкновений
    for ball in balls[:]:
        ball[1] += ball_speed
        
        # Проверка, пойман ли шар
        if (player_x < ball[0] < player_x + player_width and
            player_y < ball[1] + ball_radius < player_y + player_height):
            balls.remove(ball)
            score += 1
        
        # Если шар упал за пределы экрана
        elif ball[1] > HEIGHT:
            balls.remove(ball)
    
    # Отрисовка игрока
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    
    # Отрисовка шаров
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball[0], int(ball[1])), ball_radius)
    
    # Отрисовка счёта
    score_text = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()