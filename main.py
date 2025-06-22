import pygame as pg
from tracks import TankTracks
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT, screen
from objects import Explosion
from levels import init_map

pg.init()
clock = pg.time.Clock()

def draw_text(text, center, font, color=(255, 255, 255)):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)
    return rect

track_manager = TankTracks(
    "Sprites/animations/tracksSmall.png",
    spacing=1000,      
    fade_time=0.8,
    track_width=30,
    track_height=50
)

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

def reset_round():
    global background, tanks, winner, boxes, bullets, explosions, round_over
    if score_blue < 3 and score_green < 3:
        background, boxes, tanks, bullets, explosions, winner = init_map(current_map)
        round_over = False

state = "menu"
running = True
start_rect = None
settings_rect = None
map_rects = None
return_rect = None
final_button = None

while running:
    for ev in pg.event.get():
        match ev.type:
            case pg.QUIT:
                running = False
            case pg.KEYDOWN if ev.key == pg.K_ESCAPE:
                match state:
                    case "settings" | "game":
                        background = None
                        boxes = tanks = bullets = explosions = []
                        winner = None
                        state = "menu"
                    case _:
                        pass
            case pg.MOUSEBUTTONDOWN if ev.button == 1:
                mx, my = ev.pos
                match state:
                    case "menu":
                        if start_rect.collidepoint(mx, my):
                            state = "map_selection"
                        elif settings_rect.collidepoint(mx, my):
                            state = "settings"
                    case "map_selection":
                        for i, map_rect in enumerate(map_rects):
                            if map_rect.collidepoint(mx, my):
                                current_map = i
                                (background, boxes, tanks,
                                bullets, explosions, winner) = init_map(i)
                                score_blue = score_green = 0
                                round_over = False
                                state = "game"
                                break
                    case "final":
                        if final_button.collidepoint(mx, my):
                            background = None
                            boxes = tanks = bullets = explosions = []
                            winner = None
                            state = "menu"
                    case _:
                        pass

    screen.fill((0, 0, 0))

    match state:
        case "menu":
            draw_text("TANKS", (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), FONT, (255,255,0))
            start_rect = draw_text("Начать игру", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), FONT)
            settings_rect = draw_text("Настройки (Esc)", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), FONT)

        case "settings":
            draw_text("Настройки: нажмите ESC, чтобы вернуться",
                    (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), FONT)

        case "map_selection":
            draw_text("Выберите карту", (SCREEN_WIDTH//2, SCREEN_HEIGHT//4), FONT, (255,255,0))
            map_rects = [
                draw_text(f"Карта {i+1}",
                        (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60 + i*60),
                        FONT)
                for i in range(3)
            ]

        case "game":
            if background is None:
                (background, boxes, tanks, bullets, explosions, winner) = init_map(current_map)

                track_manager = TankTracks(
                    "Sprites/animations/tracksSmall.png",
                    spacing=1000,      
                    fade_time=0.8,
                    track_width=30,
                    track_height=50
                )

            screen.blit(background, (0, 0))

            track_manager.draw(screen)

            for box in boxes:
                box.update()
                box.draw(screen)

            keys = pg.key.get_pressed()
            buttons = [pg.K_UP, pg.K_w]
            for idx, tank in enumerate(tanks):
                moving = keys[buttons[idx]]
                new_b = tank.update(moving, boxes)
                track_manager.update(tank.x, tank.y, tank.angle)
                tank.draw(screen)
                if new_b and not round_over:
                    bullets.append(new_b)

            for b in bullets[:]:
                if not b.update(boxes):
                    bullets.remove(b); continue
                b.draw(screen)
                if not round_over:
                    for t in tanks:
                        if (t.alive and t is not b.owner and b.get_rect().colliderect(t.get_rect())):
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
                for i in range(tanks[0].lives):
                    screen.blit(heart_img, (SCREEN_WIDTH - 20 - (i+1)*50, 20))
                for i in range(tanks[1].lives):
                    screen.blit(heart_img, (20 + i*50, 20))

            draw_text(f"Зеленый: {score_green}   Синий: {score_blue}",
                    (SCREEN_WIDTH//2, 30), FONT)

            if round_over and not explosions:
                reset_round()
            if score_blue >= 3 or score_green >= 3:
                winner = "Синий" if score_blue > score_green else "Зеленый"
                state = "final"

        case "final":
            draw_text(f"Победил: {winner}",
                    (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30), FONT)
            final_button = pg.draw.rect(screen, (200,50,50),(SCREEN_WIDTH//2 -100, SCREEN_HEIGHT//2 +30, 200,60))
            draw_text("В меню", (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +60), FONT)

    pg.display.flip()
    clock.tick(60)

pg.quit()