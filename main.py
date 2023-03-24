import random
import pygame
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GOLD = 249, 225, 7
scores = 0
IMG_PATH = 'static/image/'
IMG_PATH_GOOSE = 'static/image/goose/'
enemies = []
bonuses = []
img_index = 0

font = pygame.font.SysFont('verdana', 15)

screen = width, height = 900, 600
main_surface = pygame.display.set_mode(screen)

player_img = [pygame.transform.scale(pygame.image.load(IMG_PATH_GOOSE + image).convert_alpha(), (60, 30))
              for image in listdir(IMG_PATH_GOOSE)
              ]
player = player_img[0]
player_rect = player.get_rect()
player_speed = 5


def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load(IMG_PATH + 'enemy.png').convert_alpha(), (60, 15))
    enemy_rect = pygame.Rect(width, random.randint(0, height-15), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load(IMG_PATH + 'bonus.png').convert_alpha(), (60, 60))
    bonus_rect = pygame.Rect(random.randint(0, width-55), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

CHANGE_PLAYER_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_PLAYER_IMG, 125)

background = pygame.transform.scale(pygame.image.load(IMG_PATH + 'background.png').convert(), screen)
background_x1 = 0
background_x2 = background.get_width()
background_speed = 0.1

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

        if event.type == CHANGE_PLAYER_IMG:
            img_index += 1
            if img_index == len(player_img):
                img_index = 0
            player = player_img[img_index]

    background_x1 -= background_speed
    background_x2 -= background_speed

    if background_x1 < -background.get_width():
        background_x1 = background.get_width()

    if background_x2 < -background.get_width():
        background_x2 = background.get_width()

    main_surface.blit(background, (background_x1, 0))
    main_surface.blit(background, (background_x2, 0))

    main_surface.blit(player, player_rect)
    main_surface.blit(font.render('Scores: '+str(scores), True, BLACK), (width-120, 0))

    for specified_enemy in enemies:
        specified_enemy[1] = specified_enemy[1].move(-specified_enemy[2], 0)
        main_surface.blit(specified_enemy[0], specified_enemy[1])

        if specified_enemy[1].left < 0:
            enemies.pop(enemies.index(specified_enemy))

        if player_rect.colliderect(specified_enemy[1]):
            is_working = False

    for current_bonus in bonuses:
        current_bonus[1] = current_bonus[1].move(0, current_bonus[2])
        main_surface.blit(current_bonus[0], current_bonus[1])

        if current_bonus[1].bottom > height:
            bonuses.pop(bonuses.index(current_bonus))

        if player_rect.colliderect(current_bonus[1]):
            bonuses.pop(bonuses.index(current_bonus))
            scores += 1

    pressed_key = pygame.key.get_pressed()

    if pressed_key[K_DOWN]:
        if player_rect.bottom < height:
            player_rect = player_rect.move(0, player_speed)

    if pressed_key[K_UP]:
        if player_rect.top > 0:
            player_rect = player_rect.move(0, -player_speed)

    if pressed_key[K_LEFT]:
        if player_rect.left > 0:
            player_rect = player_rect.move(-player_speed, 0)

    if pressed_key[K_RIGHT]:
        if player_rect.right < width:
            player_rect = player_rect.move(player_speed, 0)

    pygame.display.flip()
