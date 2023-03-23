import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
WHITE = 255, 255, 255
RED = 255, 0, 0
GOLD = 249, 225, 7
FPS = pygame.time.Clock()

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)
ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 5


def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.Surface((20, 20))
    bonus.fill(GOLD)
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

enemies = []
bonuses = []
is_working = True

while is_working:
    FPS.tick(80)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    main_surface.fill((24, 145, 26))
    main_surface.blit(ball, ball_rect)

    for specified_enemy in enemies:
        specified_enemy[1] = specified_enemy[1].move(-specified_enemy[2], 0)
        main_surface.blit(specified_enemy[0], specified_enemy[1])

        if specified_enemy[1].left < 0:
            enemies.pop(enemies.index(specified_enemy))

        if ball_rect.colliderect(specified_enemy[1]):
            enemies.pop(enemies.index(specified_enemy))

    for current_bonus in bonuses:
        current_bonus[1] = current_bonus[1].move(0, current_bonus[2])
        main_surface.blit(current_bonus[0], current_bonus[1])

        if current_bonus[1].bottom > height:
            bonuses.pop(bonuses.index(current_bonus))

        if ball_rect.colliderect(current_bonus[1]):
            bonuses.pop(bonuses.index(current_bonus))

    pressed_key = pygame.key.get_pressed()

    if pressed_key[K_DOWN]:
        if ball_rect.bottom < height:
            ball_rect = ball_rect.move(0, ball_speed)

    if pressed_key[K_UP]:
        if ball_rect.top > 0:
            ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_key[K_LEFT]:
        if ball_rect.left > 0:
            ball_rect = ball_rect.move(-ball_speed, 0)

    if pressed_key[K_RIGHT]:
        if ball_rect.right < width:
            ball_rect = ball_rect.move(ball_speed, 0)

    pygame.display.flip()
