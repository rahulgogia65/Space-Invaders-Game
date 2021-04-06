import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')

icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('gaming.png')
enemy_img = pygame.image.load('enemy.png')
background = pygame.image.load('background.png')
bullet = pygame.image.load('bullet.png')

mixer.music.load('background.wav')
mixer.music.play(-1)


player_x = 370
player_y = 480
player_speed = 0

enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
enemy_x_speed = 4
enemy_y_speed = 0

bullet_x = bullet_y = 0


running = True
kleft = kright = False
bullet_stat = False
game = False

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
game_txt = pygame.font.Font('freesansbold.ttf', 80)

text_x = 10
text_y = 10


def game_over():
    msg = game_txt.render('GAME OVER!', True, (255, 255, 255))
    screen.blit(msg, (150, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x, 2))+(math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


while running:

    # screen.fill((255, 0, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:

                kleft = True
                player_speed = -5
                # print('kleft is true')

            if event.key == pygame.K_RIGHT:

                kright = True
                player_speed = 5

                # print('kright is true')

            if event.key == pygame.K_SPACE:
                if bullet_stat is False:
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_stat = True
                    bullet_x = player_x + 16
                    bullet_y = player_y - 20

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                # print('kleft is false')
                if kleft is True and kright is True:
                    player_speed = 5
                kleft = False

            if event.key == pygame.K_RIGHT:

                # print('kright is false')
                if kleft is True and kright is True:
                    player_speed = -5
                kright = False

        if kleft is False and kright is False:
            player_speed = 0

    if player_x <= 0:
        player_x = 0

    elif player_x >= 736:
        player_x = 736

    player_x += player_speed

    if enemy_x <= 0:
        enemy_x_speed = 4
        enemy_y += 25

    elif enemy_x >= 736:
        enemy_x_speed = -4
        enemy_y += 25

    enemy_x += enemy_x_speed

    if enemy_y > 440 or score_value == 10:
        game = True

    if bullet_stat:
        bullet_y -= 10
        screen.blit(bullet, (bullet_x, bullet_y))
        if bullet_y <= 0:
            bullet_stat = False

    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)

    if collision:
        collision_sound = mixer.Sound('explosion.wav')
        collision_sound.play()
        bullet_stat = False
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)
        score_value += 1

    player(player_x, player_y)

    if game:
        game_over()
    else:
        enemy(enemy_x, enemy_y)

    show_score(text_x, text_y)

    pygame.display.update()
