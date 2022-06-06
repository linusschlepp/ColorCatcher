import math
import random

import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 55
HEIGHT = 40
MAX_HEIGT = 750
MAX_WIDTH = 750

WIN = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGT))

pygame.display.set_caption("ColorCatcher")

STAR = pygame.image.load('assets/star.png')
STAR = pygame.transform.scale(STAR, (WIDTH, HEIGHT))

RHOMBUS = pygame.image.load('assets/rhombus.png')
RHOMBUS = pygame.transform.scale(RHOMBUS, (WIDTH, HEIGHT))

SQUARE = pygame.image.load('assets/square.png')
SQUARE = pygame.transform.scale(SQUARE, (WIDTH, HEIGHT))

PLAYER_PLATFORM = pygame.image.load('assets/player_platform.png')
PLAYER_PLATFORM = pygame.transform.scale(SQUARE, (WIDTH, HEIGHT))

FPS = 60
VEL = 5


def update_window(rect, rect_1, player_platform):
    WIN.fill(WHITE)
    WIN.blit(PLAYER_PLATFORM, (player_platform.x, player_platform.y))
    WIN.blit(STAR, (rect.x, rect.y))
    WIN.blit(SQUARE, (rect_1.x, rect_1.y))
    pygame.display.update()


def handle_movement_player(keys_pressed, player_platform):
    if keys_pressed[pygame.K_a]:
        if player_platform.x >= 0:
            player_platform.x -= VEL
    if keys_pressed[pygame.K_d]:
        if player_platform.x <= MAX_WIDTH - WIDTH:
            player_platform.x += VEL


def update_score(player_platform, rect, rect_1, score_count):
    if player_platform.colliderect(rect):
        score_count += 1
        print(score_count)
    if player_platform.colliderect(rect_1):
        score_count += 1
        print(score_count)



def main():
    score_count = 0
    rect = pygame.Rect(400, 0, WIDTH, HEIGHT)
    rect_1 = pygame.Rect(100, 0, WIDTH, HEIGHT)
    player_platform = pygame.Rect(375, 675, WIDTH - 30, HEIGHT - 30)
    different_objects = [STAR, RHOMBUS, SQUARE]
    objects= []

    for object in range(1000000):
        objects.append(pygame.Rect(float(random.randrange(0, MAX_WIDTH)), 0, WIDTH, HEIGHT))


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        handle_movement_player(keys_pressed, player_platform)
        update_score(player_platform, rect, rect_1, score_count)

        rect.y += 1
        rect_1.y += 1


        if rect.y >= MAX_HEIGT and rect_1.y >= MAX_HEIGT:
            rect.y = 0
            rect_1.y = 0

        update_window(rect, rect_1, player_platform)


if __name__ == "__main__":
    main()
